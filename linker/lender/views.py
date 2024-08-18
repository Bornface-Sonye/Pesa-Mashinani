from .utils import *

from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView

from django import forms
from django.db import models
from django.db.models import Sum
from decimal import Decimal


from django.views.generic.edit import FormView
from django.utils import timezone


from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from django.db import models
from django.db.models import DecimalField
from django.core.exceptions import ValidationError
from django.db.models import Sum
import string
import random
from datetime import datetime
import time
import hashlib
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

from django.contrib.auth import logout as django_logout
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.urls import reverse

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from .models import (
    Constituency, Ward, SubLocation, Borrower, Entrepreneur,Company, Commission,
    CivilServant, Employee, Unemployed, Group, BorrowerGroup, Lender, Bank, GroupLender, Allocation, System_User,
    Application, Disbursement, Payment, Guarantor, County, Account, GroupMember, Message, Defaulter, Loan, Loanee
)


from .forms import BorrowerForm, EntrepreneurForm, CivilServantForm, EmployeeForm, UnemployedForm, GroupForm
from .forms import AllocationForm, PaymentForm, ApplicationForm, DisbursementForm, GroupMemberForm, GuarantorForm
from .forms import LenderForm, BankForm, GroupLenderForm, BorrowerSignUpForm, BankSignUpForm, PesaSignUpForm, GroupMemmberShipForm
from .forms import GroupSignUpForm, LoginForm, BorrowerGroupForm, UserForm, DefaulterForm,  DefaulterUpdateForm, PaymentForm


class HelpPageView(TemplateView):
    template_name = 'help_page.html'  # Specify your template name here


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        django_logout(request)
        return redirect('home')  # Redirect to home page after logout


class HomePage_View(View):
    def get(self,request):
        return render(request, 'index.html')


    
class TemplateView(View):
    def get(self,request):
        return render(request, 'success.html')  
    
    

# views.py
from django.views.generic import TemplateView

class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username', 'default_value')  # Safely access username
        return context

    

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register_user.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)




class BorrowerCreateView(View):
    template_name = 'register_borrower.html'

    def get(self, request):
        form = BorrowerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BorrowerForm(request.POST)
        
        if form.is_valid():
            email_address = form.cleaned_data['email_address'].lower()
            username = generate_borrower_username(email_address)
            national_id_no = form.cleaned_data['national_id']
            borrower_no = generate_unique_borrower_number(national_id_no, email_address)
            borrower_type = form.cleaned_data['borrower_type']
            
            # Check if the national_id_no exists in GroupMember only if borrower_type is not 'group'
            if borrower_type not in ['group']:
                try:
                    group_member = GroupMember.objects.get(national_id=national_id_no)
                except GroupMember.DoesNotExist:
                    return render(request, self.template_name, {
                        'form': form,
                        'error_message': 'Member does not exist. Please enter a valid National Identification Number.'
                    })

            # Proceed with registration
            borrower = form.save(commit=False)
            borrower.username = username
            borrower.borrower_no = borrower_no
            borrower.save()
            
            # Create and save the payment
            borrower_no = borrower_no
            loanee = Loanee(
                borrower_no=borrower_no,
                approved = 'YES'
            )
            loanee.save()
            
            if borrower_type == 'entrepreneur':
                return redirect('register_entrepreneur', borrower_id=national_id_no, username=username)
            elif borrower_type == 'civil_servant':
                return redirect('register_civil_servant', borrower_id=national_id_no, username=username)
            elif borrower_type == 'employee':
                return redirect('register_employee', borrower_id=national_id_no, username=username)
            elif borrower_type == 'unemployed':
                return redirect('register_unemployed', borrower_id=national_id_no, username=username)
            elif borrower_type == 'group':
                return redirect('register_group', borrower_id=national_id_no, username=username)
            
            return redirect('success', username=username)

        return render(request, self.template_name, {'form': form})





class EntrepreneurCreateView(CreateView):
    model = Entrepreneur
    form_class = EntrepreneurForm
    template_name = 'register_entrepreneur.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['borrower_no'] = self.kwargs['borrower_id']
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower_id'] = self.kwargs['borrower_id']
        context['username'] = self.kwargs.get('username')
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        username = self.kwargs.get('username')
        success_url = reverse('success', kwargs={'username': username})
        return HttpResponseRedirect(success_url)


class CivilServantCreateView(CreateView):
    model = CivilServant
    form_class = CivilServantForm
    template_name = 'register_civil_servant.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['borrower_no'] = self.kwargs['borrower_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower_id'] = self.kwargs['borrower_id']
        context['username'] = self.kwargs.get('username')
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        username = self.kwargs.get('username')
        success_url = reverse('success', kwargs={'username': username})
        return HttpResponseRedirect(success_url)


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'register_employee.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['borrower_no'] = self.kwargs['borrower_id']
        return initial
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower_id'] = self.kwargs['borrower_id']
        context['username'] = self.kwargs.get('username')
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        username = self.kwargs.get('username')
        success_url = reverse('success', kwargs={'username': username})
        return HttpResponseRedirect(success_url)

class UnemployedCreateView(CreateView):
    model = Unemployed
    form_class = UnemployedForm
    template_name = 'register_unemployed.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['borrower_no'] = self.kwargs['borrower_id']
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower_id'] = self.kwargs['borrower_id']
        context['username'] = self.kwargs.get('username')
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        username = self.kwargs.get('username')
        success_url = reverse('success', kwargs={'username': username})
        return HttpResponseRedirect(success_url)

class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'register_group.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['borrower_no'] = self.kwargs['borrower_id']
        return initial
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower_id'] = self.kwargs['borrower_id']
        context['username'] = self.kwargs.get('username')
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        username = self.kwargs.get('username')
        success_url = reverse('success', kwargs={'username': username})
        return HttpResponseRedirect(success_url)

    
class BorrowerGroupCreateView(CreateView):
    model = BorrowerGroup
    form_class = BorrowerGroupForm
    template_name = 'register_borrower_group.html'
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['group_no'] = self.kwargs['group_id']
        return initial
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower_id'] = self.kwargs['borrower_id']
        return context


class LenderCreateView(View):
    template_name = 'register_lender.html'

    def get(self, request):
        form = LenderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LenderForm(request.POST)
        
        if form.is_valid():
            email_address = form.cleaned_data['email_address'].lower()
            lender_id_no = form.cleaned_data['lender_id_no']
            username = generate_lender_username(email_address)
            lender_no = generate_unique_lender_number(lender_id_no, email_address)
            lender_id = lender_id_no
            
            # Corrected handling of 'account_no'
            account = form.cleaned_data['account_no']  # Use 'account_no' from cleaned_data
            account_bal = account.account_bal

            if account_bal < 10000:
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': 'Account balance is below 10,000. Registration cannot proceed.'
                })
            
            lender = form.save(commit=False)
            lender.username = username
            lender.lender_no = lender_no
            lender.save()

            lender_type = form.cleaned_data['lender_type']
            
            if lender_type == 'bank':
                return redirect('register_bank', lender_id=lender_id, username=username)
            elif lender_type == 'group':
                return redirect('register_group_lender', lender_id=lender_id, username=username)
            
            return redirect('success', username=username)

        return render(request, self.template_name, {'form': form})


class BankCreateView(CreateView):
    model = Bank
    form_class = BankForm
    template_name = 'register_bank.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['lender_no'] = self.kwargs['lender_id']
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lender_id'] = self.kwargs['lender_id']
        context['username'] = self.kwargs.get('username')
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        username = self.kwargs.get('username')
        success_url = reverse('success', kwargs={'username': username})
        return HttpResponseRedirect(success_url)

class GroupLenderCreateView(CreateView):
    model = GroupLender
    form_class = GroupLenderForm
    template_name = 'register_group_lender.html'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['lender_no'] = self.kwargs['lender_id']
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lender_id'] = self.kwargs['lender_id']
        context['username'] = self.kwargs.get('username')
        context['groups'] = Group.objects.all()
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        username = self.kwargs.get('username')
        success_url = reverse('success', kwargs={'username': username})
        return HttpResponseRedirect(success_url)


class GroupSignUpView(View):
    template_name = 'group_signup.html'

    def get(self, request):
        form = GroupSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GroupSignUpForm(request.POST)

        if form.is_valid():
            borrower_no = form.cleaned_data['borrower_no']
            lender_no = form.cleaned_data['lender_no']
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']

            # REQ-1: Check if account already exists
            if System_User.objects.filter(username=username).exists():
                form.add_error(None, "This username has already been used!")
                return render(request, self.template_name, {'form': form})
            else:
                # Create the account
                # Save the application
                new_account = form.save(commit=False)
                new_account.set_password(form.cleaned_data['password_hash'])
                new_account.save()
                return redirect('group_login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})

class BorrowerSignUpView(View):
    template_name = 'borrower_signup.html'

    def get(self, request):
        form = BorrowerSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BorrowerSignUpForm(request.POST)

        if form.is_valid():
            borrower_no = form.cleaned_data['borrower_no']
            lender_no = form.cleaned_data['borrower_no']
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']

            # REQ-1: Check if account already exists
            if System_User.objects.filter(username=username).exists():
                form.add_error(None, "This username has already been used!")
                return render(request, self.template_name, {'form': form})
            else:
                # Create the account
                # Save the application
                new_account = form.save(commit=False)
                new_account.set_password(form.cleaned_data['password_hash'])
                new_account.save()
                return redirect('borrower_login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        
class BankSignUpView(View):
    template_name = 'bank_signup.html'

    def get(self, request):
        form = BankSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BankSignUpForm(request.POST)

        if form.is_valid():
            lender_no = form.cleaned_data['lender_no']
            borrower_no = form.cleaned_data['lender_no']
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']

            # Check if lender_no and username exist in the Lender model
            lender_exists = Lender.objects.filter(lender_no=lender_no).exists()
            username_exists = Lender.objects.filter(username=username).exists()

            if not lender_exists or not username_exists:
                # If either lender_no or username does not exist in the Lender model
                error_message = ""
                if not lender_exists:
                    error_message += "The lender number does not exist. Please register as a lender first."
                if not username_exists:
                    error_message += " The username does not exist. Please register as a lender first."

                form.add_error(None, error_message)
                return render(request, self.template_name, {'form': form}, error_message)

            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('bank_login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})


class PesaSignUpView(View):
    template_name = 'pesa_signup.html'

    def get(self, request):
        form = PesaSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PesaSignUpForm(request.POST)

        if form.is_valid():
            lender_no = "form.cleaned_data['lender_no']"
            borrower_no = "form.cleaned_data['lender_no']"
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']
            
            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('bank_login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})

class PesaLoginView(View):
    template_name = 'pesa_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    
            user = System_User.objects.filter(username=username).first()
            if user and user.check_password(password):
                 # Authentication successful
                request.session['username'] = user.username  # Store username in session
                return redirect(reverse('pesa'))
            else:
                # Authentication failed
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})


class Pesa_Dashboard_View(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('pesa_login')  # Redirect to login if username is not in session

        try:
            user = System_User.objects.get(username=username)
            
        except System_User.DoesNotExist:
            return redirect('pesa_login')

        return render(request, 'pesa.html', {'user': user})

class BorrowerListView(ListView):
    model = Borrower
    template_name = 'borrowers_list.html'  # Specify your template name here
    context_object_name = 'borrowers'  # The name of the list in the template context

    def get_queryset(self):
        # Optionally filter or order the queryset here
        return Borrower.objects.all()


class LenderListView(ListView):
    model = Lender
    template_name = 'lenders_list.html'  # Specify your template name here
    context_object_name = 'lenders'  # The name of the list in the template context

    def get_queryset(self):
        # Optionally filter or order the queryset here
        return Lender.objects.all()

                
class GroupLoginView(View):
    template_name = 'group_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if the username exists in the Lender model with lender_type 'group'
            lender = Lender.objects.filter(username=username, lender_type='group').first()
            if lender:
                user = System_User.objects.filter(username=username).first()
                if user and user.check_password(password):
                    # Authentication successful
                    request.session['username'] = user.username  # Store username in session
                    return redirect(reverse('group'))
                else:
                    # Authentication failed
                    error_message = 'Wrong Username or Password'
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            else:
                # Username does not exist in the Lender model with lender_type 'group'
                error_message = 'Username does not exist or is not associated with a group'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})

        
        
class BorrowerLoginView(View):
    template_name = 'borrower_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if the username exists in the Borrower model
            borrower = Borrower.objects.filter(username=username).first()
            if borrower:
                user = System_User.objects.filter(username=username).first()
                if user and user.check_password(password):
                    # Authentication successful
                    request.session['username'] = user.username  # Store username in session
                    return redirect(reverse('borrower'))
                else:
                    # Authentication failed
                    error_message = 'Wrong Username or Password'
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            else:
                # Username does not exist in the Borrower model
                error_message = 'Username does not exist or is not associated with a borrower'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})

        
        
class BankLoginView(View):
    template_name = 'bank_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = System_User.objects.filter(username=username).first()
            if user and user.check_password(password):
                # Authentication successful
                request.session['username'] = user.username  # Store username in session
                return redirect(reverse('bank'))
            else:
                # Authentication failed
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})
        

