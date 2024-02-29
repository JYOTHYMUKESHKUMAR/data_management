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
from .models import Category, Product






    
admin.site.register(Category)
admin.site.register(Product)
