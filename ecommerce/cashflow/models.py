from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from datetime import timedelta
from django.contrib.auth.models import User




class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    def get_url(self):
        return reverse('cashflow:Products_by_categories', args=[self.slug])
class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    image = models.ImageField(upload_to='product', blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    def get_url(self):
        return reverse('cashflow:productdetails',args=[self.category.slug,self.slug])


class UpdateCashIn(models.Model):
    income_source = models.CharField(max_length=250)
    date = models.DateField()  # Remove unique=True
    status = models.CharField(max_length=50, default='update', choices=[('Received', 'Received'), ('Scheduled', 'Scheduled')])
    remark = models.TextField(blank=True)
    cash_in = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    processed = models.BooleanField(default=False)
    project = models.CharField(max_length=250,default='')  # New field for projects
    cost_center = models.CharField(max_length=50, default='update',choices=[
    ('catalyst', 'Catalyst'),
    ('oil_and_gas', 'Oil and Gas'),
    ('general_chemicals', 'General Chemicals'),
    ('overhead', 'Overhead'),
   
]
)  
    # New field for division

    def save(self, *args, **kwargs):
        # If the provided remark is None, set it to an empty string
        if self.remark is None:
            self.remark = ''
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Update Cash In -  {self.date}"


class UpdateCashOut(models.Model):
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('important', 'Important'),
        ('normal', 'Normal'),
    ]

    expense_source = models.CharField(max_length=250)
    date = models.DateField()
    status = models.CharField(max_length=50, default='update', choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    remark = models.TextField(blank=True)
    cash_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    processed = models.BooleanField(default=False)
    priority_level = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    project = models.CharField(max_length=250,default='')  # New field for projects
    cost_center = models.CharField(max_length=50, default='update',choices=[
    ('catalyst', 'Catalyst'),
    ('oil_and_gas', 'Oil and Gas'),
    ('general_chemicals', 'General Chemicals'),
    ('overhead', 'Overhead'),
   
]
)  

    

    def save(self, *args, **kwargs):
        if self.remark is None:
            self.remark = ''
        super().save(*args, **kwargs)

    def __str__(self):
        priority_color = {
            'urgent': 'red',
            'important': 'orange',
            'normal': 'blue',
        }
        font_color = priority_color.get(self.priority_level, 'black')
        formatted_priority = self.priority_level.capitalize()
        return f"<span style='color: {font_color};'>{formatted_priority} - {self.date}</span>"
class Dashboard(models.Model):
    total_cash_in = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cash_out = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_actual_cash_in = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_actual_cash_out = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboard"
        
class AvailableBalance(models.Model):
    date = models.DateField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Available Balance for {self.date}'



class Summary(models.Model):
    date = models.DateField(unique=True)
    cash_in = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_out = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cash_in = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cash_out = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    planned_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    


    def __str__(self):

        return f'Summary for {self.date}'

class UserActionLog(models.Model):
    user = models.ForeignKey(User, related_name='cashflow_user_action_logs', on_delete=models.CASCADE)
    action_time = models.DateTimeField(auto_now_add=True)
    action_description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.action_time} - {self.action_description}"