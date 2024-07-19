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
    Application, Disbursement, Payment, Guarantor, County, Account, GroupMember, Message, Defaulter
)


from .forms import BorrowerForm, EntrepreneurForm, CivilServantForm, EmployeeForm, UnemployedForm, GroupForm
from .forms import AllocationForm, PaymentForm, ApplicationForm, DisbursementForm, GroupMemberForm
from .forms import LenderForm, BankForm, GroupLenderForm, BorrowerSignUpForm, BankSignUpForm
from .forms import GroupSignUpForm, LoginForm, BorrowerGroupForm, UserForm

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
    
     


from django.views.generic import TemplateView

class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['username']  # Access username from self.kwargs
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


from django.shortcuts import render, redirect
from django.views import View
from .forms import BorrowerForm
from .models import GroupMember
from datetime import datetime
from .utils import generate_borrower_username, generate_unique_borrower_number

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
            dor = datetime.now()  # Get current date and time
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
            borrower.dor = dor
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

from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from .forms import LenderForm
from .models import Lender, Account

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
            dor = datetime.now()
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




from django.shortcuts import render, redirect
from django.views import View
from .forms import GroupMemberForm
from .models import System_User, Borrower, Group, GroupMember
import random
import string

class AddGroupMemberView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('group_login')  # Redirect to login if username is not in session

        try:
            # Fetch the user and related details (borrower_no, lender_no, etc.)
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
            borrower = Borrower.objects.get(borrower_no=borrower_no)
            # Fetch the group object using borrower_no
            group = Group.objects.get(borrower_no=borrower)
        except System_User.DoesNotExist:
            return redirect('group_login')
        except Borrower.DoesNotExist:
            return redirect('group_login')
        except Group.DoesNotExist:
            return redirect('group_login')

        # Store necessary session data
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
        try:
            # Fetch the user and related details (borrower_no, lender_no, etc.)
            user = System_User.objects.get(username=username)
            borrower_no = user.borrower_no
            borrower = Borrower.objects.get(borrower_no=borrower_no)
            # Fetch the group object using borrower_no
            group = Group.objects.get(borrower_no=borrower)
        except System_User.DoesNotExist:
            return redirect('group_login')
        except Borrower.DoesNotExist:
            return redirect('group_login')
        except Group.DoesNotExist:
            return redirect('group_login')

        if form.is_valid():
            try:
                # Save the form data to database
                group_member = form.save(commit=False)
                member_no = self.generate_unique_member_number()
                group_member.member_no = member_no                
                group_member.group = group  # Assuming group is the correct Group object
                group_member.save()
                # On success, pass the member_no to the template
                return render(request, 'add_group_member.html', {
                    'form': GroupMemberForm(),
                    'member_no': member_no
                })
            except Exception as e:
                # On error, pass the error_member_no to the template
                return render(request, 'add_group_member.html', {
                    'form': form,
                    'error_member_no': member_no
                })

        # If form is not valid, render the form again with errors
        return render(request, 'add_group_member.html', {'form': form})

    def generate_unique_member_number(self):
        # Generate a unique member number, e.g., using a similar approach to generate_message_no
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            member_no = letters + digits
            if not GroupMember.objects.filter(member_no=member_no).exists():
                return member_no





