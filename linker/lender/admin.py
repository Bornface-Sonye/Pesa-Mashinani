from django.contrib import admin
from .models import (
    Constituency, Ward, SubLocation, Borrower, Entrepreneur,Company, Commission,
    CivilServant, Employee, Unemployed, Group, BorrowerGroup, Lender, Bank, GroupLender, Allocation, Application, 
    Disbursement, Payment, System_User, Guarantor, County, Account, GroupMember, Message, Defaulter, Loan
)

models_to_register = [
   Constituency, Ward, SubLocation, Borrower, Entrepreneur,Company, Commission,
   CivilServant, Employee, Unemployed, Group, BorrowerGroup, Lender, Bank, GroupLender, Allocation, Application, 
   Disbursement, Payment, System_User, Guarantor, County, Account, GroupMember, Message, Defaulter, Loan
    
]

i = 0
while True:
    admin.site.register(models_to_register[i])
    i += 1
    if i >= len(models_to_register):
        break