class Group_Dashboard_View(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('group_login')  # Redirect to login if username is not in session

        try:
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no  # Assuming borrower_no in System_User corresponds to borrower_no in Borrower
            lender_no = user.lender_no

            # Fetch the borrower object using borrower_no
            borrower = Borrower.objects.get(borrower_no=borrower_no)
            
            # Fetch the group object using the borrower
            group = Group.objects.get(borrower_no=borrower)
        except System_User.DoesNotExist:
            return redirect('group_login')
        except Borrower.DoesNotExist:
            return redirect('group_login')
        except Group.DoesNotExist:
            return redirect('group_login')

        request.session['borrower_no'] = borrower_no
        request.session['lender_no'] = lender_no

        return render(request, 'group.html', {'user': user, 'borrower_no': borrower_no, 'lender_no': lender_no, 'group': group})




class AddGroupMemberView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('group_login')  # Redirect to login if username is not in session

        try:
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
            borrower = Borrower.objects.get(borrower_no=borrower_no)
            group = Group.objects.get(borrower_no=borrower)
        except (System_User.DoesNotExist, Borrower.DoesNotExist, Group.DoesNotExist):
            return redirect('group_login')

        request.session['borrower_no'] = borrower_no

        form = GroupMemberForm()
        context = {
            'user': user,
            'group': group,
            'form': form,
        }
        return render(request, 'add_group_member.html', context)

    def post(self, request):
        form = GroupMemberForm(request.POST)
        username = request.session.get('username')
        if not username:
            return redirect('group_login')

        try:
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
            borrower = Borrower.objects.get(borrower_no=borrower_no)
            group = Group.objects.get(borrower_no=borrower)
        except (System_User.DoesNotExist, Borrower.DoesNotExist, Group.DoesNotExist):
            return redirect('group_login')

        if form.is_valid():
            account = form.cleaned_data.get('account')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            national_id = form.cleaned_data.get('national_id')
            if Defaulter.objects.filter(national_id=national_id).exists():
                return render(request, 'add_group_member.html', {
                    'form': form,
                    'error_message': 'This member is listed as a defaulter and cannot be added to the group.'
                })

            try:
                group_member = form.save(commit=False)
                group_member.member_no = generate_unique_member_number()  # Assign generated member number
                group_member.group = group  # Assign the group fetched from the session
                group_member.save()
                
                # Create and save the account
                account = Account(
                    account_no=account,
                    account_name=f'{first_name}  {last_name}',
                    account_bal=0.00,
                )
                account.save()

                return render(request, 'add_group_member.html', {
                    'form': GroupMemberForm(),
                    'member_no': group_member.member_no,
                    'success_message': f'Member {group_member.member_no} added successfully.'
                })
            except Exception as e:
                return render(request, 'add_group_member.html', {
                    'form': form,
                    'error_message': 'An error occurred while adding the member. Please try again.'
                })
        else:
            # Added detailed form errors for debugging
            print(form.errors)  # Print form errors to console or log them for debugging

        return render(request, 'add_group_member.html', {
            'form': form,
            'error_message': 'Form Invalid. Errors: {}'.format(form.errors)
        })

class MemberListView(ListView):
    template_name = 'member_list.html'
    context_object_name = 'members'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('group_login')  # Redirect to login if username is not in session
        try:
            # Query the user from the database using the username
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
            lender_no = user.lender_no
            
            borrower = Borrower.objects.get(borrower_no=borrower_no)
            # Retrieve the group using borrower_no (assuming it's a string)
            group = Group.objects.get(borrower_no=borrower)
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('group_login')
        except Group.DoesNotExist:
            # Handle the case where the group does not exist
            return redirect('group_login')

        # Store borrower_no and lender_no in session for future use
        request.session['borrower_no'] = borrower_no
        request.session['lender_no'] = lender_no
        group_no = group.group_no

        # Retrieve group members
        members = GroupMember.objects.filter(group=group_no)

        return render(request, self.template_name, {'members': members})


class MemberUpdateView(UpdateView):
    model = GroupMember
    fields = ['member_no', 'first_name', 'last_name', 'national_id', 'phone_number', 'dob', 'gender', 'group', 'grp_worth', 'account', 'approved']
    widgets = {
            'gender': forms.RadioSelect(choices=GroupMember.GENDER_CHOICES),
        }
    template_name = 'member_update_form.html'
    success_url = reverse_lazy('member_list')


class MemberDeleteView(DeleteView):
    model = GroupMember
    template_name = 'member_confirm_delete.html'
    success_url = reverse_lazy('member_list')


class Borrower_Dashboard_View(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('borrower_login')  # Redirect to login if username is not in session

        try:
            # Query the user from the database using the username
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('borrower_login')

        # Store borrower_no in the session
        request.session['borrower_no'] = borrower_no

        return render(request, 'borrower.html', {'user': user, 'borrower_no': borrower_no})
 
    


class Bank_Dashboard_View(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank_login')  # Redirect to login if username is not in session

        try:
            # Query the user from the database using the username
            user = System_User.objects.get(username=username)
            lender_no = user.lender_no
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('bank_login')
        
        # Store lender_no in the session
        request.session['lender_no'] = lender_no

        return render(request, 'bank.html', {'user': user, 'lender_no': lender_no})


class DefaultersView(View):
    template_name = 'defaulter.html'

    def get(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank')  # Redirect to the bank dashboard if lender_no is not in session

        form = DefaulterForm(initial={'lender_no': lender_no})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank')  # Redirect to the bank dashboard if lender_no is not in session

        form = DefaulterForm(request.POST)

        if form.is_valid():
            national_id = form.cleaned_data['national_id']
            amount_owed = form.cleaned_data['amount_owed']

            if Defaulter.objects.filter(national_id=national_id, lender_no=lender_no).exists():
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': 'Defaulter already exists. Please try again.'
                })

            defaulter = form.save(commit=False)
            defaulter.submission_date = datetime.now()  # Assign current date and time
            defaulter.lender_no = lender_no  # Assign lender_no from session
            defaulter.save()

            return redirect('defaulter_list')  # Redirect to the defaulter list after adding

        return render(request, self.template_name, {'form': form})


class DefaulterListView(View):
    template_name = 'defaulter_list.html'

    def get(self, request):
        defaulters = Defaulter.objects.all()
        return render(request, self.template_name, {'defaulters': defaulters})



class DefaulterUpdateView(View):
    template_name = 'defaulter_update.html'

    def get(self, request, pk):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank')  # Redirect to the bank dashboard if lender_no is not in session

        defaulter = get_object_or_404(Defaulter, pk=pk)
        if defaulter.lender_no != lender_no:
            messages.error(request, 'You have no privilege to update the details of this defaulter.')
            return redirect('defaulter_list')  # Redirect to the defaulter list if lender_no does not match

        form = DefaulterUpdateForm(instance=defaulter)
        return render(request, self.template_name, {'form': form, 'defaulter': defaulter})

    def post(self, request, pk):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank')  # Redirect to the bank dashboard if lender_no is not in session

        defaulter = get_object_or_404(Defaulter, pk=pk)
        if defaulter.lender_no != lender_no:
            messages.error(request, 'You have no privilege to update the details of this defaulter.')
            return redirect('defaulter_list')  # Redirect to the defaulter list if lender_no does not match

        form = DefaulterUpdateForm(request.POST, instance=defaulter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Defaulter details successfully updated.')
            return redirect('defaulter_list')  # Redirect to the defaulter list after updating

        return render(request, self.template_name, {'form': form, 'defaulter': defaulter})



class DefaulterDeleteView(View):

    def post(self, request, pk):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank')  # Redirect to the bank dashboard if lender_no is not in session

        defaulter = get_object_or_404(Defaulter, pk=pk)
        if defaulter.lender_no != lender_no:
            messages.error(request, 'You have no privilege to delete this defaulter.')
            return redirect('defaulter_list')  # Redirect to the defaulter list if lender_no does not match

        defaulter.delete()
        messages.success(request, 'Defaulter successfully deleted.')
        return redirect('defaulter_list')  # Redirect to the defaulter list after deleting


class AllocationView(View):
    template_name = 'allocation.html'

    def get(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank')  # Redirect to the bank dashboard if lender_no is not in session

        form = AllocationForm(initial={'lender_no': lender_no})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank_login')  # Redirect to the bank dashboard if lender_no is not in session

        form = AllocationForm(request.POST)

        if form.is_valid():
            allocation_no = unique_allocation_number()
            amount = form.cleaned_data['amount']
            allocation_date = datetime.now()  # Get current date and time

            # Fetch the lender and their account balance
            try:
                lender = Lender.objects.get(lender_no=lender_no)
                account = Account.objects.get(account_no=lender.account_no.account_no)
                account_balance = account.account_bal
            except Lender.DoesNotExist:
                return redirect('bank')
            except Account.DoesNotExist:
                return redirect('bank')

            # Ensure the amount is 2000 less than the account balance
            if amount > (account_balance - 2000):
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': f'The allocated amount must be less than {account_balance - 2000}.'
                })

            # Create and save the allocation
            allocation = form.save(commit=False)
            allocation.allocation_no = allocation_no  # Assign the generated allocation number
            allocation.allocation_date = allocation_date  # Assign current date and time
            allocation.lender_no = lender_no  # Assign lender_no from session
            allocation.save()

            # Create and save the message
            message_no = self.generate_unique_message_number()
            message = Message(
                message_no=message_no,
                sender_username=lender.username,  # Assuming lender.username is the sender
                recipient_username=lender.username,  # Assuming the recipient is also the lender
                message_name='Allocation Notice',  # You can customize this
                message_description=f'Allocation Number {allocation_no} of amount {amount} has been successfully processed.',
                message_date=allocation_date.date()  # Use only the date part
            )
            message.save()

            return render(request, self.template_name, {
                'form': AllocationForm(),
                'allocation_no': allocation_no,
                'success_message': f'Allocation successful. Allocation Number: {allocation_no}'
            })

        else:
            print(form.errors)  # Print form errors to console or log them for debugging

            # If the form is not valid, return the template with the form
            return render(request, self.template_name,  {
                'form': AllocationForm(),
                'allocation_no': allocation_no,
                'error_message': 'Form Invalid. Errors: {}'.format(form.errors)
            })

    def generate_unique_allocation_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            allocation_no = letters + digits
            if not Allocation.objects.filter(allocation_no=allocation_no).exists():
                return allocation_no

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no


        
class GroupAllocationView(View):
    template_name = 'group_allocation.html'

    def get(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('group')

        form = AllocationForm(initial={'lender_no': lender_no})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('group_login')

        form = AllocationForm(request.POST)

        if form.is_valid():
            allocation_no = unique_allocation_number()
            amount = form.cleaned_data['amount']
            allocation_date = datetime.now()

            try:
                lender = Lender.objects.get(lender_no=lender_no)
            except Lender.DoesNotExist:
                return redirect('group')

            allocation = form.save(commit=False)
            allocation.allocation_no = allocation_no
            allocation.allocation_date = allocation_date
            allocation.lender_no = lender_no
            allocation.save()

            return render(request, self.template_name, {
                'form': AllocationForm(),
                'allocation_no': allocation_no,
                'success_message': f'Allocation successful. Allocation Number: {allocation_no}'
            })
            
               
        print(form.errors)  # Print form errors to console or log them for debugging
        return render(request, self.template_name, {
            'form': form,
            'error_message': 'Form Invalid. Errors: {}'.format(form.errors),
        })

    def generate_unique_allocation_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            allocation_no = letters + digits
            if not Allocation.objects.filter(allocation_no=allocation_no).exists():
                return allocation_no

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no



        
class AllocationsView(ListView):
    model = Allocation
    template_name = 'allocations_list.html'
    context_object_name = 'allocations'


class GroupAllocationsView(ListView):
    model = Allocation
    template_name = 'grp_allocations_list.html'
    context_object_name = 'allocations'

    def get_queryset(self):
        # Get the lender_no from the session
        lender_no_session = self.request.session.get('lender_no')

        # Check if lender_no is present in the session
        if lender_no_session:
            # Filter allocations where lender_no does not match the lender_no in the session
            return Allocation.objects.exclude(lender_no=lender_no_session)
        else:
            # If lender_no is not in the session, handle according to your application needs
            # For example, return an empty queryset or handle the case appropriately
            return Allocation.objects.none()  # No allocations listed if lender_no is not in session
        


class ApplicationView(FormView):
    form_class = ApplicationForm
    template_name = 'application.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        allocation_no = self.kwargs['allocation_no']
        
        # Retrieve borrower_no from session
        borrower_no = self.request.session.get('borrower_no', None)
        
        kwargs['initial'] = {
            'allocation_no': allocation_no,
            'application_no': self.generate_unique_application_number(),
            'application_date': timezone.now().date(),
            'borrower_no': borrower_no  # Add borrower_no to initial data
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocation_no'] = self.kwargs['allocation_no']
        
        # Add borrower_no to context
        context['borrower_no'] = self.request.session.get('borrower_no', None)
        
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        allocation_no = self.kwargs['allocation_no']
        application_no = unique_application_number()
        borrower_no = self.request.session.get('borrower_no', None)
        
        # Fetch Borrower object using borrower_no
        borrower = get_object_or_404(Borrower, borrower_no=borrower_no)
        
        # Fetch GroupMember related to the borrower's national_id
        group_member = get_object_or_404(GroupMember, national_id=borrower.national_id)
        
        group_no = group_member.group.group_no if hasattr(group_member.group, 'group_no') else group_member.group  # Ensure this is fetching the correct attribute
        member_count = GroupMember.objects.filter(group=group_member.group).count()

        


        # Fetch Group object related to group_no
        group = get_object_or_404(Group, group_no=group_no)

        # Fetch Account object related to group's account
        account = get_object_or_404(Account, account_no=group.account.account_no)
        group_lender = get_object_or_404(GroupLender, group_no=group)
        lender_no = group_lender.lender_no.lender_no
        total_allocations = Allocation.objects.filter(lender_no=lender_no).count()
        grp_worth = account.account_bal
        account_n = group_member.account
        member_acc = get_object_or_404(Account, account_no=account_n)
        member_bal = member_acc.account_bal
        # Additional logic you have in your form_valid method
        age = group_member.calculate_age()
        gender = group_member.gender
        membgrp_worth = group_member.grp_worth
        
        # Check if the member is approved
        if group_member.approved != GroupMember.YES:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': 'This group member is not approved for a loan.'
            })
        
        # Assign account balance to member_balance
        member_balance = account.account_bal
        #loan =  get_object_or_404(Loan, borrower_no=borrower_no)
        
        # Fetch GroupLender object based on group_no
        #group_lender = get_object_or_404(GroupLender, group_no=group_member.group.group_no)
        
        # Fetch Allocation object
        allocation = get_object_or_404(Allocation, allocation_no=allocation_no)
        
        # Fetch Lender object based on lender_no from Allocation
        lender = get_object_or_404(Lender, lender_no=allocation.lender_no)

        # Calculate the total applied amount for the allocation_no
        total_applied_amount = Application.objects.filter(allocation_no=allocation_no).aggregate(total=models.Sum('loan_amount'))['total'] or 0
        remaining_amount = allocation.amount - total_applied_amount

        # Check if the loan amount to be applied is less than or equal to the remaining amount
        loan_amount = form.cleaned_data['loan_amount']
        if loan_amount > remaining_amount:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'The loan amount exceeds the remaining allocation amount of {remaining_amount}.'
            })
            
        # Test MachineLearningModel class
        ml_model = MachineLearningModel()
        mse, r2 = ml_model.accuracy()
        loan_proposal = LoanProposal()
        #loan_proposal.data_retrieval('Mary', age, 'Male', member_bal, member_count, 300000, 3500, 7, loan_amount)
        loan_proposal.data_retrieval('Mary', age, gender, member_bal, member_count, grp_worth, membgrp_worth, total_allocations, loan_amount)
        prediction_result = loan_proposal.data_preparation()
        result = float(f"{float(prediction_result):.2f}")
        # Assign form data to the application instance
        application = form.save(commit=False)
        application.allocation_no = allocation_no
        application.application_no = application_no
        application.application_date = timezone.now().date()
        application.proposed_amount = result  # Assign the loan amount
        application.borrower_no = borrower_no  # Correctly assign the borrower object
        
        
        # Check if the borrower has any unsettled loans with a balance above 0   
        loanee = get_object_or_404(Loanee, borrower_no=borrower_no)    
        if loanee.approved != 'YES':
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_application_no': application_no,
                'error_message': 'You already have unsettled loan(s). Please settle your loan(s) first!'
            })
            
        if loanee.applied != 'NO':
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_application_no': application_no,
                'error_message': 'You already have an hanging application. Please be patient, Your Loan will be Disbursed soon!'
            })
        
        # Save the form instance
        application.save()
        
        # Create and save the message
        message_no = self.generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=borrower.username,  # Borrower's username
            recipient_username=lender.username,  # Lender's username
            message_name='Loan Application Submitted',
            message_description=f'Application Number {application_no} for grp_worth{grp_worth} amount membgrp_worth {membgrp_worth} has allocation count{total_allocations}been gender {gender}submitted.',
            message_date=timezone.now().date()
        )
        message.save()
        
        return render(self.request, self.template_name, {
            'form': ApplicationForm(),
            'allocation_no': allocation_no,
            'application_no': application_no,
            'success_message': f'Application successful. Application Number: {application_no}'
        })

    def form_invalid(self, form):
        allocation_no = self.kwargs['allocation_no']
        print(form.errors)  # Print form errors to console or log them for debugging
        return render(self.request, self.template_name, {
            'form': form,
            'allocation_no': allocation_no,
            'error_message': f'Form Invalid. Errors: {form.errors}',
        })

    def generate_unique_application_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            application_no = letters + digits
            if not Application.objects.filter(application_no=application_no).exists():
                return application_no

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no




        


