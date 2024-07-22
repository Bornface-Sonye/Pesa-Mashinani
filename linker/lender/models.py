from django.db import models
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .validators import validate_kenyan_id, validate_lender_id, validate_kenyan_phone_number


class County(models.Model):
    county_id = models.AutoField(primary_key=True, unique=True)
    county_name = models.CharField(max_length=100, help_text="Enter County Name")

    def __str__(self):
        return self.county_name

class Constituency(models.Model):
    constituency_id = models.AutoField(primary_key=True, unique=True)
    constituency_name = models.CharField(max_length=100, help_text="Enter Constituency Name")
    county = models.ForeignKey(County, on_delete=models.CASCADE, help_text="Choose the County Name")

    def __str__(self):
        return self.constituency_name


class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True, unique=True)
    ward_name = models.CharField(max_length=100, help_text="Enter Ward Name")
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, help_text="Choose the Constituency Name")

    def __str__(self):
        return self.ward_name





class SubLocation(models.Model):
    sublocation_id = models.AutoField(primary_key=True, unique=True)
    sublocation_name = models.CharField(max_length=100, help_text="Enter Sub Location Name")
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, help_text="Choose the Ward")
    

    def __str__(self):
        return self.sublocation_name


class Company(models.Model):
    company_no = models.CharField(max_length=50, primary_key=True, help_text="Enter Company Number")
    company_name = models.CharField(max_length=100, help_text="Enter Company Name")
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, help_text="Choose the Constituency Name")

    def __str__(self):
        return self.company_name


class Commission(models.Model):
    commission_no = models.CharField(max_length=50, primary_key=True, help_text="Enter Commission Number")
    commission_name = models.CharField(max_length=100, help_text="Enter Commission Name")
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, help_text="Choose the Constituency Name")

    def __str__(self):
        return self.commission_name

class Account(models.Model):
    account_no = models.DecimalField(max_digits=50, decimal_places=0, primary_key=True, help_text="Enter Account Number")
    account_name = models.CharField(max_length=100, help_text="Enter Account Name")
    account_bal = models.DecimalField(max_digits=20, decimal_places=2, help_text="Enter Account Balance")

    def __str__(self):
        return self.account_name

class Borrower(models.Model):
    borrower_id = models.AutoField(primary_key=True, unique=True)
    BORROWER_TYPE_CHOICES = [
        ('entrepreneur', 'Entrepreneur'),
        ('civil_servant', 'Civil Servant'),
        ('employee', 'Employee'),
        ('unemployed', 'Unemployed'),
        ('group', 'Group'),
    ]
    borrower_type = models.CharField(max_length=20, choices=BORROWER_TYPE_CHOICES)
    email_address = models.EmailField(max_length=30, unique=True, help_text="Enter Email Address:")
    national_id = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    borrower_no = models.CharField(max_length=100, help_text="Enter Borrower Number:", blank=True)
    username = models.CharField(max_length=50, help_text="Enter Borrower Username", blank=True)

    def __str__(self):
        return f"{self.username}"


class Lender(models.Model):
    lender_id = models.AutoField(primary_key=True, unique=True)
    LENDER_TYPE_CHOICES = [
        ('bank', 'Bank'),
        ('group', 'Group'),
    ]
    
    lender_type = models.CharField(max_length=20, choices=LENDER_TYPE_CHOICES)
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    lender_id_no = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_lender_id],help_text="Enter Identification Number:")
    lender_no = models.CharField(max_length=100, help_text="Enter Lender Number:", blank=True)
    account_no = models.ForeignKey(Account, on_delete=models.CASCADE, help_text="Choose Account Number")
    username = models.CharField(max_length=50, help_text="Enter Username", blank=True)
    
    def __str__(self):
        return f"{self.username}"


class Entrepreneur(models.Model):
    borrower_no = models.OneToOneField(Borrower, on_delete=models.CASCADE, help_text="Choose Borrower Number")
    entrepreneur_no = models.CharField(max_length=50, help_text="Enter Entrepreneur Number:")
    company_no = models.ForeignKey(Company, on_delete=models.CASCADE, help_text="Choose Company Number")

    def __str__(self):
        return f"{self.borrower_no}"


class CivilServant(models.Model):
    borrower_no = models.OneToOneField(Borrower, on_delete=models.CASCADE, primary_key=True)
    civil_servant_no = models.CharField(max_length=50, help_text="Enter Servant Number")
    commission_no = models.ForeignKey(Commission, on_delete=models.CASCADE, help_text="Choose Commission Number")

    def __str__(self):
        return f"{self.borrower_no}"


