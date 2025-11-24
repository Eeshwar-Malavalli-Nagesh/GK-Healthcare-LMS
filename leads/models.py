from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.db.models import Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    followup_date = models.DateField()
    followup_time = models.TimeField()
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class HospitalLead(models.Model):
    # Hospital Information
    hospital_name = models.CharField(max_length=200)
    hospital_type = models.CharField(max_length=50, choices=[
        ('Direct Hospital', 'Direct Hospital'),
        ('Distributed', 'Distributed'),
        ('Other', 'Other'),
    ])
    
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')

    # Telecalling and Decision Data
    telecalling_response = models.JSONField(default=list)
    decision_maker = models.JSONField(default=list)

    # Follow-up Information
    followup_date = models.DateField(null=True, blank=True)
    followup_time = models.TimeField(null=True, blank=True)

    # Communication Preferences
    communication_channel = models.CharField(
        max_length=20,
        choices=[
            ('SMS', 'SMS'),
            ('Email', 'Email'),
            ('WhatsApp', 'WhatsApp'),
            ('Phone', 'Phone')
        ],
        null=True,
        blank=True
    )
    
    promotional_messages = models.CharField(
        max_length=3,
        choices=[('Yes', 'Yes'), ('No', 'No')],
        null=True,
        blank=True
    )
    
    remarks = models.TextField(null=True, blank=True)

    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hospital_name} - {self.first_name} {self.last_name}"
    

class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    

class Product(models.Model):
    PRODUCT_UNITS = [
        ('kg', 'Kilogram'),
        ('ltr', 'Liter'),
        ('pcs', 'Pieces'),
        ('box', 'Box'),
        ('nos', 'Numbers'),
    ]

    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=PRODUCT_UNITS, default='pcs')
    hsn_sac = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    

class PaymentFollowUp(models.Model):
    PAYMENT_MODES = [
        ('Mail Done', 'Mail Done'),
        ('Online Transfer', 'Online Transfer'),
        ('Cheque', 'Cheque'),
        ('Cash', 'Cash'),
        ('DD', 'Demand Draft'),
    ]
    
    PAYMENT_STATUSES = [
        ('Pending', 'Pending'),
        ('Partial', 'Partial Payment'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
    ]
    
    client_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    mode_of_payment = models.CharField(max_length=50, choices=PAYMENT_MODES)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUSES)
    follow_up_date = models.DateField(null=True, blank=True)
    next_follow_date = models.DateField(null=True, blank=True)
    last_payment_date = models.DateField()
    due_days = models.IntegerField()
    present_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.client_name} - {self.amount}"
    
    class Meta:
        verbose_name = "Payment Follow-up"
        verbose_name_plural = "Payment Follow-ups"

