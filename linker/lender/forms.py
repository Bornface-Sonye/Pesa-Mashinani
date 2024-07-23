from django import forms
import re
from django.contrib.auth.models import User
from .models import (
    Constituency, Ward, SubLocation, Borrower, Entrepreneur,Company, Commission,
    CivilServant, Employee, Unemployed, Group, BorrowerGroup, Lender, Bank, GroupLender, Allocation, System_User,
    Application, Disbursement, Payment, Guarantor, County, Account, GroupMember, Message, Defaulter, Loan
)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class BorrowerForm(forms.ModelForm):
    
    class Meta:
        model = Borrower
        fields = ['borrower_type', 'national_id', 'email_address']
        labels = {
            'national_id': 'National Identification Number',
            'email_address': 'Email Address',
            
        }
        widgets = {
            'national_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter National Identification Number'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),           
           
        }
        
        
   
class EntrepreneurForm(forms.ModelForm):
    company_no = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=True,
        label='Company Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    borrower_no = forms.ModelChoiceField(
        queryset=Borrower.objects.all(),
        required=True,
        label='Borrower Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    class Meta:
        model = Entrepreneur
        fields = ['borrower_no', 'entrepreneur_no',  'company_no']
        labels = {
            'entrepreneur_no': 'Entrepreneur Number',
        }
        
        widgets = {
            'entrepreneur_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Entrepreneur Number'}),
            
        }
        
    
class CivilServantForm(forms.ModelForm):
    
    commission_no = forms.ModelChoiceField(
        queryset=Commission.objects.all(),
        required=True,
        label='Commission Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    borrower_no = forms.ModelChoiceField(
        queryset=Borrower.objects.all(),
        required=True,
        label='Borrower Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    class Meta:
        model = CivilServant
        fields = ['borrower_no', 'civil_servant_no',  'commission_no']
        labels = {
            'civil_servant_no': 'Civil Servant Number',
        }
        
        widgets = {
            'civil_servant_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Civil Servant Number'}),
           
        }

class EmployeeForm(forms.ModelForm):
    
    
    company_no = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=True,
        label='Company Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    borrower_no = forms.ModelChoiceField(
        queryset=Borrower.objects.all(),
        required=True,
        label='Borrower Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    class Meta:
        model = Employee
        fields = ['borrower_no', 'employee_no',  'company_no']
        labels = {
            'employee_no': 'Civil Servant Number',
        }
        
        widgets = {
            'employee_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Employee Number'}),
            
           
        }

class UnemployedForm(forms.ModelForm):
    
    borrower_no = forms.ModelChoiceField(
        queryset=Borrower.objects.all(),
        required=True,
        label='Borrower Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    guarantor = forms.ModelChoiceField(
        queryset=Guarantor.objects.all(),
        required=True,
        label='Guarantor Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    class Meta:
        model = Unemployed
        fields = ['borrower_no', 'guarantor']



class GroupMemberForm(forms.ModelForm):
    class Meta:
        model = GroupMember
        exclude = ['member_no', 'group']  # Exclude fields you handle manually
        labels = {
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'national_id': 'National Identification Number:',
            'phone_number': 'Phone Number:',
            'dob': 'Date Of Birth:',
            'gender': 'Gender:',
            'grp_worth': 'Worth in Kshs:',
            'account': 'Account Number',
            'approved': 'Member approved for Loan ?',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'national_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter National Identification Number'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Date Of Birth'}),
            'gender': forms.RadioSelect(choices=GroupMember.GENDER_CHOICES),
            'grp_worth': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Worth in Kshs'}),
            'account': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account Number'}),
            'approved': forms.Select(attrs={'class': 'form-control'}),
        }






class GroupForm(forms.ModelForm):
    
    borrower_no = forms.ModelChoiceField(
        queryset=Borrower.objects.all(),
        required=True,
        label='Borrower Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.all(),
        required=True,
        label='Ward',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    guarantor = forms.ModelChoiceField(
        queryset=Guarantor.objects.all(),
        required=True,
        label='Guarantor Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=True,
        label='Account Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    class Meta:
        model = Group
        fields = ['borrower_no', 'group_no', 'group_name', 'phone_number', 'ward', 'guarantor', 'account']
        labels = {
            'group_no': 'Group Number',
            'group_name': 'Group Name',
            'phone_number': 'Phone Number',
        }
        
        widgets = {
            'group_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Group Number'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Group Name'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
        }

class BorrowerGroupForm(forms.ModelForm):
    
    class Meta:
        model = BorrowerGroup
        fields = ['borrower_no', 'group_no']
        labels = {
            'borrower_no': 'Group Number',
            'group_no': 'Group Name',
        }
        
        widgets = {
            'borrower_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Borrower Number'}),
            'group_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Group Number'}),
               
        }