class GroupApplicationView(FormView):
    form_class = ApplicationForm
    template_name = 'group_application.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        allocation_no = self.kwargs['allocation_no']
        borrower_no = self.request.session.get('borrower_no', None)
        
        kwargs['initial'] = {
            'allocation_no': allocation_no,
            'application_no': unique_application_number(),
            'application_date': timezone.now().date(),
            'borrower_no': borrower_no
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocation_no'] = self.kwargs['allocation_no']
        context['borrower_no'] = self.request.session.get('borrower_no', None)
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        allocation_no = self.kwargs['allocation_no']
        application_no = unique_application_number()
        borrower_no = self.request.session.get('borrower_no', None)

        # Retrieve the Borrower instance based on borrower_no
        borrower = get_object_or_404(Borrower, borrower_no=borrower_no)

        # Retrieve the Group instance based on Borrower instance
        group = get_object_or_404(Group, borrower_no=borrower)

        # Retrieve the account related to the group
        account = group.account

        # Calculate the total amount applied for the specified allocation_no
        total_applied_amount = Application.objects.filter(allocation_no=allocation_no).aggregate(total=Sum('loan_amount'))['total'] or 0

        # Retrieve the allocation amount
        allocation = get_object_or_404(Allocation, allocation_no=allocation_no)
        allocation_amount = allocation.amount

        # Calculate the remaining amount for the allocation
        remaining_allocation_amount = allocation_amount - total_applied_amount

        loan_amount = form.cleaned_data['loan_amount']

        # Determine proposed_amount
        proposed_amount = min(loan_amount, remaining_allocation_amount)

        # Save the application
        form.instance.allocation_no = allocation_no
        form.instance.application_no = application_no
        form.instance.application_date = timezone.now().date()
        form.instance.proposed_amount = proposed_amount
        form.instance.borrower_no = borrower_no
        
        # Check if the borrower has any unsettled loans with a balance above 0   
        loanee = get_object_or_404(Loanee, borrower_no=borrower_no)    
        if loanee.approved != 'YES':
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_application_no': application_no,
                'error_message': 'You already have unsettled loan(s). Please settle your loan(s) first!'
            })
            
        if loanee.applied != 'NO':
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_application_no': application_no,
                'error_message': 'You already have an hanging application. Please be patient, Your Loan will be Disbursed soon!'
            })
            
        # Save the application instance
        application = form.save()

        # Fetch the lender’s username
        lender_no = allocation.lender_no
        try:
            lender = Lender.objects.get(lender_no=lender_no)
        except Lender.DoesNotExist:
            return self.render_to_response({
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'Lender with number {lender_no} does not exist.'
            })

        # Create and save the message
        message_no = self.generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=borrower.username,  # Using borrower directly
            recipient_username=lender.username,
            message_name='Group Loan Application Submitted',
            message_description=f'Application Number {application_no} for amount {form.cleaned_data["loan_amount"]} has been submitted.',
            message_date=timezone.now().date()
        )
        message.save()

        return self.render_to_response({
            'form': ApplicationForm(),
            'allocation_no': allocation_no,
            'application_no': application_no,
            'success_message': f'Application successful. Application Number: {application_no}'
        })

    def form_invalid(self, form):
        allocation_no = self.kwargs['allocation_no']
        return self.render_to_response({
            'form': form,
            'allocation_no': allocation_no,
            'error_message': 'Form Invalid. Errors: {}'.format(form.errors),
        })

    def generate_unique_application_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            application_no = letters + digits
            if not Application.objects.filter(application_no=application_no).exists():
                return application_no

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no


class RequestsView(ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        # Get the lender_no from the session
        lender_no_session = self.request.session.get('lender_no')

        if lender_no_session:
            # Get allocations related to the lender_no
            allocations = Allocation.objects.filter(lender_no=lender_no_session)
            
            # Extract allocation numbers
            allocation_numbers = allocations.values_list('allocation_no', flat=True)

            # Get applications related to these allocations and exclude those with disbursements
            applications_without_disbursement = Application.objects.filter(
                allocation_no__in=allocation_numbers
            ).exclude(
                application_no__in=Disbursement.objects.values_list('application_no', flat=True)
            )
            
            return applications_without_disbursement
        else:
            # If lender_no is not in the session, handle appropriately
            return Application.objects.none()  # No applications listed if lender_no is not in session



class DisbursementView(FormView):
    form_class = DisbursementForm
    template_name = 'disbursement.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        application_no = self.kwargs['application_no']
        kwargs['initial'] = {
            'application_no': application_no,
            'transaction_no': unique_transaction_number(),
            'disbursement_date': datetime.now().date()
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application_no'] = self.kwargs['application_no']
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        application_no = self.kwargs['application_no']
        transaction_no = unique_transaction_number()

        application = get_object_or_404(Application, application_no=application_no)
        allocation = get_object_or_404(Allocation, allocation_no=application.allocation_no)
        lender_no = allocation.lender_no
        borrower_no = application.borrower_no
        lender = Lender.objects.get(lender_no=lender_no)

        borrower = get_object_or_404(Borrower, borrower_no=borrower_no)

        # Get the proposed amount from the Application table
        proposed_amount = application.proposed_amount

        # Check if the entered amount is valid
        entered_amount = form.cleaned_data.get('disbursed_amount')
        if entered_amount > proposed_amount:
            entered_amount = proposed_amount
            
        if entered_amount < 100.00:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': form.cleaned_data.get('transaction_no', None),
                'error_message': 'You can not Disburse Amount less than Kshs 100'
            })

        # Determine the borrower's account based on the borrower type
        if borrower.borrower_type == 'group':
            # For group borrowers, fetch the Group and corresponding Account
            group = get_object_or_404(Group, borrower_no=borrower)
            borrower_account = get_object_or_404(Account, account_no=group.account.account_no)
        else:
            # For individual borrowers, use the national ID to find the GroupMember and their Account
            borrower_id = borrower.national_id
            member_account = get_object_or_404(GroupMember, national_id=borrower_id)
            borrower_account = Account.objects.get(account_no=member_account.account)

        # Fetch the lender's account
        lender_account = get_object_or_404(Account, account_no=lender.account_no.account_no)

        # Check if the lender's account has sufficient balance
        if lender_account.account_bal < entered_amount:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': form.cleaned_data.get('transaction_no', None),
                'error_message': f'Insufficient account balance. Current balance is {lender_account.account_bal}.'
            })

        # Update lender's account balance
        lender_account.account_bal -= entered_amount
        lender_account.save()

        # Update borrower's account balance
        borrower_account.account_bal += entered_amount
        borrower_account.save()

        disbursed_amount = entered_amount
        # Save the disbursement if everything is valid
        form.instance.disbursed_amount = disbursed_amount
        form.instance.application_no = application_no
        form.instance.transaction_no = transaction_no
        form.instance.borrower_no = borrower_no
        form.instance.loan_duration_months = 12
        form.instance.disbursement_date = datetime.now().date()

        form.save()
        
        loanee = get_object_or_404(Loanee, borrower_no=borrower_no)
        loanee.approved = 'NO'
        loanee.applied = 'NO'
        loanee.save()

        # Create and save the message
        message_no = self.generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=lender.username,
            recipient_username=borrower.username,
            message_name='Disbursement Successfully Submitted',
            message_description=f'Transaction Number {transaction_no} for amount {entered_amount} has been submitted.',
            message_date=timezone.now().date()
        )
        message.save()

        # Create and save the payment
        payment_no = unique_payment_number()
        payment = Payment(
            payment_no=payment_no,
            transaction_no=transaction_no,
            payment_amount=0,
            payment_date=timezone.now().date()
        )
        payment.save()

        # Create and save the loan
        payment_no = unique_payment_number()
        loan = Loan(
            transaction_no=transaction_no,
            payment_no=payment_no,
            borrower_no=borrower_no,
            lender_no=lender_no,
            principal=disbursed_amount,
            loan_interest=allocation.interest_rate,
            principal_interest=disbursed_amount,
            amount_paid=0,
            balance=disbursed_amount,
            loan_date=timezone.now().date()
        )
        loan.save()
        return render(self.request, self.template_name, {
            'form': DisbursementForm(),
            'application_no': application_no,
            'transaction_no': transaction_no,
            'success_message': f'Disbursement successful. Transaction Number: {form.instance.transaction_no}'
        })

    def form_invalid(self, form):
        application_no = self.kwargs['application_no']
        return render(self.request, self.template_name, {
            'form': form,
            'application_no': application_no,
            'error_transaction_no': form.cleaned_data.get('transaction_no', None),
            'error_message': 'There was an error with your disbursement. Please correct the errors.'
        })

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no




