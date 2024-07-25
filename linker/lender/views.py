from .utils import *
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from .models import System_User
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import GroupMember
from django.shortcuts import render, redirect
from django.views import View
from .models import Borrower
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Disbursement, Payment
from django.urls import reverse_lazy
from .forms import ApplicationForm
from .models import Application
from django import forms
from django.db import models
from django.db.models import Sum

from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Borrower, Application, GroupMember, Group, Account, Allocation, Lender, GroupLender, Message
from .forms import ApplicationForm
import random
import string
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from datetime import datetime
from .models import Disbursement, Application
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Application, Allocation, Account, Borrower, Lender, Group, Message, Disbursement
from .forms import DisbursementForm
from django.db.models import DecimalField
from django.core.exceptions import ValidationError
import random
import string

from django.shortcuts import redirect, render
from django.views import View
from .models import GroupMember, System_User, Borrower, Group, Defaulter
from .forms import GroupMemberForm
from .utils import generate_unique_member_number  # Ensure this utility function is defined

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.utils import timezone
from django.db.models import Sum
import random
import string

from .models import Application, Allocation, Borrower, Group, Lender, Message
from .forms import ApplicationForm


from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from .forms import ApplicationForm
from .models import GroupMember, Group, Borrower, Allocation, Account, GroupLender
from django.urls import reverse_lazy
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ApplicationForm
from .models import Allocation, Application, Borrower, GroupMember, Group, Account, GroupLender
from datetime import datetime
import random
from django.views.generic import TemplateView
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Defaulter
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Defaulter
from .forms import DefaulterUpdateForm

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
from django.shortcuts import render, redirect,get_object_or_404
from tabulate import tabulate
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph

from django.shortcuts import render, redirect
from django.views import View
from .forms import BorrowerForm
from .models import GroupMember
from datetime import datetime
from .utils import generate_borrower_username, generate_unique_borrower_number


import random
import string
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from .models import System_User, Message, GroupMember  # Ensure to import the relevant models
from .forms import GroupMemberForm  # Ensure to import the relevant forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .models import GroupMember

from django.views.generic import CreateView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import (
    Constituency, Ward, SubLocation, Borrower, Entrepreneur,Company, Commission,
    CivilServant, Employee, Unemployed, Group, BorrowerGroup, Lender, Bank, GroupLender, Allocation, System_User,
    Application, Disbursement, Payment, Guarantor, County, Account, GroupMember, Message, Defaulter, Loan
)


from .forms import BorrowerForm, EntrepreneurForm, CivilServantForm, EmployeeForm, UnemployedForm, GroupForm
from .forms import AllocationForm, PaymentForm, ApplicationForm, DisbursementForm, GroupMemberForm
from .forms import LenderForm, BankForm, GroupLenderForm, BorrowerSignUpForm, BankSignUpForm
from .forms import GroupSignUpForm, LoginForm, BorrowerGroupForm, UserForm, DefaulterForm,  DefaulterUpdateForm
   

def grouplogout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('home')  # Redirect to home page after logout
    return render(request, 'group.html') 
 
def borrowerlogout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('home')  # Redirect to home page after logout
    return render(request, 'borrower.html') 