class LenderForm(forms.ModelForm):
    
    account_no = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=True,
        label='Account Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    class Meta:
        model = Lender
        fields = ['lender_type', 'email_address', 'lender_id_no', 'account_no']
        labels = {
            'email_address': 'Email Address',
            'lender_id_no': 'Identification Number',
        }
        widgets = {
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'lender_id_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Identification Identification Number'}),   
        }
        

class BankForm(forms.ModelForm):
    
    constituency = forms.ModelChoiceField(
        queryset = Constituency.objects.all(),
        required = True,
        label = 'Constituency',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    lender_no = forms.ModelChoiceField(
        queryset=Lender.objects.all(),
        required=True,
        label='Lender Number',
       widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
      
    class Meta:
        model = Bank
        fields = ['lender_no','bank_no', 'bank_name', 'phone_number', 'constituency']
        labels = {
            'bank_no': 'Bank Number',
            'bank_name': 'Bank Name',
            'phone_number': 'Phone Number',
        }
        widgets = {
            'bank_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Number'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Name'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}), 
        }

class GroupLenderForm(forms.ModelForm):
    
    lender_no = forms.ModelChoiceField(
        queryset=Lender.objects.all(),
        required=True,
        label='Lender Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    group_no = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label='Group Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    
    class Meta:
        model = GroupLender
        fields = ['lender_no','group_no']      
        
        
class GroupSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        fields = ['borrower_no', 'lender_no', 'username', 'password_hash']
        labels = {
            'borrower_no': 'Borrower Number',
            'lender_no': 'Lender Number',
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'borrower_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Borrower Number'}),
            'lender_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Lender Number'}),
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg kcbgroup@lender.co.ke'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance


class BorrowerSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        fields = ['borrower_no', 'username', 'password_hash']
        labels = {
            'borrower_no': 'Borrower Number',
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'borrower_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Borrower Number'}),
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg kcbgroup@lender.co.ke'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance



class BankSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        fields = ['lender_no', 'username', 'password_hash']
        labels = {
            'lender_no': 'Lender Number',
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'lender_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Lender Number'}),
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg kcbgroup@lender.co.ke'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    username = forms.EmailField(
        label="Username",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username:'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password:'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        return cleaned_data
    

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        exclude = ['allocation_no', 'lender_no']
        fields = ['allocation_no', 'lender_no', 'amount', 'interest_rate', 'allocation_date']
        labels = {
            'amount': 'Amount to Allocate',
            'interest_rate': 'Interest Rate'
        }
        widgets = {
            'lender_no': forms.HiddenInput(),  # Hide lender_no field
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount to Allocate'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Interest Rate/per Month'}),
        }

class DisbursementForm(forms.ModelForm):
     class Meta:
        model = Disbursement
        fields = ['disbursed_amount']
        labels = {
            'disbursed_amount': 'Amount to Disburse',
        }
        widgets = {
            'disbursed_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount to Disburse'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['borrower_no']
        fields = ['borrower_no', 'loan_amount']
        labels = {
            'loan_amount': 'Loan Amount',
        }
        widgets = {
            'borrower_no': forms.HiddenInput(),  # Hide borrower_no field
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Loan Amount'}),
        }



              
class PaymentForm(forms.ModelForm):
     class Meta:
        model = Payment
        fields = ['payment_amount']
        labels = {
            'payment_amount': 'Amount ',
        }
        widgets = {
            'payment_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
        }
        

class DefaulterForm(forms.ModelForm):
    class Meta:
        model = Defaulter
        exclude = ['lender_no']  # Exclude fields you handle manually
        fields = ['national_id', 'lender_no', 'amount_owed']
        widgets = {
            'submission_date': forms.HiddenInput(),
        }




class DefaulterUpdateForm(forms.ModelForm):
    class Meta:
        model = Defaulter
        fields = ['amount_owed']