class GroupDisbursementView(FormView):
    form_class = DisbursementForm
    template_name = 'group_disbursement.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        application_no = self.kwargs['application_no']
        kwargs['initial'] = {
            'application_no': application_no,
            'transaction_no': unique_transaction_number(),
            'disbursement_date': timezone.now().date()
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application_no'] = self.kwargs['application_no']
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        application_no = self.kwargs['application_no']
        transaction_no = unique_transaction_number()

        # Retrieve application and related models
        application = get_object_or_404(Application, application_no=application_no)
        allocation = get_object_or_404(Allocation, allocation_no=application.allocation_no)
        
        lender_no = allocation.lender_no
        borrower_no = application.borrower_no
        lender = get_object_or_404(Lender, lender_no=lender_no)
        borrower = get_object_or_404(Borrower, borrower_no=borrower_no)

        # Get the proposed amount from the Application table
        proposed_amount = application.proposed_amount

        # Check if the entered amount is valid
        entered_amount = form.cleaned_data.get('disbursed_amount')
        if entered_amount > proposed_amount:
            entered_amount = proposed_amount 
            
        if entered_amount < 100.00:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': form.cleaned_data.get('transaction_no', None),
                'error_message': 'You can not Disburse Amount less than Kshs 100'
            })
       
        
        # Determine the borrower's account based on the borrower type
        if borrower.borrower_type == 'group':
            # For group borrowers, fetch the Group and corresponding Account
            group = get_object_or_404(Group, borrower_no=borrower)
            borrower_account = get_object_or_404(Account, account_no=group.account.account_no)
        else:
            # For individual borrowers, use the national ID to find the GroupMember and their Account
            borrower_id = borrower.national_id
            member_account = get_object_or_404(GroupMember, national_id=borrower_id)
            borrower_account = Account.objects.get(account_no=member_account.account)
        # Get lender's account using the lender's account number
        lender_account = get_object_or_404(Account, account_no=lender.account_no.account_no)

        # Check if the lender's account has sufficient balance
        if lender_account.account_bal < entered_amount:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': form.cleaned_data.get('transaction_no', None),
                'error_message': f'Insufficient account balance. Current balance is {lender_account.account_bal}.'
            })
            
        # Update lender's account balance
        lender_account.account_bal -= entered_amount
        lender_account.save()

        # Update borrower's account balance
        borrower_account.account_bal += entered_amount
        borrower_account.save()
        disbursed_amount = entered_amount

        # Save the disbursement if everything is valid
        form.instance.disbursed_amount = disbursed_amount
        form.instance.application_no = application_no
        form.instance.transaction_no = transaction_no
        form.instance.borrower_no = borrower_no
        form.instance.loan_duration_months = 12
        form.instance.disbursement_date = timezone.now().date()

        form.save()
        
        loanee = get_object_or_404(Loanee, borrower_no=borrower_no)
        loanee.approved = 'NO'
        loanee.applied = 'NO'
        loanee.save()


        # Create and save the message
        message_no = generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=lender.username,
            recipient_username=borrower.username,
            message_name='Disbursement Successfully Submitted',
            message_description=f'Transaction Number {transaction_no} for amount {entered_amount} has been submitted.',
            message_date=timezone.now().date()
        )
        message.save()
        
        # Create and save the payment
        payment_no = unique_payment_number()
        payment = Payment(
            payment_no=payment_no,
            transaction_no=transaction_no,
            payment_amount=0,
            payment_date=timezone.now().date()
        )
        payment.save()
        
        
        # Create and save the loan
        payment_no = unique_payment_number()
        loan = Loan(
            transaction_no=transaction_no,
            payment_no=payment_no,
            borrower_no = borrower_no,
            lender_no = lender_no,
            principal = disbursed_amount,
            loan_interest = allocation.interest_rate,
            principal_interest = disbursed_amount,
            amount_paid = 0,
            balance = disbursed_amount,
            loan_date=timezone.now().date()
        )
        loan.save()


        return self.render_success(form, application_no, transaction_no)

    def form_invalid(self, form):
        application_no = self.kwargs['application_no']
        transaction_no = form.cleaned_data.get('transaction_no', None)
        return self.render_error(form, application_no, transaction_no, 'There was an error with your disbursement. Please correct the errors.')

    def render_error(self, form, application_no, transaction_no, error_message):
        return render(self.request, self.template_name, {
            'form': form,
            'application_no': application_no,
            'transaction_no': transaction_no,
            'error_message': error_message
        })

    def render_success(self, form, application_no, transaction_no):
        return render(self.request, self.template_name, {
            'form': DisbursementForm(),
            'application_no': application_no,
            'transaction_no': transaction_no,
            'success_message': f'Disbursement successful. Transaction Number: {transaction_no}'
        })


