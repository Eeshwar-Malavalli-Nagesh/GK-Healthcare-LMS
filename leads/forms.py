from django import forms
from .models import Lead
from django.utils import timezone
from .models import Project, Expense, ExpenseCategory
from django.utils import timezone


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets = {
            'followup_date': forms.DateInput(attrs={'type': 'date'}),
            'followup_time': forms.TimeInput(attrs={'type': 'time'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
        

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'amount', 'expense_date', 'category', 'vendor', 'employee_name', 
            'description', 'notes', 'payment_type', 'is_paid'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'step': '0.01',
                'min': '0'
            }),
            'expense_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vendor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vendor name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter expense description'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes (optional)'
            }),
            'payment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_paid': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default expense_date to today if not set
        if not self.instance.pk:
            self.fields['expense_date'].initial = timezone.now().date()
        # Optional: add empty option for category
        self.fields['category'].empty_label = "Select Category"

from django import forms
from django.utils import timezone
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'started_date']
        widgets = {
            'project_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Project ID (e.g., PRJ-001)'
            }),
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Project Name'
            }),
            'started_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default started_date to today if creating a new Project
        if not self.instance.pk:
            self.fields['started_date'].initial = timezone.now().date()
            
class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter category description (optional)'
            }),
        }

#quotation form

from .models import Quotation, QuotationItem, Category, Bank, TaxType
from django.forms import inlineformset_factory

class QuotationForm(forms.ModelForm):
    quotation_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'dd/mm/yyyy'
        }),
        input_formats=['%d/%m/%Y', '%Y-%m-%d']  # Accept both formats
    )
    
    customer_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter customer name'
        })
    )
    class Meta:
        model = Quotation
        fields = [
            'quotation_number','customer_name', 'category', 'payment_terms', 'delivery_terms',
            'freight_charges', 'validity_period', 'warranty_period', 'bank', 'tax_type', 'notes'
        ]
        widgets = {
            'quotation_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., GK/NCP/2025/001'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control form-select',
                'data-placeholder': 'Select a category'
            }),
            'payment_terms': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'delivery_terms': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'freight_charges': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'validity_period': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'warranty_period': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'bank': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'tax_type': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes or terms...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty labels for better UX
        self.fields['category'].empty_label = "Select a category"
        self.fields['bank'].empty_label = "Select bank for payment"
        self.fields['tax_type'].empty_label = "Select tax type"
        
        # Make certain fields required
        self.fields['quotation_number'].required = True
        self.fields['payment_terms'].required = True
        self.fields['delivery_terms'].required = True
class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItem
        fields = ['item_name', 'description', 'quantity', 'unit_price']
        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Item description'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control quantity-input',
                'min': '0.01',
                'step': '0.01',
                'placeholder': '1.00'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control price-input',
                'min': '0.01',
                'step': '0.01',
                'placeholder': '0.00'
            })
        }

# Formset for handling multiple quotation items
QuotationItemFormSet = inlineformset_factory(
    Quotation,
    QuotationItem,
    form=QuotationItemForm,
    extra=1,  # Number of empty forms to display
    min_num=1,  # Minimum number of forms required
    validate_min=True,
    can_delete=True
)

class QuotationSearchForm(forms.Form):
    quotation_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by quotation number...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    payment_terms = forms.ChoiceField(
        choices=[('', 'All Payment Terms')] + Quotation.PAYMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )