from django.urls import path
from .views import (
    UserCreateView, BorrowerCreateView, EntrepreneurCreateView, CivilServantCreateView, EmployeeCreateView, UnemployedCreateView,
    GroupCreateView, LenderCreateView, BankCreateView, GroupLenderCreateView, HomePage_View, 
    Borrower_Dashboard_View, Group_Dashboard_View, Bank_Dashboard_View, grouplogout, banklogout, borrowerlogout,  BorrowerGroupCreateView, SuccessView, 
    AllocationView, RequestsView,  ApplicationView, DisbursementView,  Group_Dashboard_View, 
    AllocationsView, MemberListView, BankLoginView, GroupLoginView, BorrowerLoginView, BankSignUpView,
    BorrowerSignUpView, GroupSignUpView, AddGroupMemberView, MemberUpdateView, MemberDeleteView, AddGroupMemberView, 
    GroupAllocationView, GroupApplicationView, GroupAllocationsView, DefaultersView, DefaulterListView, DefaulterUpdateView, 
    DefaulterDeleteView, GroupDisbursementView, LoanPaymentView, GroupLoansView, BankLoansView, 
    BorrowerLoansView, GroupLoanPaymentView
)

urlpatterns = [
    path('', HomePage_View.as_view(), name='home'),
    path('register_user/', UserCreateView.as_view(), name='register_user'),
    path('register_borrower/', BorrowerCreateView.as_view(), name='register_borrower'),
    path('register_entrepreneur/<int:borrower_id>/<str:username>/', EntrepreneurCreateView.as_view(), name='register_entrepreneur'),
    path('register_civil_servant/<int:borrower_id>/<str:username>/', CivilServantCreateView.as_view(), name='register_civil_servant'),
    path('register_employee/<int:borrower_id>/<str:username>/', EmployeeCreateView.as_view(), name='register_employee'),
    path('register_unemployed/<int:borrower_id>/<str:username>/', UnemployedCreateView.as_view(), name='register_unemployed'),
    path('register_group/<int:borrower_id>/<str:username>/', GroupCreateView.as_view(), name='register_group'),
    path('register_lender/', LenderCreateView.as_view(), name='register_lender'),
    path('register_bank/<int:lender_id>/<str:username>/', BankCreateView.as_view(), name='register_bank'),
    path('register_group_lender/<int:lender_id>/<str:username>/', GroupLenderCreateView.as_view(), name='register_group_lender'),
    path('group/signup/', GroupSignUpView.as_view(), name='group_signup'),
    path('group/login/', GroupLoginView.as_view(), name='group_login'),
    path('borrower/signup/', BorrowerSignUpView.as_view(), name='borrower_signup'),
    path('borrower/login/', BorrowerLoginView.as_view(), name='borrower_login'),
    path('bank/signup/', BankSignUpView.as_view(), name='bank_signup'),
    path('bank/login/', BankLoginView.as_view(), name='bank_login'),
    path('borrower/', Borrower_Dashboard_View.as_view(), name='borrower'),
    path('group/', Group_Dashboard_View.as_view(), name='group'),
    path('bank/', Bank_Dashboard_View.as_view(), name='bank'),
    path('defaulters/', DefaulterListView.as_view(), name='defaulter_list'),
    path('defaulters/add/', DefaultersView.as_view(), name='add_defaulter'),
    path('defaulters/update/<int:pk>/', DefaulterUpdateView.as_view(), name='defaulter_update'),
    path('defaulters/delete/<int:pk>/', DefaulterDeleteView.as_view(), name='defaulter_delete'),
    path('group/logout/', grouplogout, name='grouplogout'),
    path('bank/logout/', banklogout, name='banklogout'),
    path('borrower/logout/', borrowerlogout, name='borrowerlogout'),
    path('success/<str:username>/', SuccessView.as_view(), name='success'),
    path('bank/allocation/', AllocationView.as_view(), name='bank_allocation'),
    #path('group/allocation/', GAllocationView.as_view(), name='group_allocation'),
    path('group/allocation/', GroupAllocationView.as_view(), name='group_allocation'),
    path('disbursement/<str:application_no>/', DisbursementView.as_view(), name='disbursement'),
    path('group_disbursement/<str:application_no>/', GroupDisbursementView.as_view(), name='group_disbursement'),
    path('application/<str:allocation_no>/', ApplicationView.as_view(), name='application'),
    path('grp_application/<str:allocation_no>/', GroupApplicationView.as_view(), name='grp_application'),
    path('allocations/', AllocationsView.as_view(), name='allocations_list'),
    path('grp_allocations/', GroupAllocationsView.as_view(), name='grp_allocations_list'),
    path('requests/', RequestsView.as_view(), name='requests_list'),
    path('group_payment/<str:transaction_no>/', GroupLoanPaymentView.as_view(), name='group_payment'),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('payment/<str:transaction_no>/', LoanPaymentView.as_view(), name='payment'),
    path('group_payment/<str:transaction_no>/', GroupLoanPaymentView.as_view(), name='group_payment'),
    path('members/update/<int:pk>/', MemberUpdateView.as_view(), name='update_member'),
    path('members/delete/<int:pk>/', MemberDeleteView.as_view(), name='delete_member'),
    path('add_member/', AddGroupMemberView.as_view(), name='add_group_member'),
    path('loans/', GroupLoansView.as_view(), name='loans'),
    path('bank_loans/', BankLoansView.as_view(), name='bank_loans'),
    path('borrower_loans/', BorrowerLoansView.as_view(), name='borrower_loans'),
]