class LoanPaymentView(View):
    template_name = 'payment_form.html'

    def get(self, request, transaction_no):
        loan = get_object_or_404(Loan, transaction_no=transaction_no)
        form = PaymentForm()

        context = {
            'loan': loan,
            'form': form,
            'transaction_no': transaction_no,
            'success_message': request.GET.get('success_message', ''),
            'error_message': request.GET.get('error_message', ''),
        }

        return render(request, self.template_name, context)

    def post(self, request, transaction_no):
        loan = get_object_or_404(Loan, transaction_no=transaction_no)
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment_amount = form.cleaned_data['payment_amount']

            disbursement = get_object_or_404(Disbursement, transaction_no=transaction_no)
            disbursement_date = disbursement.disbursement_date

            borrower_no = loan.borrower_no
            lender_no = loan.lender_no
            borrower = get_object_or_404(Borrower, borrower_no=borrower_no)
            lender = get_object_or_404(Lender, lender_no=lender_no)

            if borrower.borrower_type == 'group':
                group = get_object_or_404(Group, borrower_no=borrower)
                borrower_account = get_object_or_404(Account, account_no=group.account.account_no)
            else:
                borrower_id = borrower.national_id
                member_account = get_object_or_404(GroupMember, national_id=borrower_id)
                borrower_account = get_object_or_404(Account, account_no=member_account.account)

            lender_account = get_object_or_404(Account, account_no=lender.account_no.account_no)

            if borrower_account.account_bal < payment_amount:
                error_message = 'You have Insufficient Account Balance to Complete this Transaction.'
                return render(request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': error_message,
                })

            interest_rate = loan.loan_interest
            loan_duration = disbursement.loan_duration_months

            elapsed_months = calculate_time_elapsed_in_months(disbursement_date)
            new_loan_interest = calculate_compound_interest(loan.balance, interest_rate, elapsed_months)
            loan.loan_interest = interest_rate
            loan.principal_interest = new_loan_interest

            # Ensure payment amount does not exceed the loan balance
            if payment_amount > loan.balance:
                error_message = 'Payment amount exceeds the current loan balance. Please enter a valid amount.'
                return render(request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': error_message,
                })
                
            if payment_amount < 1.00:
                error_message = 'Payment amount should be Kshs 1 and above.'
                return render(self.request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': error_message,
                })


            loan.amount_paid += payment_amount
            loan.balance = loan.principal_interest - loan.amount_paid
            if loan.balance < 0:
                loan.balance = 0  # Ensure balance does not go below 0
            loan.loan_date = datetime.now().date()
            loan.save()
            if loan.balance == 0:
                loanee = get_object_or_404(Loanee, borrower_no=borrower_no)
                loanee.approved = 'YES'
                loanee.save()

            
            borrower_account.account_bal -= payment_amount
            borrower_account.save()

            # Update lender's and borrower's account balances
            lender_account.account_bal += payment_amount
            lender_account.save()

            # Create and save the message
            message_no = generate_unique_message_number()
            message = Message(
                message_no=message_no,
                sender_username=lender.username,
                recipient_username=borrower.username,
                message_name='Payment Successfully Completed',
                message_description=(
                    f'Loan Payment for Disbursement Transaction Number {transaction_no} '
                    f'amount {payment_amount} has been submitted. '
                    f'Balance: {loan.balance}'
                ),
                message_date=timezone.now().date()
            )
            message.save()

            success_message = f'Payment of {payment_amount} received successfully. Loan balance updated.'
            return redirect(f'{reverse("payment", args=[transaction_no])}?success_message={success_message}')

        error_message = 'Payment failed. Please correct the errors below.'
        return render(request, self.template_name, {
            'loan': loan,
            'form': form,
            'transaction_no': transaction_no,
            'error_message': error_message,
        })



class GroupLoanPaymentView(View):
    template_name = 'payment_form.html'

    def calculate_loan_interest(self, principal, rate, duration_months):
        """
        Calculate loan interest based on principal, rate, and duration.
        """
        rate = Decimal(rate)
        duration_months = Decimal(duration_months)
        return principal * rate * duration_months

    def get(self, request, transaction_no):
        loan = get_object_or_404(Loan, transaction_no=transaction_no)
        form = PaymentForm()
        context = {
            'loan': loan,
            'form': form,
            'transaction_no': transaction_no,
        }
        return render(request, self.template_name, context)

    def post(self, request, transaction_no):
        loan = get_object_or_404(Loan, transaction_no=transaction_no)
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment_amount = form.cleaned_data['payment_amount']

            disbursement = get_object_or_404(Disbursement, transaction_no=transaction_no)
            disbursement_date = disbursement.disbursement_date

            borrower_no = loan.borrower_no
            lender_no = loan.lender_no
            borrower = get_object_or_404(Borrower, borrower_no=borrower_no)
            lender = get_object_or_404(Lender, lender_no=lender_no)

            if borrower.borrower_type == 'group':
                group = get_object_or_404(Group, borrower_no=borrower)
                borrower_account = get_object_or_404(Account, account_no=group.account.account_no)
            else:
                borrower_id = borrower.national_id
                member_account = get_object_or_404(GroupMember, national_id=borrower_id)
                borrower_account = get_object_or_404(Account, account_no=member_account.account)

            if borrower_account.account_bal < payment_amount:
                return render(request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': 'You have Insufficient Account Balance to Complete this Transaction.'
                })

            lender_account = get_object_or_404(Account, account_no=lender.account_no.account_no)

            # Update loan details
            interest_rate = loan.loan_interest
            loan_duration = disbursement.loan_duration_months
            elapsed_months = calculate_time_elapsed_in_months(disbursement_date)
            new_loan_interest = calculate_compound_interest(loan.balance, interest_rate, elapsed_months)
            loan.loan_interest = interest_rate
            loan.principal_interest = new_loan_interest

            # Ensure payment does not reduce balance below 0
            if payment_amount > loan.balance:
                return render(request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': 'Payment amount exceeds the current loan balance.'
                })
                
            if payment_amount < 1.00:
                error_message = 'Payment amount should be Kshs 1 and above.'
                return render(self.request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': error_message,
                })

            loan.amount_paid += payment_amount
            loan.balance = loan.principal_interest - loan.amount_paid
            if loan.balance < 0:
                loan.balance = 0  # Ensure balance does not go below 0
            loan.loan_date = datetime.now().date()
            loan.save()
            if loan.balance == 0:
                loanee = get_object_or_404(Loanee, borrower_no=borrower_no)
                loanee.approved = 'YES'
                loanee.save()

            borrower_account.account_bal -= payment_amount
            borrower_account.save()

            # Update lender's account balance
            lender_account.account_bal += payment_amount
            lender_account.save()

            # Create and save the message
            message_no = generate_unique_message_number()
            message = Message(
                message_no=message_no,
                sender_username=lender.username,
                recipient_username=borrower.username,
                message_name='Payment Successfully Completed',
                message_description=(
                    f'Loan Payment for Disbursement Transaction Number {transaction_no} '
                    f'amount {payment_amount} has been submitted. '
                    f'Balance: {loan.balance}'
                ),
                message_date=timezone.now().date()
            )
            message.save()

            return render(request, self.template_name, {
                'loan': loan,
                'form': PaymentForm(),
                'transaction_no': transaction_no,
                'success_message': 'Payment processed successfully.'
            })

        return render(request, self.template_name, {
            'loan': loan,
            'form': form,
            'transaction_no': transaction_no,
            'error_message': 'Form Invalid. Errors: {}'.format(form.errors),
        })