from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import System_User, Group, GroupMember

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
    fields = ['member_no', 'first_name', 'last_name', 'national_id', 'phone_no', 'dob', 'gender', 'group', 'grp_worth', 'account', 'approved']
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
            submission_date = datetime.now()  # Get current date and time
            
            if Defaulter.objects.filter(national_id=national_id).exists():
                return render(request, self.template_name, {
                    'form': form,
                    'error_national_id': national_id,
                    'error_message': 'Defaulter already exists. Please try again.'
                })
            defaulters = form.save(commit=False)
            allocation.allocation_no = allocation_no  # Assign the generated allocation number
            defaulters.allocation_date = allocation_date  # Assign current date and time
            defaulters.lender_no = lender_no  # Assign lender_no from session
            defaulters.save()

            return render(request, self.template_name, {
                'form': DefaulterForm(),
                'national_id': national_id,
                'success_message': f'Defaulter added successfully.'
            })

        else:
            # If the form is not valid, return the template with the form
            return render(request, self.template_name, {'form': form})

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
            return redirect('bank_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

        form = AllocationForm(request.POST)

        if form.is_valid():
            allocation_no = unique_allocation_number()
            amount = form.cleaned_data['amount']
            allocation_date = datetime.now()  # Get current date and time

            # Check if the allocation number already exists
            if Allocation.objects.filter(allocation_no=allocation_no).exists():
                return render(request, self.template_name, {
                    'form': form,
                    'error_allocation_no': allocation_no,
                    'error_message': 'Allocation number already exists. Please try again.'
                })

            allocation = form.save(commit=False)
            allocation.allocation_no = allocation_no  # Assign the generated allocation number
            allocation.allocation_date = allocation_date  # Assign current date and time
            allocation.lender_no = lender_no  # Assign lender_no from session
            allocation.save()

            return render(request, self.template_name, {
                'form': AllocationForm(),
                'allocation_no': allocation_no,
                'success_message': f'Allocation successful. Allocation Number: {allocation_no}'
            })

        else:
            # If the form is not valid, return the template with the form
            return render(request, self.template_name, {'form': form})
        
class GroupAllocationView(View):
    template_name = 'group_allocation.html'

    def get(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('group_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

        form = AllocationForm(initial={'lender_no': lender_no})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        lender_no = request.session.get('lender_no')
        if not lender_no:
            return redirect('group_dashboard')  # Redirect to the bank dashboard if lender_no is not in session

        form = AllocationForm(request.POST)

        if form.is_valid():
            allocation_no = unique_allocation_number()
            amount = form.cleaned_data['amount']
            allocation_date = datetime.now()  # Get current date and time

            # Check if the allocation number already exists
            if Allocation.objects.filter(allocation_no=allocation_no).exists():
                return render(request, self.template_name, {
                    'form': form,
                    'error_allocation_no': allocation_no,
                    'error_message': 'Allocation number already exists. Please try again.'
                })

            allocation = form.save(commit=False)
            allocation.allocation_no = allocation_no  # Assign the generated allocation number
            allocation.allocation_date = allocation_date  # Assign current date and time
            allocation.lender_no = lender_no  # Assign lender_no from session
            allocation.save()

            return render(request, self.template_name, {
                'form': AllocationForm(),
                'allocation_no': allocation_no,
                'success_message': f'Allocation successful. Allocation Number: {allocation_no}'
            })

        else:
            # If the form is not valid, return the template with the form
            return render(request, self.template_name, {'form': form})
        
class AllocationsView(ListView):
    model = Allocation
    template_name = 'allocations_list.html'
    context_object_name = 'allocations'


class GroupAllocationsView(ListView):
    model = Allocation
    template_name = 'grp_allocations_list.html'
    context_object_name = 'allocations'        


from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from .forms import ApplicationForm
from .models import GroupMember, Group, Borrower, Allocation, Account, GroupLender
from django.urls import reverse_lazy
from datetime import datetime

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
            'application_no': unique_application_number(),
            'application_date': datetime.now().date(),
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
        try:
            borrower = Borrower.objects.get(borrower_no=borrower_no)
        except Borrower.DoesNotExist:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'Borrower with number {borrower_no} does not exist.'
            })
        
        # Fetch GroupMember related to the borrower's national_id
        try:
            group_member = GroupMember.objects.get(national_id=borrower.national_id)
        except GroupMember.DoesNotExist:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'Group member with national ID {borrower.national_id} does not exist.'
            })
        
        group_no = group_member.group
        member_count = GroupMember.objects.filter(group=group_no).count()

        # Fetch Group object related to group_no
        try:
            group = Group.objects.get(group_no=group_no)
        except Group.DoesNotExist:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'Group with number {group_no} does not exist.'
            })

        # Fetch Account object related to group's account
        try:
            account = Account.objects.get(account_no=group.account.account_no)
        except Account.DoesNotExist:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'Account with number {group.account.account_no} does not exist.'
            })
        
        grp_worth = account.account_bal
        
        # Additional logic you have in your form_valid method
        age = group_member.calculate_age()
        gender = group_member.gender
        membgrp_worth = group_member.grp_worth
        
        # Check if the member is approved
        if group_member.approved != GroupMember.YES:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'This group member is not approved for a loan.'
            })
        
        # Assign account balance to member_balance
        member_balance = account.account_bal
        
        # Fetch GroupLender object based on group_no
        try:
            group_lender = GroupLender.objects.get(group_no=group_member.group)
        except GroupLender.DoesNotExist:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'Group lender for group {group_member.group} does not exist.'
            })
        
        # Fetch Allocation count for the lender_no in Allocation table
        allocation_count = Allocation.objects.filter(lender_no=group_lender.lender_no.lender_no).count()
        
        # Additional variables for your MachineLearningModel and LoanProposal
        group_transactions = allocation_count
        loan_amount = form.cleaned_data['loan_amount']
        (self, name, age, gender, worth, grp_population, grp_worth, memb_grp_worth, grp_transactions, requested_amt)
        ml_model = MachineLearningModel()
        loan_proposal = LoanProposal()
        loan_proposal.data_retrieval('Mary', age, gender,member_balance, member_count, grp_worth, membgrp_worth, group_transactions, loan_amount)
        prediction_result = loan_proposal.data_preparation()
        result = f"{float(prediction_result):.2f}"

        form.instance.allocation_no = allocation_no
        form.instance.application_no = application_no
        form.instance.application_date = datetime.now().date()
        form.instance.proposed_amount = result
        form.instance.borrower_no = borrower_no
        
        # Check if application number already exists
        if Application.objects.filter(application_no=application_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': 'Application number already exists. Please try again.'
            })
        
        # Save the form instance
        form.save()
        
        return render(self.request, self.template_name, {
            'form': ApplicationForm(),
            'allocation_no': allocation_no,
            'application_no': application_no,
            'success_message': f'Application successful. Application Number: {form.instance.application_no}'
        })

    def form_invalid(self, form):
        allocation_no = self.kwargs['allocation_no']
        return render(self.request, self.template_name, {
            'form': form,
            'allocation_no': allocation_no,
            'error_message': 'There was an error with your application. Please correct the errors.'
        })


        