class Employee(models.Model):
    borrower_no = models.OneToOneField(Borrower, on_delete=models.CASCADE, primary_key=True)
    employee_no = models.CharField(max_length=50, help_text="Enter Employee Number")
    company_no = models.ForeignKey(Company, on_delete=models.CASCADE, help_text="Choose Company Number")

    def __str__(self):
        return f"{self.borrower_no}"
    
    
class Guarantor(models.Model):
    guarantor_id = models.AutoField(primary_key=True, unique=True)
    national_id = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    guarantor_first_name = models.CharField(max_length=30, help_text="Enter First Name")
    guarantor_last_name = models.CharField(max_length=30, help_text="Enter Last Name")
    phone_number = models.CharField(
        max_length=13,  # Maximum length for +254xxxxxxxxx format
        validators=[validate_kenyan_phone_number],
        help_text="Enter phone number in the format 0798073204 or +254798073404"
    )
    dob = models.DateField(help_text="Enter Date of Birth")
    occupation = models.CharField(max_length=100, help_text="Enter Occupation")
    account_no = models.ForeignKey(Account, on_delete=models.CASCADE, help_text="Choose Account Number")
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, help_text="Choose the Ward")
    
    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    def __str__(self):
        return f"Guarantor - {self.guarantor_no}"



class Unemployed(models.Model):
    borrower_no = models.OneToOneField(Borrower, on_delete=models.CASCADE, primary_key=True)
    guarantor = models.ForeignKey(Guarantor, on_delete=models.CASCADE, help_text="Choose the Guarantor")

    def __str__(self):
        return f"{self.borrower_no}"


class Bank(models.Model):
    lender_no = models.OneToOneField(Lender, on_delete=models.CASCADE, primary_key=True)
    bank_name = models.CharField(max_length=50, unique=True, help_text="Enter Bank Name")
    phone_number = models.CharField(
        max_length=13,  # Maximum length for +254xxxxxxxxx format
        validators=[validate_kenyan_phone_number],
        help_text="Enter phone number in the format 0798073204 or +254798073404"
    )
    bank_no = models.CharField(max_length=50, unique=True, help_text="Enter Bank Number")
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, help_text="Choose the Constituency")
   
    def __str__(self):
        return f"Bank - {self.bank_no}"


class Group(models.Model):
    borrower_no = models.OneToOneField(Borrower, on_delete=models.CASCADE, primary_key=True)
    group_no = models.CharField(max_length=50, unique=True, help_text="Enter Group Number")
    group_name = models.CharField(max_length=100, help_text="Enter Group Name")
    phone_number = models.CharField(
        max_length=13,  # Maximum length for +254xxxxxxxxx format
        validators=[validate_kenyan_phone_number],
        help_text="Enter phone number in the format 0798073204 or +254798073404"
    )
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, help_text="Choose Ward of Operation")
    guarantor = models.ForeignKey(Guarantor, on_delete=models.CASCADE, help_text="Choose the Guarantor")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, help_text="Account Number")

    def __str__(self):
        return self.group_no


class GroupLender(models.Model):
    lender_no = models.OneToOneField(Lender, on_delete=models.CASCADE, primary_key=True)
    group_no = models.ForeignKey(Group, on_delete=models.CASCADE, help_text="Choose the Group")

    def __str__(self):
        return f"{self.group_no}"


class BorrowerGroup(models.Model):
    borrower_group_id = models.AutoField(primary_key=True, unique=True)
    borrower_no = models.ForeignKey(Borrower, on_delete=models.CASCADE, help_text="Choose the Borrower Number")
    group_no = models.ForeignKey(Group, on_delete=models.CASCADE, help_text="Choose the Group Number")

    def __str__(self):
        return f"{self.borrower_no} - {self.group_no}"
    
    
class Message(models.Model):
    message_id = models.AutoField(primary_key=True, unique=True)
    message_no = models.CharField(max_length=50, help_text="Enter Message Number")
    sender_usename = models.CharField(max_length=50, help_text="Enter Sender Username")
    recipient_username = models.CharField(max_length=50, help_text="Enter Recipient Username")
    message_name = models.CharField(max_length=50, help_text="Enter Message Name")
    message_description = models.CharField(max_length=50, help_text="Enter Message Description")
    message_date = models.DateField(help_text="Enter Date Sent")

    def __str__(self):
        return f"{self.message_no}"
    

