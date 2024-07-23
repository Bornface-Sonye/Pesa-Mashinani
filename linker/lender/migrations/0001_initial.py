# Generated by Django 4.2.7 on 2024-07-22 17:16

from django.db import migrations, models
import django.db.models.deletion
import lender.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_no', models.DecimalField(decimal_places=0, help_text='Enter Account Number', max_digits=50, primary_key=True, serialize=False)),
                ('account_name', models.CharField(help_text='Enter Account Name', max_length=100)),
                ('account_bal', models.DecimalField(decimal_places=2, help_text='Enter Account Balance', max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('allocation_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('allocation_no', models.CharField(blank=True, help_text='Enter the Allocation Number', max_length=50, unique=True)),
                ('lender_no', models.CharField(help_text='Enter Lender Number:', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Enter Amount to Allocate', max_digits=15)),
                ('interest_rate', models.DecimalField(decimal_places=2, help_text='Enter Interest Rate', max_digits=15)),
                ('allocation_date', models.DateField(blank=True, help_text='Enter Date of Allocation')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('application_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('application_no', models.CharField(blank=True, help_text='Enter the Application Number', max_length=50, unique=True)),
                ('borrower_no', models.CharField(help_text='Enter Borrower Number:', max_length=100)),
                ('allocation_no', models.CharField(help_text='Enter the Allocation Number', max_length=50)),
                ('loan_amount', models.DecimalField(decimal_places=2, help_text='Enter Amount to Request', max_digits=15)),
                ('proposed_amount', models.DecimalField(decimal_places=2, help_text='Enter Amount Proposed', max_digits=15)),
                ('application_date', models.DateField(blank=True, help_text='Enter Date of Application')),
            ],
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('borrower_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('borrower_type', models.CharField(choices=[('entrepreneur', 'Entrepreneur'), ('civil_servant', 'Civil Servant'), ('employee', 'Employee'), ('unemployed', 'Unemployed'), ('group', 'Group')], max_length=20)),
                ('email_address', models.EmailField(help_text='Enter Email Address:', max_length=30, unique=True)),
                ('national_id', models.DecimalField(decimal_places=0, help_text='Enter National Identification Number:', max_digits=8, unique=True, validators=[lender.validators.validate_kenyan_id])),
                ('borrower_no', models.CharField(blank=True, help_text='Enter Borrower Number:', max_length=100)),
                ('username', models.CharField(blank=True, help_text='Enter Borrower Username', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_no', models.CharField(help_text='Enter Company Number', max_length=50, primary_key=True, serialize=False)),
                ('company_name', models.CharField(help_text='Enter Company Name', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('constituency_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('constituency_name', models.CharField(help_text='Enter Constituency Name', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('county_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('county_name', models.CharField(help_text='Enter County Name', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Defaulter',
            fields=[
                ('national_id', models.DecimalField(decimal_places=0, help_text='Enter National Identification Number:', max_digits=8, primary_key=True, serialize=False, unique=True, validators=[lender.validators.validate_kenyan_id])),
                ('lender_no', models.CharField(help_text='Enter Group Number', max_length=50, unique=True)),
                ('amount_owed', models.DecimalField(decimal_places=2, help_text='Enter Amount Owed', max_digits=15)),
                ('submission_date', models.DateField(blank=True, help_text='Enter Date of Submission')),
            ],
        ),
        migrations.CreateModel(
            name='Disbursement',
            fields=[
                ('disbursement_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('transaction_no', models.CharField(blank=True, help_text='Enter the Transaction Number', max_length=30, unique=True)),
                ('application_no', models.CharField(help_text='Enter the Application Number', max_length=50)),
                ('disbursed_amount', models.DecimalField(decimal_places=2, help_text='Enter Amount to Disburse', max_digits=15)),
                ('disbursement_date', models.DateField(help_text='Enter Date of Disbursement')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('member_no', models.CharField(help_text='Enter Member Number', max_length=50)),
                ('first_name', models.CharField(help_text='Enter First Name', max_length=50)),
                ('last_name', models.CharField(help_text='Enter Last Name', max_length=50)),
                ('national_id', models.DecimalField(decimal_places=0, help_text='Enter National Identification Number:', max_digits=20, unique=True, validators=[lender.validators.validate_kenyan_id])),
                ('phone_number', models.CharField(help_text='Enter phone number in the format 0798073204 or +254798073404', max_length=13, validators=[lender.validators.validate_kenyan_phone_number])),
                ('dob', models.DateField(help_text='Enter Date of Birth')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], help_text='Enter Member Gender', max_length=10)),
                ('group', models.CharField(help_text='Enter Group Number', max_length=50)),
                ('grp_worth', models.DecimalField(decimal_places=2, default=0.0, help_text='Enter Group Worth in Kshs.', max_digits=20)),
                ('account', models.CharField(default='00000000', help_text='Account Number', max_length=50)),
                ('approved', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', help_text='Is the member approved', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Lender',
            fields=[
                ('lender_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('lender_type', models.CharField(choices=[('bank', 'Bank'), ('group', 'Group')], max_length=20)),
                ('email_address', models.EmailField(help_text='Enter Email Address', max_length=50, unique=True)),
                ('lender_id_no', models.DecimalField(decimal_places=0, help_text='Enter Identification Number:', max_digits=8, unique=True, validators=[lender.validators.validate_lender_id])),
                ('lender_no', models.CharField(blank=True, help_text='Enter Lender Number:', max_length=100)),
                ('username', models.CharField(blank=True, help_text='Enter Username', max_length=50)),
                ('account_no', models.ForeignKey(help_text='Choose Account Number', on_delete=django.db.models.deletion.CASCADE, to='lender.account')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('payment_no', models.CharField(blank=True, help_text='Enter the Payment Number', max_length=30, unique=True)),
                ('transaction_no', models.CharField(help_text='Enter the Transaction Number', max_length=30)),
                ('principal', models.DecimalField(decimal_places=2, help_text='Enter Amount to Pay', max_digits=15)),
                ('principal_interest', models.DecimalField(decimal_places=2, help_text='Total Amount', max_digits=15)),
                ('amount_paid', models.DecimalField(decimal_places=2, help_text='Total Paid', max_digits=15)),
                ('balance', models.DecimalField(decimal_places=2, help_text='Balance', max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('message_no', models.CharField(help_text='Enter Message Number', max_length=50)),
                ('sender_usename', models.CharField(help_text='Enter Sender Username', max_length=50)),
                ('recipient_username', models.CharField(help_text='Enter Recipient Username', max_length=50)),
                ('message_name', models.CharField(help_text='Enter Message Name', max_length=50)),
                ('message_description', models.CharField(help_text='Enter Message Description', max_length=50)),
                ('message_date', models.DateField(help_text='Enter Date Sent')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('payment_no', models.CharField(blank=True, help_text='Enter the Payment Number', max_length=30, unique=True)),
                ('transaction_no', models.CharField(help_text='Enter the Transaction Number', max_length=30)),
                ('payment_amount', models.DecimalField(decimal_places=2, help_text='Enter Amount to Pay', max_digits=15)),
                ('payment_date', models.DateField(help_text='Enter Date of Disbursement')),
            ],
        ),
        migrations.CreateModel(
            name='System_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrower_no', models.CharField(blank=True, help_text='Enter Borrower Number/System-Generated:', max_length=100)),
                ('lender_no', models.CharField(blank=True, help_text='Enter Lender Number/System-Generated:', max_length=100)),
                ('username', models.EmailField(help_text='Enter a valid Username', max_length=50, unique=True)),
                ('password_hash', models.CharField(help_text='Enter a valid password', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('borrower_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lender.borrower')),
                ('group_no', models.CharField(help_text='Enter Group Number', max_length=50, unique=True)),
                ('group_name', models.CharField(help_text='Enter Group Name', max_length=100)),
                ('phone_number', models.CharField(help_text='Enter phone number in the format 0798073204 or +254798073404', max_length=13, validators=[lender.validators.validate_kenyan_phone_number])),
                ('account', models.ForeignKey(help_text='Account Number', on_delete=django.db.models.deletion.CASCADE, to='lender.account')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('ward_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('ward_name', models.CharField(help_text='Enter Ward Name', max_length=100)),
                ('constituency', models.ForeignKey(help_text='Choose the Constituency Name', on_delete=django.db.models.deletion.CASCADE, to='lender.constituency')),
            ],
        ),
        migrations.CreateModel(
            name='SubLocation',
            fields=[
                ('sublocation_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('sublocation_name', models.CharField(help_text='Enter Sub Location Name', max_length=100)),
                ('ward', models.ForeignKey(help_text='Choose the Ward', on_delete=django.db.models.deletion.CASCADE, to='lender.ward')),
            ],
        ),
        migrations.CreateModel(
            name='Guarantor',
            fields=[
                ('guarantor_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('national_id', models.DecimalField(decimal_places=0, help_text='Enter National Identification Number:', max_digits=8, unique=True, validators=[lender.validators.validate_kenyan_id])),
                ('email_address', models.EmailField(help_text='Enter Email Address', max_length=50, unique=True)),
                ('guarantor_first_name', models.CharField(help_text='Enter First Name', max_length=30)),
                ('guarantor_last_name', models.CharField(help_text='Enter Last Name', max_length=30)),
                ('phone_number', models.CharField(help_text='Enter phone number in the format 0798073204 or +254798073404', max_length=13, validators=[lender.validators.validate_kenyan_phone_number])),
                ('dob', models.DateField(help_text='Enter Date of Birth')),
                ('occupation', models.CharField(help_text='Enter Occupation', max_length=100)),
                ('account_no', models.ForeignKey(help_text='Choose Account Number', on_delete=django.db.models.deletion.CASCADE, to='lender.account')),
                ('ward', models.ForeignKey(help_text='Choose the Ward', on_delete=django.db.models.deletion.CASCADE, to='lender.ward')),
            ],
        ),
        migrations.CreateModel(
            name='Entrepreneur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrepreneur_no', models.CharField(help_text='Enter Entrepreneur Number:', max_length=50)),
                ('borrower_no', models.OneToOneField(help_text='Choose Borrower Number', on_delete=django.db.models.deletion.CASCADE, to='lender.borrower')),
                ('company_no', models.ForeignKey(help_text='Choose Company Number', on_delete=django.db.models.deletion.CASCADE, to='lender.company')),
            ],
        ),
        migrations.AddField(
            model_name='constituency',
            name='county',
            field=models.ForeignKey(help_text='Choose the County Name', on_delete=django.db.models.deletion.CASCADE, to='lender.county'),
        ),
        migrations.AddField(
            model_name='company',
            name='constituency',
            field=models.ForeignKey(help_text='Choose the Constituency Name', on_delete=django.db.models.deletion.CASCADE, to='lender.constituency'),
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('commission_no', models.CharField(help_text='Enter Commission Number', max_length=50, primary_key=True, serialize=False)),
                ('commission_name', models.CharField(help_text='Enter Commission Name', max_length=100)),
                ('constituency', models.ForeignKey(help_text='Choose the Constituency Name', on_delete=django.db.models.deletion.CASCADE, to='lender.constituency')),
            ],
        ),
        migrations.CreateModel(
            name='Unemployed',
            fields=[
                ('borrower_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lender.borrower')),
                ('guarantor', models.ForeignKey(help_text='Choose the Guarantor', on_delete=django.db.models.deletion.CASCADE, to='lender.guarantor')),
            ],
        ),
        migrations.CreateModel(
            name='GroupLender',
            fields=[
                ('lender_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lender.lender')),
                ('group_no', models.ForeignKey(help_text='Choose the Group', on_delete=django.db.models.deletion.CASCADE, to='lender.group')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='guarantor',
            field=models.ForeignKey(help_text='Choose the Guarantor', on_delete=django.db.models.deletion.CASCADE, to='lender.guarantor'),
        ),
        migrations.AddField(
            model_name='group',
            name='ward',
            field=models.ForeignKey(help_text='Choose Ward of Operation', on_delete=django.db.models.deletion.CASCADE, to='lender.ward'),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('borrower_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lender.borrower')),
                ('employee_no', models.CharField(help_text='Enter Employee Number', max_length=50)),
                ('company_no', models.ForeignKey(help_text='Choose Company Number', on_delete=django.db.models.deletion.CASCADE, to='lender.company')),
            ],
        ),
        migrations.CreateModel(
            name='CivilServant',
            fields=[
                ('borrower_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lender.borrower')),
                ('civil_servant_no', models.CharField(help_text='Enter Servant Number', max_length=50)),
                ('commission_no', models.ForeignKey(help_text='Choose Commission Number', on_delete=django.db.models.deletion.CASCADE, to='lender.commission')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowerGroup',
            fields=[
                ('borrower_group_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('borrower_no', models.ForeignKey(help_text='Choose the Borrower Number', on_delete=django.db.models.deletion.CASCADE, to='lender.borrower')),
                ('group_no', models.ForeignKey(help_text='Choose the Group Number', on_delete=django.db.models.deletion.CASCADE, to='lender.group')),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('lender_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lender.lender')),
                ('bank_name', models.CharField(help_text='Enter Bank Name', max_length=50, unique=True)),
                ('phone_number', models.CharField(help_text='Enter phone number in the format 0798073204 or +254798073404', max_length=13, validators=[lender.validators.validate_kenyan_phone_number])),
                ('bank_no', models.CharField(help_text='Enter Bank Number', max_length=50, unique=True)),
                ('constituency', models.ForeignKey(help_text='Choose the Constituency', on_delete=django.db.models.deletion.CASCADE, to='lender.constituency')),
            ],
        ),
    ]