class GroupLoansView(ListView):
    template_name = 'loans.html'
    context_object_name = 'loans'

    def get(self, request):
        # Check if user is logged in and retrieve their information
        username = request.session.get('username')
        if not username:
            return redirect('group_login')  # Redirect to login if username is not in session

        try:
            # Get the user and related borrower and lender numbers
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
            lender_no = user.lender_no
        except System_User.DoesNotExist:
            return redirect('group_login')

        # Initialize loan lists as empty
        loans_to_pay = []
        loans_to_be_paid = []

        # Retrieve loans if borrower_no and lender_no are in session
        if borrower_no:
            loans_to_pay = Loan.objects.filter(borrower_no=borrower_no)
        if lender_no:
            loans_to_be_paid = Loan.objects.filter(lender_no=lender_no)

        # Pass the loans to the template
        return render(request, self.template_name, {
            'loans_to_pay': loans_to_pay,
            'loans_to_be_paid': loans_to_be_paid
        })

class BankLoansView(ListView):
    template_name = 'bank_loans.html'
    context_object_name = 'loans_to_be_paid'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank_login')  # Redirect to login if username is not in session
        try:
            # Query the user from the database using the username
            user = System_User.objects.get(username=username)
            lender_no = user.lender_no
            
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('bank_login')

        # Store  lender_no in session for future use
        request.session['lender_no'] = lender_no

        # Retrieve loans
        loans_to_be_paid = Loan.objects.filter(lender_no = lender_no)

        return render(request, self.template_name, {'loans_to_be_paid': loans_to_be_paid})
    
    
class BorrowerLoansView(ListView):
    template_name = 'borrower_loans.html'
    context_object_name = 'loans_to_pay'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('borrower_login')  # Redirect to login if username is not in session
        try:
            # Query the user from the database using the username
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
            
            borrower = Borrower.objects.get(borrower_no=borrower_no)
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('borrower_login')

        # Store borrower_no  in session for future use
        request.session['borrower_no'] = borrower_no

        # Retrieve Loans
        loans_to_pay = Loan.objects.filter(borrower_no = borrower_no)
        
        return render(request, self.template_name, {'loans_to_pay': loans_to_pay})
    


class MessagesListView(ListView):
    template_name = 'messages.html'
    context_object_name = 'messages'

    def get(self, request):
        # Check if user is logged in and retrieve their information
        username = request.session.get('username')
        if not username:
            return redirect('group_login')  # Redirect to login if username is not in session
        
        # Initialize message lists as empty
        received_mssgs = []
        sent_mssgs = []

        # Retrieve loans if borrower_no and lender_no are in session
        if username:
            received_mssgs = Message.objects.filter(recipient_username=username)
        if username:
            sent_mssgs = Message.objects.filter(sender_username=username)

        # Pass the loans to the template
        return render(request, self.template_name, {
            'received_mssgs': received_mssgs,
            'sent_mssgs': sent_mssgs
        })


class GuarantorFormView(View):
    def get(self, request):
        return render(request, 'guarantor_form.html')

    def post(self, request):
        national_id = request.POST.get('national_id')
        try:
            guarantor = Guarantor.objects.get(national_id=national_id)
        except Guarantor.DoesNotExist:
            return render(request, 'guarantor_form.html', {'error_message': f'Guarantor with National Identification Number "{national_id}" not found.'})

        report_data = {
            'guarantor_details': {
                'National ID Number': guarantor.national_id,
                'First Name': guarantor.guarantor_first_name,
            },
            'last_name': guarantor.guarantor_last_name,
            'phone_number': guarantor.phone_number,
        }

        # Generate PDF
        pdf_generator = GroupPDFGenerator(report_data)
        pdf_bytes = pdf_generator.generate_pdf()

        # Return the PDF file as a response
        response = HttpResponse(pdf_bytes, content_type='form/pdf')
        response['Content-Disposition'] = f'attachment; filename="{guarantor.guarantor_first_name} {guarantor.guarantor_last_name}_form.pdf"'
        return response
    
class BankShipFormView(View):
    def get(self, request):
        return render(request, 'bank_form.html')

    def post(self, request):
        bank_name = request.POST.get('bank_name')
        report_data = {
            'bank_name': bank_name,
        }

        # Generate PDF
        pdf_generator = BankPDFGenerator(report_data)
        pdf_bytes = pdf_generator.generate_pdf()

        # Return the PDF file as a response
        response = HttpResponse(pdf_bytes, content_type='form/pdf')
        response['Content-Disposition'] = f'attachment; filename="{bank_name}_form.pdf"'
        return response
    
    


class GroupMemberShipFormView(View):
    def get(self, request):
        return render(request, 'borrower_registration_form.html')

    def post(self, request):
        group_no = request.POST.get('group_no')
        try:
            group = Group.objects.get(group_no=group_no)
        except Group.DoesNotExist:
            return render(request, 'borrower_registration_form.html', {'error_message': f'Group with Group Number "{group_no}" not found.'})

        report_data = {
            'group_details': {
                'Group Number': group.group_no,
                'Group Name': group.group_name,
            },
            'group': group.group_name,
            'phone_number': group.phone_number,
        }

        # Generate PDF
        pdf_generator = PDFGenerator(report_data)
        pdf_bytes = pdf_generator.generate_pdf()

        # Return the PDF file as a response
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{group.group_name}_form.pdf"'
        return response