class GroupMember(models.Model):
    member_id = models.AutoField(primary_key=True, unique=True)
    member_no = models.CharField(max_length=50, help_text="Enter Member Number")
    first_name = models.CharField(max_length=50, help_text="Enter First Name")
    last_name = models.CharField(max_length=50, help_text="Enter Last Name")
    national_id = models.DecimalField(max_digits=20, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    phone_number = models.CharField(
        max_length=13,  # Maximum length for +254xxxxxxxxx format
        validators=[validate_kenyan_phone_number],
        help_text="Enter phone number in the format 0798073204 or +254798073404"
    )
    dob = models.DateField(help_text="Enter Date of Birth")
    
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        help_text="Enter Member Gender"
    )

    group = models.CharField(max_length=50, help_text="Enter Group Number")
    grp_worth = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, help_text="Enter Group Worth in Kshs.")
    account = models.CharField(max_length=50, default='00000000', help_text="Account Number")

    YES = 'yes'
    NO = 'no'
    APPROVAL_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No'),
    ]

    approved = models.CharField(
        max_length=3,
        choices=APPROVAL_CHOICES,
        default=NO,  # Default value can be set to 'no'
        help_text="Is the member approved"

    )

    def __str__(self):
        return f"{self.member_no}"

    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age


class System_User(models.Model):
    borrower_no = models.CharField(max_length=100, help_text="Enter Borrower Number/System-Generated:", blank=True)
    lender_no = models.CharField(max_length=100, help_text="Enter Lender Number/System-Generated:", blank=True)
    username = models.EmailField(unique=True, max_length=50, help_text="Enter a valid Username")
    password_hash = models.CharField(max_length=128, help_text="Enter a valid password")  # Store hashed password

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def clean(self):
        # Custom validation for password field
        if len(self.password_hash) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def __str__(self):
        return self.username


class Allocation(models.Model):
    allocation_id = models.AutoField(primary_key=True, unique=True)
    allocation_no = models.CharField(unique=True, max_length=50, help_text="Enter the Allocation Number", blank=True)
    lender_no = models.CharField(max_length=100, help_text="Enter Lender Number:")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Allocate")
    interest_rate = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Interest Rate")
    allocation_date = models.DateField(help_text="Enter Date of Allocation", blank=True)

    def __str__(self):
        return f"Allocation - {self.allocation_no}"
    
    
    


class Defaulter(models.Model):
    national_id = models.DecimalField(
        max_digits=8,
        decimal_places=0,
        primary_key=True,
        unique=True,
        validators=[validate_kenyan_id],
        help_text="Enter National Identification Number:"
    )
    lender_no = models.CharField(
        max_length=50,
        unique=True,
        help_text="Enter Group Number"
    )
    amount_owed = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Enter Amount Owed"
    )
    submission_date = models.DateField(help_text="Enter Date of Submission", blank=True)

    def __str__(self):
        return str(self.national_id)



class Application(models.Model):
    application_id = models.AutoField(primary_key=True, unique=True)
    application_no = models.CharField(unique=True, max_length=50, help_text="Enter the Application Number", blank=True)
    borrower_no = models.CharField(max_length=100, help_text="Enter Borrower Number:")
    allocation_no = models.CharField(max_length=50, help_text="Enter the Allocation Number")
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Request")
    proposed_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount Proposed")
    application_date = models.DateField(help_text="Enter Date of Application", blank=True)

    def __str__(self):
        return f"Application - {self.application_no}"


class Disbursement(models.Model):
    disbursement_id = models.AutoField(primary_key=True, unique=True)
    transaction_no = models.CharField(unique=True, max_length=30, help_text="Enter the Transaction Number", blank=True)
    application_no = models.CharField(max_length=50, help_text="Enter the Application Number")
    disbursed_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Disburse")
    disbursement_date = models.DateField(help_text="Enter Date of Disbursement")

    def __str__(self):
        return f"Disbursement - {self.transaction_no}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, unique=True)
    payment_no = models.CharField(unique=True, max_length=30, help_text="Enter the Payment Number", blank=True)
    transaction_no = models.CharField(max_length=30, help_text="Enter the Transaction Number")
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Pay")
    payment_date = models.DateField(help_text="Enter Date of Disbursement")

    def __str__(self):
        return f"Payment - {self.payment_no}"
    
    
class Loans(models.Model):
    payment_id = models.AutoField(primary_key=True, unique=True)
    payment_no = models.CharField(unique=True, max_length=30, help_text="Enter the Payment Number", blank=True)
    transaction_no = models.CharField(max_length=30, help_text="Enter the Transaction Number")
    principal = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Pay")
    principal_interest = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total Amount")
    amount_paid =  models.DecimalField(max_digits=15, decimal_places=2, help_text="Total Paid")
    balance =  models.DecimalField(max_digits=15, decimal_places=2, help_text="Balance")

    def __str__(self):
        return f"Loan - {self.transaction_no}"