class Parts(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    
    # New optional fields
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    parts_image = models.ImageField(upload_to='parts_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Parts"
        verbose_name_plural = "Parts"
        ordering = ['-created_at']


class Customer(models.Model):
    # Company Information
    
    company_name = models.CharField(max_length=200, blank=True, null=True)
    customer_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # New field for customer ID
    
    customer_name = models.CharField(max_length=200)
    
    # Contact Information
    phone_number = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    
    # Address Information
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    # Website
    company_website = models.URLField(blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.company_name or 'Individual'}"
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['-created_at']

class Employee(models.Model):
    POSITION_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('analyst', 'Analyst'),
        ('hr', 'HR'),
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('admin', 'Admin'),
        ('intern', 'Intern'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='employees')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    class Meta:
        ordering = ['-created_at']

# If you don't have a CustomerProduct model, create one:
class CustomerProduct(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilogram'),
        ('ltr', 'Liter'),
        ('box', 'Box'),
        ('nos', 'Numbers'),
        ('mtr', 'Meter'),
        ('sqft', 'Square Feet'),
        ('set', 'Set'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products')
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    product_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, blank=True)
    hsn_sac = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    product_image = models.ImageField(upload_to='customer_products/', blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    installation_date = models.DateField(null=True, blank=True)
    warranty_period_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.product_name} - {self.customer.customer_name}"
    

class Vendor(models.Model):
    vendor_id = models.CharField(max_length=20, unique=True) 
    company_name = models.CharField(max_length=200, blank=True, null=True)
    vendor_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor_name} - {self.company_name or 'No Company'}"

    class Meta:
        ordering = ['-created_at']

class VendorEmployee(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='employees')
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.position} ({self.vendor.vendor_name})"

    class Meta:
        ordering = ['-created_at']

class VendorProduct(models.Model):

    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('meter', 'Meters'),
        ('liter', 'Liters'),
        ('box', 'Box'),
        ('set', 'Set'),
        ('roll', 'Roll'),
        ('packet', 'Packet'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    installation_date = models.DateField(null=True, blank=True)
    warranty_period_date = models.DateField(null=True, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    product_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='pcs')
    hsn_sac = models.CharField(max_length=20)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    product_image = models.ImageField(upload_to='vendor_products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product_name} - {self.vendor.vendor_name}"
    
    def get_product_unit_display(self):
        return dict(self.UNIT_CHOICES).get(self.product_unit, self.product_unit)
    
    class Meta:
        ordering = ['-created_at']

class Project(models.Model):
    project_id = models.CharField(
        max_length=50, 
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text="Enter a unique identifier for this project (e.g., PRJ-001, WEBSITE-2025)"
    )
    project_name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3)],
        help_text="Enter a descriptive name for your project"
    )
    started_date = models.DateField(
        default=timezone.now,
        help_text="Select the project start date"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Is this project currently active?")
    
    class Meta:
        ordering = ['-started_date']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return f"{self.project_id} - {self.project_name}"
    
    @property
    def total_expense_amount(self):
        """Calculate total expenses for this project"""
        total = self.expenses.aggregate(total=Sum('amount'))['total']
        return total if total is not None else 0
    
    @property
    def expense_count(self):
        """Count of expenses for this project"""
        return self.expenses.count()
    
    def total_expenses(self):
        """Calculate total expenses - method for backward compatibility"""
        return self.total_expense_amount
    
    @property
    def paid_expenses(self):
        """Calculate paid expenses"""
        paid = self.expenses.filter(status='paid').aggregate(total=Sum('amount'))['total']
        return paid if paid is not None else 0
    
    @property
    def pending_expenses(self):
        """Calculate pending expenses"""
        pending = self.expenses.filter(status='pending').aggregate(total=Sum('amount'))['total']
        return pending if pending is not None else 0


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Expense Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_TYPES = [
        ('UPI', 'UPI'),
        ('Net Banking', 'Net Banking'),
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Cheque', 'Cheque'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    expense_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.CharField(max_length=200, blank=True)
    employee_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    notes = models.TextField(blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='UPI')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-expense_date', '-created_at']
    
    def __str__(self):
        return f"{self.expense_number} - {self.description[:50]}"
    
    def save(self, *args, **kwargs):
        if not self.expense_number:
            # Generate expense number like EXP-1, EXP-2, etc.
            last_expense = Expense.objects.order_by('-id').first()
            if last_expense:
                last_num = int(last_expense.expense_number.split('-')[1])
                self.expense_number = f"EXP-{last_num + 1}"
            else:
                self.expense_number = "EXP-1"
        
        # Update status based on is_paid
        if self.is_paid:
            self.status = 'paid'
        elif self.status == 'paid' and not self.is_paid:
            self.status = 'pending'
            
        super().save(*args, **kwargs)


class HospitalLeadParts(models.Model):
    """Model to store parts selected for each hospital lead"""
    hospital_lead = models.ForeignKey(HospitalLead, on_delete=models.CASCADE, related_name='lead_parts')
    part = models.ForeignKey(Parts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('hospital_lead', 'part')  # Prevent duplicate parts for same lead
        verbose_name = "Hospital Lead Part"
        verbose_name_plural = "Hospital Lead Parts"
    
    def __str__(self):
        return f"{self.hospital_lead.hospital_name} - {self.part.name}"


# Also add a similar model for HospitalLeadProducts if you want to store product selections
class HospitalLeadProducts(models.Model):
    """Model to store products selected for each hospital lead"""
    hospital_lead = models.ForeignKey(HospitalLead, on_delete=models.CASCADE, related_name='lead_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('hospital_lead', 'product')  # Prevent duplicate products for same lead
        verbose_name = "Hospital Lead Product"
        verbose_name_plural = "Hospital Lead Products"
    
    def __str__(self):
        return f"{self.hospital_lead.hospital_name} - {self.product.name}"

#quotation

class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class TaxType(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Quotation(models.Model):
    PAYMENT_CHOICES = [
        ('10_advance', '10% Advance'),
        ('20_advance', '20% Advance'),
        ('30_advance', '30% Advance'),
        ('40_advance', '40% Advance'),
        ('50_advance', '50% Advance'),
        ('full_advance', '100% Advance'),
        ('on_delivery', 'On Delivery'),
        ('30_days', '30 Days Credit'),
        ('60_days', '60 Days Credit'),
        ('90_days', '90 Days Credit'),
    ]
    
    DELIVERY_CHOICES = [
        ('immediate', 'Immediate'),
        ('7_days', '7 Days'),
        ('15_days', '15 Days'),
        ('30_days', '30 Days'),
        ('45_days', '45 Days'),
        ('60_days', '60 Days'),
        ('custom', 'Custom'),
    ]
    
    FREIGHT_CHOICES = [
        ('included', 'Included'),
        ('excluded', 'Excluded'),
        ('fob', 'FOB'),
        ('cif', 'CIF'),
    ]
    
    VALIDITY_CHOICES = [
        ('7_days', '7 Days'),
        ('15_days', '15 Days'),
        ('30_days', '30 Days'),
        ('45_days', '45 Days'),
        ('60_days', '60 Days'),
        ('90_days', '90 Days'),
    ]
    
    WARRANTY_CHOICES = [
        ('no_warranty', 'No Warranty'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('5_years', '5 Years'),
        ('lifetime', 'Lifetime'),
    ]
    
    # Basic Information
    quotation_number = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_name=models.CharField(max_length=30,null=True,blank=True)
    
    # Product Details
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    # Terms & Conditions
    payment_terms = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='40_advance')
    delivery_terms = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='15_days')
    freight_charges = models.CharField(max_length=20, choices=FREIGHT_CHOICES, default='excluded')
    validity_period = models.CharField(max_length=20, choices=VALIDITY_CHOICES, default='30_days')
    warranty_period = models.CharField(max_length=20, choices=WARRANTY_CHOICES, default='2_years')
    
    # Bank Details
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)
    tax_type = models.ForeignKey(TaxType, on_delete=models.CASCADE, null=True, blank=True)
    
    # Financial Details
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Additional Fields
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.quotation_number
    
    def calculate_totals(self):
        """Calculate subtotal, tax and total amounts"""
        items_total = sum(item.total_price for item in self.items.all())
        self.subtotal = items_total
        
        if self.tax_type:
            self.tax_amount = (items_total * self.tax_type.percentage) / 100
        else:
            self.tax_amount = 0
            
        self.total_amount = self.subtotal + self.tax_amount
        self.save()
    
    def get_payment_terms_display_custom(self):
        """Custom display for payment terms"""
        return dict(self.PAYMENT_CHOICES).get(self.payment_terms, self.payment_terms)

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Recalculate quotation totals
        self.quotation.calculate_totals()
    
    def __str__(self):
        return f"{self.item_name} - {self.quotation.quotation_number}"