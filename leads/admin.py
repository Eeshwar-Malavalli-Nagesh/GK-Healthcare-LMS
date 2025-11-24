from django.contrib import admin
from .models import HospitalLead
from .models import Category
from .models import Product
from .models import Parts
from .models import Customer
from .models import Employee
from .models import Vendor
from .models import Project
from .models import Expense
from .models import Bank
from .models import TaxType

admin.site.register(HospitalLead)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Parts)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Vendor)
admin.site.register(Project)
admin.site.register(Expense)
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['is_active']

@admin.register(TaxType)
class TaxTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'is_active', 'formatted_percentage')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    ordering = ('name',)
    
    def formatted_percentage(self, obj):
        return f"{obj.percentage}%"
    formatted_percentage.short_description = 'Tax Rate'