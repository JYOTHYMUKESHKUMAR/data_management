from django.contrib import admin
from django import forms
from django.db import models
from django.db.models import Sum
import csv
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from collections import defaultdict
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import fields, resources,widgets
from django.contrib.auth.decorators import user_passes_test
from .models import Category, Product,  UpdateCashIn, UpdateCashOut, AvailableBalance,Dashboard, Summary,UserActionLog


class UpdateCashInInline(admin.TabularInline):
    model = UpdateCashIn
    extra = 1

class UpdateCashOutInline(admin.TabularInline):
    model = UpdateCashOut
    extra = 1



class UpdateCashInResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id', widget=widgets.IntegerWidget())

    income_source = fields.Field(
        column_name='Income Source',
        attribute='income_source',
        widget=widgets.CharWidget()  # Use CharWidget instead of ForeignKeyWidget
    )
    class Meta:
        model = UpdateCashIn
        fields = ('id', 'date', 'income_source','project','cost_center', 'cash_in', 'status', 'remark') 
        export_order = fields # Include 'id' in the fields for import
    def before_import_row(self, row, **kwargs):
        # Disable date validation to allow importing all data
        pass 
class UpdateCashInAdminForm(forms.ModelForm):
    class Meta:
        model = UpdateCashIn
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Check if it's a new record (not being edited)
            self.fields['processed'].initial = True  # Set processed checkbox to True by default
            self.fields['processed'].widget = forms.HiddenInput() 


class UpdateCashInAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_class = UpdateCashInResource
    list_display = ['date', 'income_source','project', 'cost_center', 'cash_in', 'status', 'remark']
    search_fields = ['income_source', 'date', 'project', 'cost_center']
    list_filter = ['date','status', 'cost_center']
    ordering = ['-date']
    form = UpdateCashInAdminForm
    
    actions = ['update_summary_action', 'delete_all_data_action']
    
    def delete_all_data_action(self, request, queryset):
        # Delete all records from UpdateCashIn model
        UpdateCashIn.objects.all().delete()

        # Delete all records from UpdateCashOut model
        UpdateCashOut.objects.all().delete()

        # Delete all records from Summary model
        Summary.objects.all().delete()

        self.message_user(request, "DELETE ALL RECORD")

    delete_all_data_action.short_description = "Delete all records"

    def update_summary_action(self, request, queryset):
    # Group queryset by date
     grouped_by_date = defaultdict(list)
     for obj in queryset:
        grouped_by_date[obj.date].append(obj)

    # Update or create Summary record for each unique date
     for date, objects_with_same_date in grouped_by_date.items():
        # Collect cash_in values for the objects with the same date
        cash_in_values = [obj.cash_in for obj in objects_with_same_date]

        # Calculate the sum for cash_in and actual_cash_in
        total_cash_in = sum(cash_in_values)
        total_actual_cash_in = sum(obj.cash_in if obj.status == 'Received' else 0 for obj in objects_with_same_date)

        # Update or create Summary record for the specified date
        summary, _ = Summary.objects.update_or_create(
            date=date,
            defaults={
                'cash_in': total_cash_in,
                'actual_cash_in': total_actual_cash_in,
                # Add other fields as needed
            }
        )

     self.message_user(request, f"Summary updated for {len(grouped_by_date)} unique dates.")



    def update_summary(self, obj):
        summary, _ = Summary.objects.get_or_create(date=obj.date)
        cash_in_delta = obj.cash_in
        summary.cash_in += cash_in_delta
        summary.actual_cash_in += cash_in_delta if obj.status == 'Received' else 0
        summary.save()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.update_summary(obj)
    update_summary_action.short_description = "Update summary"

    def delete_model(self, request, obj):
        # Delete corresponding data from Summary
        summary = Summary.objects.filter(date=obj.date).first()
        if summary:
            summary.cash_in -= obj.cash_in
            summary.actual_cash_in -= obj.cash_in if obj.status == 'Received' else 0
            summary.save()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            summary = Summary.objects.filter(date=obj.date).first()
            if summary:
                summary.cash_in -= obj.cash_in
                summary.actual_cash_in -= obj.cash_in if obj.status == 'Received' else 0
                summary.save()
        queryset.delete()
    def log_user_action(self, request, action_description):
        # Log the user action
        UserActionLog.objects.create(
            user=request.user,
            action_description=action_description,
        )

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        self.log_user_action(request, f"Deleted UpdateCashIn - {obj.date} - {obj.income_source} - {obj.cash_in}")

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        self.log_user_action(request, "Deleted queryset in UpdateCashIn")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.log_user_action(request, f"Saved UpdateCashIn - {obj.date} - {obj.income_source} - {obj.cash_in}")

    def import_action(self, request, *args, **kwargs):
        result = super().import_action(request, *args, **kwargs)
        self.log_user_action(request, f"Imported data in UpdateCashIn")
        return result

    def export_action(self, request, *args, **kwargs):
        result = super().export_action(request, *args, **kwargs)
        self.log_user_action(request, f"Exported data in UpdateCashIn")
        return result
    
    
class UpdateCashOutResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id', widget=widgets.IntegerWidget())

    expense_source = fields.Field(
        column_name='Expense Source',
        attribute='expense_source',
        widget=widgets.CharWidget()  # Use CharWidget instead of ForeignKeyWidget
    )


    class Meta:
        model = UpdateCashOut
        fields = ('id', 'date', 'expense_source', 'project','cost_center','cash_out', 'status', 'remark')
        export_order = fields  # Include 'id' in the fields for import
    def before_import_row(self, row, **kwargs):
        # Disable date validation to allow importing all data
        pass
class UpdateCashOutAdminForm(forms.ModelForm):
    class Meta:
        model = UpdateCashOut
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Check if it's a new record (not being edited)
            self.fields['processed'].initial = True  # Set processed checkbox to True by default
            self.fields['processed'].widget = forms.HiddenInput() 



class UpdateCashOutAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_class = UpdateCashOutResource
    list_display = ['date', 'expense_source','project', 'cost_center', 'cash_out', 'status', 'remark',  'formatted_priority']
    search_fields = ['expense_source', 'date', 'project', 'cost_center']
    list_filter = ['date','status', 'priority_level', 'cost_center']
    ordering = ['-date']
    form = UpdateCashOutAdminForm

    def formatted_priority(self, obj):
        priority_color = {
            'urgent': 'red',
            'important': 'orange',
            'normal': 'blue',
        }
        font_color = priority_color.get(obj.priority_level, 'black')
        formatted_priority = obj.priority_level.capitalize()
        return format_html("<span style='color: {};'>{}</span>", font_color, formatted_priority)
    
    formatted_priority.short_description = 'Priority Level'
    
    actions = ['update_summary_action','delete_all_data_action']
    def delete_all_data_action(self, request, queryset):
        # Delete all records from UpdateCashIn model
        UpdateCashOut.objects.all().delete()

        # Delete all records from UpdateCashOut model
        UpdateCashIn.objects.all().delete()

        # Delete all records from Summary model
        Summary.objects.all().delete()

        self.message_user(request, "DELETE ALL RECORD")

    delete_all_data_action.short_description = "Delete all records"


    def update_summary_action(self, request, queryset):
        grouped_by_date = defaultdict(list)

        for obj in queryset:
            grouped_by_date[obj.date].append(obj)

        # Update or create Summary record for each unique date
        for date, objects_with_same_date in grouped_by_date.items():
            # Collect cash_out values for the objects with the same date
            cash_out_values = [obj.cash_out for obj in objects_with_same_date]

            # Calculate the sum for cash_out and actual_cash_out
            total_cash_out = sum(cash_out_values)
            total_actual_cash_out = sum(obj.cash_out if obj.status == 'Paid' else 0 for obj in objects_with_same_date)

            # Update or create Summary record for the specified date
            summary, _ = Summary.objects.update_or_create(
                date=date,
                defaults={
                    'cash_out': total_cash_out,
                    'actual_cash_out': total_actual_cash_out,
                    # Add other fields as needed
                }
            )

        self.message_user(request, f"Summary updated for {len(grouped_by_date)} unique dates.")
    

        
    def update_summary(self, obj):
        summary, _ = Summary.objects.get_or_create(date=obj.date)
        cash_out_delta = obj.cash_out
        summary.cash_out += cash_out_delta
        summary.actual_cash_out += cash_out_delta if obj.status == 'Paid' else 0
        summary.save()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.update_summary(obj)
    update_summary_action.short_description = "Update Summary"

    def delete_model(self, request, obj):
        # Delete corresponding data from Summary
        summary = Summary.objects.filter(date=obj.date).first()
        if summary:
            summary.cash_out -= obj.cash_out
            summary.actual_cash_out-= obj.cash_out if obj.status == 'Paid' else 0
            summary.save()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            summary = Summary.objects.filter(date=obj.date).first()
            if summary:
                summary.cash_out -= obj.cash_out
                summary.actual_cash_out -= obj.cash_out if obj.status == 'Paid' else 0
                summary.save()
        queryset.delete()
    def log_user_action(self, request, action_description):
        # Log the user action
        UserActionLog.objects.create(
            user=request.user,
            action_description=action_description,
        )

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        self.log_user_action(request, f"Deleted UpdateCashOut - {obj.date} - {obj.expense_source} - {obj.cash_out}")

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        self.log_user_action(request, "Deleted queryset in UpdateCashOut")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.log_user_action(request, f"Saved UpdateCashOut - {obj.date} - {obj.expense_source} - {obj.cash_out}")

    def import_action(self, request, *args, **kwargs):
        result = super().import_action(request, *args, **kwargs)
        self.log_user_action(request, f"Imported data in UpdateCashOut")
        return result

    def export_action(self, request, *args, **kwargs):
        result = super().export_action(request, *args, **kwargs)
        self.log_user_action(request, f"Exported data in UpdateCashOut")
        return result
    
    
    

class AvailableBalanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount')
    search_fields = ['date']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update the corresponding Summary model
        summary, created = Summary.objects.get_or_create(date=obj.date)
        summary.actual_balance = obj.amount 
        summary.planned_balance = obj.amount
        
        summary.save()
        # Log the user action
        UserActionLog.objects.create(
            user=request.user,
            action_description=f"Updated AvailableBalance - {obj.date} - {obj.amount}",
        )

        
        
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('total_cash_in', 'total_cash_out', 'total_actual_cash_in', 'total_actual_cash_out', 'current_balance')
    readonly_fields = ('total_cash_in', 'total_cash_out', 'total_actual_cash_in', 'total_actual_cash_out', 'current_balance')

    def has_add_permission(self, request):
        return False  # Disable the ability to add new Dashboard records

    def has_change_permission(self, request, obj=None):
        return False  # Disable the ability to change existing Dashboard records

    def has_delete_permission(self, request, obj=None):
        return False  # Disable the ability to delete existing Dashboard records

    def get_queryset(self, request):
        # Calculate the total values for the dashboard
        total_cash_in = Summary.objects.aggregate(models.Sum('cash_in'))['cash_in__sum'] or 0
        total_cash_out = Summary.objects.aggregate(models.Sum('cash_out'))['cash_out__sum'] or 0
        total_actual_cash_in = Summary.objects.aggregate(models.Sum('actual_cash_in'))['actual_cash_in__sum'] or 0
        total_actual_cash_out = Summary.objects.aggregate(models.Sum('actual_cash_out'))['actual_cash_out__sum'] or 0

        # Create or update a single Dashboard record with the calculated totals
        dashboard, created = Dashboard.objects.get_or_create(pk=1)
        dashboard.total_cash_in = total_cash_in
        dashboard.total_cash_out = total_cash_out
        dashboard.total_actual_cash_in = total_actual_cash_in
        dashboard.total_actual_cash_out = total_actual_cash_out

        # Calculate and update the current balance
        dashboard.current_balance = total_actual_cash_in - total_actual_cash_out

        dashboard.save()

        # Return a queryset with only the calculated Dashboard record
        return Dashboard.objects.filter(pk=1)
    
    

class SummaryResource(resources.ModelResource):
    class Meta:
        model = Summary
        exclude = ('id',)  # Exclude the 'id' column from the export
class SummaryAdminForm(forms.ModelForm):
    class Meta:
        model = Summary
        exclude = []  # Include all fields from the model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all fields as read-only
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['readonly'] = True
            self.fields[field_name].widget.attrs['style'] = 'background-color: #f2f2f2;'  # Optional: Apply a different background color

class SummaryAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_class = SummaryResource
    list_display = ('date', 'cash_in', 'cash_out', 'actual_cash_in', 'actual_cash_out', 'actual_balance', 'planned_balance')
    search_fields = ['date']
    ordering = ['-date']
    form = SummaryAdminForm


    actions = ['update_balance_action', 'delete_all_data_action', 'delete_blank_rows_action', 'generate_transaction_details','show_transaction_history']
    def has_add_permission(self, request):
        # Disable the ability to add new Summary records
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the ability to change existing Summary records
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable the ability to delete existing Summary records
        return False
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/view-details/',
                 self.admin_site.admin_view(self.view_transaction_details),
                 name='summary-view-details'),
        ]
        return custom_urls + urls

    def view_transaction_details(self, request, object_id, *args, **kwargs):
        # Fetch and prepare details from UpdateCashIn and UpdateCashOut tables
        selected_date = Summary.objects.get(pk=object_id).date
        cash_in_details = UpdateCashIn.objects.filter(date=selected_date)
        cash_out_details = UpdateCashOut.objects.filter(date=selected_date)

        # Render the details as HTML
        details_html = render_to_string('admin/cashflow/summary/transaction_details_table.html', {
            'selected_date': selected_date,
            'cash_in_details': cash_in_details,
            'cash_out_details': cash_out_details,
        })

        # Return HTML response
        return HttpResponse(details_html)
    change_list_template = 'admin/cashflow/summary/change_list.html'

    def changelist_view(self, request, extra_context=None):
        # Fetch aggregated data from Summary
        aggregated_data = Summary.objects.aggregate(
            total_cash_in=Sum('cash_in'),
            total_cash_out=Sum('cash_out'),
            total_actual_cash_in=Sum('actual_cash_in'),
            total_actual_cash_out=Sum('actual_cash_out'),
            current_balance=Sum('actual_cash_in') - Sum('actual_cash_out'),
        )

        extra_context = extra_context or {}
        extra_context.update(aggregated_data)

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if "_viewdetails" in request.POST:
            return HttpResponseRedirect(reverse('admin:summary-view-details', args=[object_id]))
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        extra_context = {'show_viewdetails': True}
        return super().render_change_form(request, context, add, change, form_url, obj, extra_context=extra_context)
    def generate_transaction_details(self, request, queryset):
        if queryset.count() == 1:
            selected_date = queryset[0].date

            # Fetch and prepare details from UpdateCashIn and UpdateCashOut tables
            cash_in_details = UpdateCashIn.objects.filter(date=selected_date)
            cash_out_details = UpdateCashOut.objects.filter(date=selected_date)

            # Render the details as HTML
            details_html = render_to_string('admin/cashflow/summary/transaction_details_table.html', {
                'selected_date': selected_date,
                'cash_in_details': cash_in_details,
                'cash_out_details': cash_out_details,
            })

            # Return HTML response
            return HttpResponse(details_html)

        self.message_user(request, "Please select exactly one date to generate transaction details.")

    generate_transaction_details.short_description = "Generate transaction details"
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        # Fetch and prepare details from UpdateCashIn and UpdateCashOut tables
        selected_date = Summary.objects.get(pk=object_id).date
        cash_in_details = UpdateCashIn.objects.filter(date=selected_date)
        cash_out_details = UpdateCashOut.objects.filter(date=selected_date)

        # Add the transaction details to the extra_context
        extra_context['show_transaction_details'] = True
        extra_context['transaction_details'] = {
            'selected_date': selected_date,
            'cash_in_details': cash_in_details,
            'cash_out_details': cash_out_details,
        }

        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        extra_context = context.copy()

        # Get the transaction details from the extra_context
        transaction_details = extra_context.get('transaction_details', None)

        if transaction_details:
            # Render the transaction details table
            transaction_details_html = render_to_string('admin/cashflow/summary/transaction_details_table.html', transaction_details)
            extra_context['transaction_details_html'] = transaction_details_html

        return super().render_change_form(request, extra_context, add, change, form_url, obj)
    def delete_blank_rows_action(self, request, queryset):
        # Filter out and delete blank rows in Summary model
        blank_rows = queryset.filter(
            cash_in=0,
            cash_out=0,
            actual_cash_in=0,
            actual_cash_out=0,
        )
        blank_rows.delete()

        self.message_user(request, f"{blank_rows.count()} blank rows deleted from Summary.")

    delete_blank_rows_action.short_description = "Delete blank rows in summary"
    def delete_all_data_action(self, request, queryset):
        # Delete all records from UpdateCashIn model
        UpdateCashIn.objects.all().delete()

        # Delete all records from UpdateCashOut model
        UpdateCashOut.objects.all().delete()

        # Delete all records from Summary model
        Summary.objects.all().delete()
        

        self.message_user(request, "DELETE ALL RECORD")

    delete_all_data_action.short_description = "Delete all records"

    def update_balance_action(self, request, queryset):
        for obj in queryset:
            self.update_balance(obj)
        self.message_user(request, f"Balance updated for {queryset.count()} records.")

    update_balance_action.short_description = "Update balance for selected records"

    def update_balance(self, obj):
        # Find the most recent existing row
        previous_summary = Summary.objects.filter(date__lt=obj.date).order_by('-date').first()
        
        if previous_summary:
            obj.actual_balance = (
                previous_summary.actual_balance +
                obj.actual_cash_in -
                obj.actual_cash_out
            )
            obj.planned_balance = (
                previous_summary.planned_balance +
                obj.cash_in -
                obj.cash_out
            )
        obj.save()
        
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # If it's not the first row, update the actual_balance and planned_balance
        if obj.id:
            self.update_balance(obj)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_time', 'action_description']
    search_fields = ['user__username', 'action_description']
    ordering = ['-action_time']
    
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UpdateCashIn, UpdateCashInAdmin)
admin.site.register(UpdateCashOut, UpdateCashOutAdmin)
admin.site.register(AvailableBalance, AvailableBalanceAdmin)
admin.site.register(Summary, SummaryAdmin) 
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(UserActionLog, UserActionLogAdmin)