def banklogout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('home')  # Redirect to home page after logout
    return render(request, 'bank.html') 

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
            return redirect('bank_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

        form = DefaulterForm(initial={'lender_no': lender_no})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

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
            return redirect('bank_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

        defaulter = get_object_or_404(Defaulter, pk=pk)
        if defaulter.lender_no != lender_no:
            messages.error(request, 'You have no privilege to update the details of this defaulter.')
            return redirect('defaulter_list')  # Redirect to the defaulter list if lender_no does not match

        form = DefaulterUpdateForm(instance=defaulter)
        return render(request, self.template_name, {'form': form, 'defaulter': defaulter})

    def post(self, request, pk):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('bank_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

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
            return redirect('bank_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

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
            return redirect('bank_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

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
                return redirect('bank_dashboard')
            except Account.DoesNotExist:
                return redirect('bank_dashboard')

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
            return redirect('group_dashboard')

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
                return redirect('group_dashboard')

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
        
        if Loan.objects.filter(borrower_no=borrower_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': transaction_no,
                'error_message': 'You already have unsettled loan, Please settle you Loan First !'
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
        if Loan.objects.filter(borrower_no=borrower_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': transaction_no,
                'error_message': 'You already have unsettled loan, Please settle you Loan First !'
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
            
            # Get applications related to these allocations
            return Application.objects.filter(allocation_no__in=allocation_numbers)
        else:
            # If lender_no is not in the session, handle according to your application needs
            # For example, return an empty queryset or handle the case appropriately
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
        #borrower = Borrower.objects.get(borrower_no=borrower_no)
        borrower = get_object_or_404(Borrower, borrower_no=borrower_no)
        # Get the proposed amount from the Application table
        proposed_amount = application.proposed_amount
        
        # Check if the entered amount is valid
        entered_amount = form.cleaned_data.get('disbursed_amount')
        if entered_amount > proposed_amount:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'transaction_no': transaction_no,
                'error_message': 'Entered amount cannot be greater than proposed amount.'
            })
            
        borrower_id = borrower.national_id
        member_account =get_object_or_404(GroupMember, national_id=borrower_id)
        #group = get_object_or_404(Group, borrower_no=borrower)

        borrower_account = Account.objects.get(account_no=member_account.account)
        #lender_account = get_object_or_404(Account, account_no=lender.account_no.account_no)
        
        #lender_account = Account.objects.get(account_no=lender.account_no)
        lender_account = get_object_or_404(Account, account_no=lender.account_no.account_no)
        # Check if the lender's account has sufficient balance
        if lender_account.account_bal < entered_amount:
                return render(request, self.template_name, {
                    'form': form,
                    'application_no': application_no,
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
        form.instance.disbursement_date = datetime.now().date()

        form.save()
        
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
            borrower_no = borrower_no,
            lender_no = lender_no
            principal = disbursed_amount
            loan_interest = allocation.interest_rate
            principal_interest = disbursed_amount
            amount_paid = 0,
            balance = disbursed_amount,
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
            'transaction_no': form.cleaned_data.get('transaction_no', None),
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
            return self.render_error(form, application_no, transaction_no, 'Entered amount cannot be greater than proposed amount.')

        # Get the group and its associated account
        group = get_object_or_404(Group, borrower_no=borrower)
        borrower_account = get_object_or_404(Account, account_no=group.account.account_no)

        # Get lender's account using the lender's account number
        lender_account = get_object_or_404(Account, account_no=lender.account_no.account_no)

        # Check if the lender's account has sufficient balance
        if lender_account.account_bal < entered_amount:
            return self.render_error(form, application_no, transaction_no, f'Insufficient account balance. Current balance is {lender_account.account_bal}.')

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
        form.instance.disbursement_date = timezone.now().date()

        form.save()

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
            borrower_no = borrower_no,
            lender_no = lender_no
            principal = disbursed_amount
            loan_interest = allocation.interest_rate
            principal_interest = disbursed_amount
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

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no


class TransactionsView(View):
    def get(self, request):
        lender_no = request.session.get('lender_no')
        borrower_no = request.session.get('borrower_no')

        if not lender_no or not borrower_no:
            return redirect('group_login')  # Redirect if lender number or borrower number is not in session

        try:
            # Filter allocations for the current lender number
            allocations = Allocation.objects.filter(lender_no=lender_no)

            # Get application numbers related to the allocations
            application_numbers = [allocation.allocation_no for allocation in allocations]

            # Filter applications for the current borrower number and related allocation numbers
            applications = Application.objects.filter(borrower_no=borrower_no, allocation_no__in=application_numbers)

            # Get application numbers related to the applications
            application_numbers = [application.application_no for application in applications]

            # Filter disbursements related to the current application numbers
            disbursements = Disbursement.objects.filter(application_no__in=application_numbers)

            # Filter payments related to the current application numbers
            payments = Payment.objects.filter(transaction_no__in=application_numbers)

        except Allocation.DoesNotExist:
            allocations = []

        except Application.DoesNotExist:
            applications = []
            disbursements = []
            payments = []

        return render(self.request, 'transactions.html', {'disbursements': disbursements, 'payments': payments})

    

class PaymentView(FormView):
    form_class = PaymentForm
    template_name = 'payment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        transaction_no = self.kwargs['transaction_no']
        kwargs['initial'] = {
            'transaction_no': transaction_no,
            'payment_no': unique_payment_number(),
            'payment_date': datetime.now().date()
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_no = self.kwargs['transaction_no']
        loan = get_object_or_404(Loans, transaction_no=transaction_no)
        context['transaction_no'] = transaction_no
        context['remaining_balance'] = loan.balance
        context['total_amount'] = loan.principal_interest
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        transaction_no = self.kwargs['transaction_no']
        payment_no = unique_payment_number()
        payment_amount = form.cleaned_data['payment_amount']

        # Retrieve the loan based on transaction_no
        loan = get_object_or_404(Loans, transaction_no=transaction_no)

        # Check if payment amount exceeds the balance
        if payment_amount > loan.balance:
            return render(self.request, self.template_name, {
                'form': form,
                'transaction_no': transaction_no,
                'error_payment_no': payment_no,
                'error_message': f'Payment amount exceeds the remaining balance of {loan.balance}. Please enter a valid amount.',
                'remaining_balance': loan.balance,
                'total_amount': loan.principal_interest
            })

        # Update the loan balance
        loan.amount_paid += payment_amount
        loan.balance -= payment_amount
        loan.save()

        # Retrieve borrower based on loan
        borrower_no = loan.borrower_no
        borrower = get_object_or_404(Borrower, borrower_no=borrower_no)
        
        # Retrieve lender based on loan allocation
        allocation = get_object_or_404(Allocation, allocation_no=loan.allocation_no)
        lender = get_object_or_404(Lender, lender_no=allocation.lender_no)

        # Update the lender's account balance
        lender_account = lender.account_no
        lender_account.account_bal += payment_amount
        lender_account.save()

        # Update the borrower's account balance
        borrower_account = borrower.account_no
        borrower_account.account_bal -= payment_amount
        borrower_account.save()

        # Save the payment
        form.instance.transaction_no = transaction_no
        form.instance.payment_no = payment_no
        form.instance.payment_date = datetime.now().date()

        if Payment.objects.filter(payment_no=payment_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'transaction_no': transaction_no,
                'error_payment_no': payment_no,
                'error_message': 'Payment number already exists. Please try again.',
                'remaining_balance': loan.balance,
                'total_amount': loan.principal_interest
            })

        form.save()

        # Create and save the message
        message_no = self.generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=borrower.username,  # Borrower's username
            recipient_username=lender.username,  # Lender's username
            message_name='Payment Completed',
            message_description=f'Payment of amount {payment_amount} has been processed for Transaction Number {transaction_no}.',
            message_date=datetime.now().date()
        )
        message.save()

        # Check if payment completes the loan
        if loan.balance <= 0:
            return render(self.request, self.template_name, {
                'form': PaymentForm(),
                'transaction_no': transaction_no,
                'payment_no': payment_no,
                'success_message': f'Payment successful. Payment Number: {payment_no}. The loan has been fully repaid.',
                'remaining_balance': loan.balance,
                'total_amount': loan.principal_interest
            })

        return render(self.request, self.template_name, {
            'form': PaymentForm(),
            'transaction_no': transaction_no,
            'payment_no': payment_no,
            'success_message': f'Payment successful. Payment Number: {payment_no}. Remaining balance: {loan.balance}.',
            'remaining_balance': loan.balance,
            'total_amount': loan.principal_interest
        })

    def form_invalid(self, form):
        transaction_no = self.kwargs['transaction_no']
        loan = get_object_or_404(Loans, transaction_no=transaction_no)
        print(form.errors)  # Print form errors to console or log them for debugging
        return render(self.request, self.template_name, {
            'form': form,
            'transaction_no': transaction_no,
            'error_message': 'Form Invalid. Errors: {}'.format(form.errors),
            'remaining_balance': loan.balance,
            'total_amount': loan.principal_interest
        })

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no
            
            
class GroupPaymentView(FormView):
    form_class = PaymentForm
    template_name = 'payment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        transaction_no = self.kwargs['transaction_no']
        kwargs['initial'] = {
            'transaction_no': transaction_no,
            'payment_no': unique_payment_number(),
            'payment_date': datetime.now().date()
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_no = self.kwargs['transaction_no']
        loan = get_object_or_404(Loans, transaction_no=transaction_no)
        context['transaction_no'] = transaction_no
        context['remaining_balance'] = loan.balance
        context['total_amount'] = loan.principal_interest
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        transaction_no = self.kwargs['transaction_no']
        payment_no = unique_payment_number()
        payment_amount = form.cleaned_data['payment_amount']

        # Retrieve the loan based on transaction_no
        loan = get_object_or_404(Loans, transaction_no=transaction_no)

        # Check if payment amount exceeds the balance
        if payment_amount > loan.balance:
            return render(self.request, self.template_name, {
                'form': form,
                'transaction_no': transaction_no,
                'error_payment_no': payment_no,
                'error_message': f'Payment amount exceeds the remaining balance of {loan.balance}. Please enter a valid amount.',
                'remaining_balance': loan.balance,
                'total_amount': loan.principal_interest
            })

        # Update the loan balance
        loan.amount_paid += payment_amount
        loan.balance -= payment_amount
        loan.save()

        # Retrieve borrower based on loan
        borrower_no = loan.borrower_no
        borrower = get_object_or_404(Borrower, borrower_no=borrower_no)
        
        # Retrieve lender based on loan allocation
        allocation = get_object_or_404(Allocation, allocation_no=loan.allocation_no)
        lender = get_object_or_404(Lender, lender_no=allocation.lender_no)

        # Update the lender's account balance
        lender_account = lender.account_no
        lender_account.account_bal += payment_amount
        lender_account.save()

        # Update the borrower's account balance
        borrower_account = borrower.account_no
        borrower_account.account_bal -= payment_amount
        borrower_account.save()

        # Save the payment
        form.instance.transaction_no = transaction_no
        form.instance.payment_no = payment_no
        form.instance.payment_date = datetime.now().date()

        if Payment.objects.filter(payment_no=payment_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'transaction_no': transaction_no,
                'error_payment_no': payment_no,
                'error_message': 'Payment number already exists. Please try again.',
                'remaining_balance': loan.balance,
                'total_amount': loan.principal_interest
            })

        form.save()

        # Create and save the message
        message_no = self.generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=borrower.username,  # Borrower's username
            recipient_username=lender.username,  # Lender's username
            message_name='Payment Completed',
            message_description=f'Payment of amount {payment_amount} has been processed for Transaction Number {transaction_no}.',
            message_date=datetime.now().date()
        )
        message.save()

        # Check if payment completes the loan
        if loan.balance <= 0:
            return render(self.request, self.template_name, {
                'form': PaymentForm(),
                'transaction_no': transaction_no,
                'payment_no': payment_no,
                'success_message': f'Payment successful. Payment Number: {payment_no}. The loan has been fully repaid.',
                'remaining_balance': loan.balance,
                'total_amount': loan.principal_interest
            })

        return render(self.request, self.template_name, {
            'form': PaymentForm(),
            'transaction_no': transaction_no,
            'payment_no': payment_no,
            'success_message': f'Payment successful. Payment Number: {payment_no}. Remaining balance: {loan.balance}.',
            'remaining_balance': loan.balance,
            'total_amount': loan.principal_interest
        })

    def form_invalid(self, form):
        transaction_no = self.kwargs['transaction_no']
        loan = get_object_or_404(Loans, transaction_no=transaction_no)
        print(form.errors)  # Print form errors to console or log them for debugging
        return render(self.request, self.template_name, {
            'form': form,
            'transaction_no': transaction_no,
            'error_message': 'Form Invalid. Errors: {}'.format(form.errors),
            'remaining_balance': loan.balance,
            'total_amount': loan.principal_interest
        })

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no


class PaymentView(UpdateView):
    model = Loan
    fields = ['member_no', 'first_name', 'last_name', 'national_id', 'phone_number', 'dob', 'gender', 'group', 'grp_worth', 'account', 'approved']
    widgets = {
            'gender': forms.RadioSelect(choices=GroupMember.GENDER_CHOICES),
        }
    template_name = 'member_update_form.html'
    success_url = reverse_lazy('member_list')
    
    
class GroupPaymentView(UpdateView):
    model = Loan
    fields = ['member_no', 'first_name', 'last_name', 'national_id', 'phone_number', 'dob', 'gender', 'group', 'grp_worth', 'account', 'approved']
    widgets = {
            'gender': forms.RadioSelect(choices=GroupMember.GENDER_CHOICES),
        }
    template_name = 'member_update_form.html'
    success_url = reverse_lazy('member_list')