class GroupApplicationView(FormView):
    form_class = ApplicationForm
    template_name = 'application.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        allocation_no = self.kwargs['allocation_no']
        
        borrower_no = self.request.session.get('borrower_no', None)
        
        # Add borrower_no to initial form data
        kwargs['initial'] = {
            'allocation_no': allocation_no,
            'application_no': unique_application_number(),
            'application_date': datetime.now().date(),
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
        
        # Retrieve the group based on borrower_no
        group = get_object_or_404(Group, borrower_no=borrower_no)
        
        # Retrieve the account related to the group
        #account = get_object_or_404(Account, account=account)
        account = group.account
        
        # Calculate 40% of the account balance
        account_balance = account.account_bal
        max_loan_amount = account_balance * 0.4
        
        loan_amount = form.cleaned_data['loan_amount']
        
        # Determine proposed_amount
        if loan_amount > max_loan_amount:
            proposed_amount = max_loan_amount
        else:
            proposed_amount = loan_amount
        
        # Save the application
        form.instance.allocation_no = allocation_no
        form.instance.application_no = application_no
        form.instance.application_date = datetime.now().date()
        form.instance.proposed_amount = proposed_amount
        form.instance.borrower_no = borrower_no
        
        if Application.objects.filter(application_no=application_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_application_no': application_no,
                'error_message': 'Application number already exists. Please try again.'
            })

        form.save()
        return render(self.request, self.template_name, {
            'form': ApplicationForm(),
            'allocation_no': allocation_no,
            'application_no': application_no,
            'success_message': f'Application successful. Application Number: {form.instance.application_no}'
        })
        
    def form_invalid(self, form):
        allocation_no = self.kwargs['allocation_no']
        return render(self.request, self.template_name, {
            'form': form,
            'allocation_no': allocation_no,
            'error_message': 'There was an error with your application. Please correct the errors.'
        })



    
class RequestsView(ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'applications' 
 
 

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
        
        # Get the proposed amount from the Application table
        application = get_object_or_404(Application, application_no=application_no)
        proposed_amount = application.proposed_amount
        
        # Check if the entered amount is valid
        entered_amount = form.cleaned_data.get('disbursed_amount')
        if entered_amount > proposed_amount:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'transaction_no': transaction_no,
                'error_message': 'Disbursed amount cannot be greater than Proposed amount.'
            })
        
        # Save the disbursement if everything is valid
        form.instance.application_no = application_no
        form.instance.transaction_no = transaction_no
        form.instance.disbursement_date = datetime.now().date()

        if Disbursement.objects.filter(transaction_no=transaction_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': transaction_no,
                'error_message': 'Transaction number already exists. Please try again.'
            })

        form.save()
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

 
          
from django.shortcuts import render, redirect
from django.views import View
from .models import Allocation, Application, Disbursement, Payment

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

        return render(request, 'transactions.html', {'disbursements': disbursements, 'payments': payments})

    

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
        context['transaction_no'] = self.kwargs['transaction_no']
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        transaction_no = self.kwargs['transaction_no']
        payment_no = unique_payment_number()
        form.instance.transaction_no = transaction_no
        form.instance.payment_no = payment_no
        form.instance.payment_date = datetime.now().date()

        if Payment.objects.filter(payment_no=payment_no).exists():
            return render(self.request, self.template_name, {
                'form': form,
                'transaction_no': transaction_no,
                'error_payment_no': payment_no,
                'error_message': 'Payment number already exists. Please try again.'
            })

        form.save()
        return render(self.request, self.template_name, {
            'form': PaymentForm(),
            'transaction_no': transaction_no,
            'payment_no': payment_no,
            'success_message': f'Payment successful. Payment Number: {form.instance.payment_no}'
        })

    def form_invalid(self, form):
        transaction_no = self.kwargs['transaction_no']
        return render(self.request, self.template_name, {
            'form': form,
            'transaction_no': transaction_no,
            'payment_no': form.cleaned_data.get('payment_no', None),
            'error_message': 'There was an error with your payment. Please correct the errors.'
        })
        