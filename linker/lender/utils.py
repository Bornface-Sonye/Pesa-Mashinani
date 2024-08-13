from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from decimal import Decimal


from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, lightgrey
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO


from .models import (
    Constituency, Ward, SubLocation, Borrower, Entrepreneur,Company, Commission,
    CivilServant, Employee, Unemployed, Group, BorrowerGroup, Lender, Bank, GroupLender, Allocation, System_User,
    Application, Disbursement, Payment, Guarantor, County, Account, GroupMember, Message, Defaulter, Loan
)


from .forms import BorrowerForm, EntrepreneurForm, CivilServantForm, EmployeeForm, UnemployedForm, GroupForm
from .forms import AllocationForm, PaymentForm, ApplicationForm, DisbursementForm, GroupMemberForm
from .forms import LenderForm, BankForm, GroupLenderForm, BorrowerGroupForm, UserForm, GuarantorForm



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


from .models import (
    Constituency, Ward, SubLocation, Borrower, Entrepreneur,Company, Commission,
    CivilServant, Employee, Unemployed, Group, BorrowerGroup, Lender, Bank, GroupLender, Allocation, System_User,
    Application, Disbursement, Payment, Guarantor, County, Account, GroupMember, Message, Defaulter
)


from .forms import BorrowerForm, EntrepreneurForm, CivilServantForm, EmployeeForm, UnemployedForm, GroupForm
from .forms import AllocationForm, PaymentForm, ApplicationForm, DisbursementForm, GroupMemberForm
from .forms import LenderForm, BankForm, GroupLenderForm, BorrowerSignUpForm, BankSignUpForm
from .forms import GroupSignUpForm, LoginForm, BorrowerGroupForm, UserForm

#Machine Learning imports;
import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from django.conf import settings

class MachineLearningModel:
    def __init__(self):
        self.new_data = None
        self.prediction = None
        self.training_features = None
        self.predictions = None
        self.model = None
        self.scaler = None
        self.actual_labels = None

        # Assuming the CSV file is named 'pesa.csv' and located in the same directory as this script
        self.file_path = os.path.join(settings.BASE_DIR, 'lender', 'pesa', 'pesa.csv')
        # self.file_path = 'pesa.csv'  # Adjust as per your actual path
        self.df = pd.read_csv(self.file_path)

        # Update feature names based on the new CSV structure
        self.feature_names = ['Age', 'Gender', 'Worth', 'GrpPopulation', 'GrpWorth', 'MembGrpWorth', 'GrpTransactions', 'RequestedAmt']
        self.training_features = self.df[self.feature_names].copy()  # Ensure to copy to avoid SettingWithCopyWarning

        # Outcome label is now ProposedAmt
        self.outcome_name = 'ProposedAmt'
        self.outcome_labels = self.df[self.outcome_name]

        # Define numeric and categorical feature names
        self.numeric_feature_names = ['Age', 'Worth', 'GrpPopulation', 'GrpWorth', 'MembGrpWorth', 'GrpTransactions', 'RequestedAmt']
        self.categorical_feature_names = ['Gender']

        # Standardize numeric features
        ss = StandardScaler()
        self.training_features.loc[:, self.numeric_feature_names] = ss.fit_transform(self.training_features.loc[:, self.numeric_feature_names])

        # Convert categorical features into dummy variables
        self.training_features = pd.get_dummies(self.training_features, columns=self.categorical_feature_names)

        # Store the scaler for later use
        self.scaler = ss

        # Train a linear regression model
        self.lr = LinearRegression()
        self.model = self.lr.fit(self.training_features, self.outcome_labels)

        # Store the model using joblib
        if not os.path.exists('Model'):
            os.mkdir('Model')
        joblib.dump(self.model, 'Model/model.pickle')
        joblib.dump(self.scaler, 'Model/scaler.pickle')

        # Predict on training data
        self.pred_labels = self.model.predict(self.training_features)
        self.actual_labels = self.outcome_labels

    def accuracy(self):
        mse = mean_squared_error(self.actual_labels, self.pred_labels)
        r2 = r2_score(self.actual_labels, self.pred_labels)

        return mse, r2

class LoanProposal:
    def __init__(self):
        self.new_data = None
        self.prediction = None
        self.training_features = None
        self.model = joblib.load('Model/model.pickle')
        self.scaler = joblib.load('Model/scaler.pickle')

        # Load the CSV file for data retrieval        
        self.file_path = os.path.join(settings.BASE_DIR, 'lender', 'pesa', 'pesa.csv')  # Adjust as per your actual path
        self.df = pd.read_csv(self.file_path)

        # Update feature names based on the new CSV structure
        self.feature_names = ['Name', 'Age', 'Gender', 'Worth', 'GrpPopulation', 'GrpWorth', 'MembGrpWorth', 'GrpTransactions', 'RequestedAmt']
        self.training_features = self.df[self.feature_names[1:]].copy()  # Ensure to copy to avoid SettingWithCopyWarning, excluding 'Name'
        self.outcome_name = 'ProposedAmt'

        # Numeric and categorical feature names
        self.numeric_feature_names = ['Age', 'Worth', 'GrpPopulation', 'GrpWorth', 'MembGrpWorth', 'GrpTransactions', 'RequestedAmt']
        self.categorical_feature_names = ['Gender']

        # Fit the scaler on the numeric features
        self.training_features.loc[:, self.numeric_feature_names] = self.scaler.transform(self.training_features.loc[:, self.numeric_feature_names])

        # Convert categorical features into dummy variables
        self.training_features = pd.get_dummies(self.training_features, columns=self.categorical_feature_names)

    def data_retrieval(self, name, age, gender, worth, grp_population, grp_worth, memb_grp_worth, grp_transactions, requested_amt):
        # Prepare new data for prediction
        self.new_data = pd.DataFrame({
            'Name': [name],
            'Age': [age],
            'Gender': [gender],
            'Worth': [worth],
            'GrpPopulation': [grp_population],
            'GrpWorth': [grp_worth],
            'MembGrpWorth': [memb_grp_worth],
            'GrpTransactions': [grp_transactions],
            'RequestedAmt': [requested_amt]
        })

    def data_preparation(self):
        # Transform and prepare new data for prediction
        self.prediction = self.new_data.copy()

        # Scale numeric features
        self.prediction.loc[:, self.numeric_feature_names] = self.scaler.transform(self.prediction.loc[:, self.numeric_feature_names])

        # Convert categorical features into dummy variables
        self.prediction = pd.get_dummies(self.prediction, columns=['Gender'])

        # Ensure all categorical features are aligned
        for feature in ['Gender_Male', 'Gender_Female']:  # Adjust as per your column names
            if feature not in self.prediction.columns:
                self.prediction[feature] = 0  # Add missing categorical feature columns with 0

        # Ensure the prediction data columns match the training data columns
        self.prediction = self.prediction[self.training_features.columns]

        # Make predictions using the loaded model
        self.predictions = self.model.predict(self.prediction)

        # Convert predictions to float to avoid Decimal issues
        self.predictions = np.array(self.predictions, dtype=float)

        # Clip predicted values to ensure they are within the desired range
        requested_amt = float(self.new_data['RequestedAmt'].iloc[0])
        self.predictions = np.clip(self.predictions, 0, requested_amt)

        # Round to the nearest 0.100
        self.predictions = np.round(self.predictions * 1) / 1

        # Return only the predicted ProposedAmt value formatted to two decimal places
        return float(f"{self.predictions[0]:.2f}")


class PDFGenerator:
    def __init__(self, report_data):
        self.report_data = report_data

    def generate_pdf(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Define custom styles
        custom_styles = self.create_custom_styles()

        # Add header
        header = self.create_header(custom_styles)
        elements.extend(header)  # Use extend to add multiple elements

        # Add form sections
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_one(elements, custom_styles)
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_two(elements, custom_styles)
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_three(elements, custom_styles)

        # Add decorative borders and watermark
        doc.build(elements, onFirstPage=self.add_decorations, onLaterPages=self.add_decorations)

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def create_custom_styles(self):
        # Define custom styles with attractive fonts and colors
        custom_styles = {
            'title': ParagraphStyle(
                'title',
                fontName='Helvetica-Bold',
                fontSize=18,
                textColor=HexColor('#003366'),  # Dark blue
                alignment=1,  # Center alignment
                spaceAfter=12,
            ),
            'header': ParagraphStyle(
                'header',
                fontName='Helvetica-Bold',
                fontSize=14,
                textColor=HexColor('#003366'),  # Dark blue text
                spaceAfter=6,
                spaceBefore=6,
                alignment=1,  # Center alignment
            ),
            'normal': ParagraphStyle(
                'normal',
                fontName='Helvetica',
                fontSize=12,
                textColor=HexColor('#333333'),  # Dark grey text
                spaceAfter=12,  # Add more space after
            ),
            'highlight': ParagraphStyle(
                'highlight',
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=HexColor('#003366'),  # Dark blue text
                spaceAfter=12,  # Add more space after
            ),
        }
        return custom_styles

    def create_header(self, styles):
        # Header with group information
        header_content = [
            Paragraph('PESA MASHINANI', styles['header']),
            Paragraph('Group Membership Registration Form', styles['header']),
            Spacer(1, 24),  # Add more space
            Spacer(1, 24),  # Add more space
        ]
        return header_content

    def add_section_one(self, elements, styles):
        section_title = Paragraph("Section I: Member Information", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph("First Name: <u>__________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Surname: <u>_____________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Sign: <u>________________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>________________________________________</u>", styles['highlight']))

    def add_section_two(self, elements, styles):
        section_title = Paragraph("Section II: For Group Use", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph(f"Group Name: <i>{self.report_data['group']}</i>", styles['highlight']))
        elements.append(Paragraph(f"Group Phone Number: <i>{self.report_data['phone_number']}</i>", styles['highlight']))
        elements.append(Paragraph("Chairman Name: <u>_______________________________</u>", styles['highlight']))
        elements.append(Paragraph("Chairman Sign: <u>_______________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>________________________________________</u>", styles['highlight']))
        # Ensure the stamp field has enough space
        elements.append(Spacer(1, 12))  # Add space before the stamp box
        elements.append(Paragraph(f"{self.report_data['group']} Official  Stamp:", styles['highlight']))
        elements.append(Spacer(1, 2))
        elements.append(StampBox())  # Add the custom stamp box flowable

    def add_section_three(self, elements, styles):
        section_title = Paragraph("Section III:For Mashinani Official Use", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph("Registrar Name: <u>______________________________</u>", styles['highlight']))
        elements.append(Paragraph("Sign: <u>________________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>________________________________________</u>", styles['highlight']))
        
        elements.append(Spacer(1, 8))
        elements.append(Paragraph("<b>Note:</b><i>Carry with you this form dully filled while coming for</i>", styles['highlight']))
        elements.append(Paragraph("<i>Registration</i>", styles['highlight']))

    def add_decorations(self, canvas, doc):
        # Add watermark
        canvas.saveState()
        canvas.setFont('Helvetica', 60)
        canvas.setStrokeColor(HexColor('#003366'))  # Dark blue
        canvas.setFillColor(lightgrey)
        canvas.rotate(45)
        canvas.drawString(100, 0, "PESA MASHINANI")
        canvas.restoreState()

        # Add flower-like decorative borders
        self.add_flower_border(canvas, doc)

    def add_flower_border(self, canvas, doc):
        # Define flower color and position
        flower_color = HexColor('#003366')  # Dark blue

        # Draw flowers on corners
        canvas.saveState()
        canvas.setStrokeColor(flower_color)
        canvas.setFillColor(flower_color)

        # Flower pattern coordinates
        flower_size = 10

        # Top-left corner
        canvas.circle(20, doc.height - 20, flower_size, stroke=1, fill=1)

        # Top-right corner
        canvas.circle(doc.width - 20, doc.height - 20, flower_size, stroke=1, fill=1)

        # Bottom-left corner
        canvas.circle(20, 20, flower_size, stroke=1, fill=1)

        # Bottom-right corner
        canvas.circle(doc.width - 20, 20, flower_size, stroke=1, fill=1)

        canvas.restoreState()

        # Add border to the edges of the PDF
        border_color = HexColor('#ff6600')  # Orange color for border
        border_thickness = 2

        # Draw border
        canvas.saveState()
        canvas.setStrokeColor(border_color)
        canvas.setLineWidth(border_thickness)

        # Top border
        canvas.line(0, doc.height, doc.width, doc.height)

        # Bottom border
        canvas.line(0, 0, doc.width, 0)

        # Left border
        canvas.line(0, 0, 0, doc.height)

        # Right border
        canvas.line(doc.width, 0, doc.width, doc.height)

        canvas.restoreState()


class GroupPDFGenerator:
    def __init__(self, report_data):
        self.report_data = report_data

    def generate_pdf(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Define custom styles
        custom_styles = self.create_custom_styles()

        # Add header
        header = self.create_header(custom_styles)
        elements.extend(header)  # Use extend to add multiple elements

        # Add form sections
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_one(elements, custom_styles)
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_two(elements, custom_styles)
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_three(elements, custom_styles)

        # Add decorative borders and watermark
        doc.build(elements, onFirstPage=self.add_decorations, onLaterPages=self.add_decorations)

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def create_custom_styles(self):
        # Define custom styles with attractive fonts and colors
        custom_styles = {
            'title': ParagraphStyle(
                'title',
                fontName='Helvetica-Bold',
                fontSize=18,
                textColor=HexColor('#003366'),  # Dark blue
                alignment=1,  # Center alignment
                spaceAfter=12,
            ),
            'header': ParagraphStyle(
                'header',
                fontName='Helvetica-Bold',
                fontSize=14,
                textColor=HexColor('#003366'),  # Dark blue text
                spaceAfter=6,
                spaceBefore=6,
                alignment=1,  # Center alignment
            ),
            'normal': ParagraphStyle(
                'normal',
                fontName='Helvetica',
                fontSize=12,
                textColor=HexColor('#333333'),  # Dark grey text
                spaceAfter=12,  # Add more space after
            ),
            'highlight': ParagraphStyle(
                'highlight',
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=HexColor('#003366'),  # Dark blue text
                spaceAfter=12,  # Add more space after
            ),
        }
        return custom_styles

    def create_header(self, styles):
        # Header with group information
        header_content = [
            Paragraph('PESA MASHINANI', styles['header']),
            Paragraph('Group Registration Form', styles['header']),
            Spacer(1, 24),  # Add more space
            Spacer(1, 24),  # Add more space
            
        ]
        return header_content

    def add_section_one(self, elements, styles):
        section_title = Paragraph("Section I: Group Information", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph("Group Name: <u>____________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Chairman Id Number: <u>____________________________</u>", styles['highlight']))
        elements.append(Paragraph("Chairman Phone Number: <u>___________________________</u>", styles['highlight']))
        elements.append(Paragraph("Sign: <u>___________________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>___________________________________________</u>", styles['highlight']))

    def add_section_two(self, elements, styles):
        section_title = Paragraph("Section II: Guarantor Information", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph(f"Guarantor Id Number: <u>{self.report_data['guarantor_details']['National ID Number']}</u>", styles['highlight']))
        elements.append(Paragraph(f"Guarantor First Name: <u>{self.report_data['guarantor_details']['First Name']}</u>", styles['highlight']))
        elements.append(Paragraph(f"Guarantor Last Name: <u>{self.report_data['last_name']}</u>", styles['highlight']))
        elements.append(Paragraph(f"Guarantor Phone Number: <u>{self.report_data['phone_number']}</u>", styles['highlight']))
        elements.append(Paragraph("Sign: <u>___________________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>___________________________________________</u>", styles['highlight']))
        
        # Ensure the stamp field has enough space
        elements.append(Paragraph(f"{self.report_data['guarantor_details']['First Name']} {self.report_data['last_name']} Official Stamp:", styles['highlight']))
        elements.append(Spacer(1, 2))
        elements.append(StampBox())  # Add the custom stamp box flowable


    def add_section_three(self, elements, styles):
        section_title = Paragraph("Section III: Mashinani Official Use", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph("Mashinani Registrar Name: <u>________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Sign: <u>________________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>________________________________________</u>", styles['highlight']))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph("<b>Note:</b><i>Carry with you this form dully filled while coming for</i>", styles['highlight']))
        elements.append(Paragraph("<i>Registration</i>", styles['highlight']))




    def add_decorations(self, canvas, doc):
        # Add watermark
        canvas.saveState()
        canvas.setFont('Helvetica', 60)
        canvas.setStrokeColor(HexColor('#003366'))  # Dark blue
        canvas.setFillColor(lightgrey)
        canvas.rotate(45)
        canvas.drawString(100, 0, "PESA MASHINANI")
        canvas.restoreState()

        # Add flower-like decorative borders
        self.add_flower_border(canvas, doc)

    def add_flower_border(self, canvas, doc):
        # Define flower color and position
        flower_color = HexColor('#003366')  # Dark blue

        # Draw flowers on corners
        canvas.saveState()
        canvas.setStrokeColor(flower_color)
        canvas.setFillColor(flower_color)

        # Flower pattern coordinates
        flower_size = 10

        # Top-left corner
        canvas.circle(20, doc.height - 20, flower_size, stroke=1, fill=1)

        # Top-right corner
        canvas.circle(doc.width - 20, doc.height - 20, flower_size, stroke=1, fill=1)

        # Bottom-left corner
        canvas.circle(20, 20, flower_size, stroke=1, fill=1)

        # Bottom-right corner
        canvas.circle(doc.width - 20, 20, flower_size, stroke=1, fill=1)

        canvas.restoreState()

        # Add border to the edges of the PDF
        border_color = HexColor('#ff6600')  # Orange color for border
        border_thickness = 2

        # Draw border
        canvas.saveState()
        canvas.setStrokeColor(border_color)
        canvas.setLineWidth(border_thickness)

        # Top border
        canvas.line(0, doc.height, doc.width, doc.height)

        # Bottom border
        canvas.line(0, 0, doc.width, 0)

        # Left border
        canvas.line(0, 0, 0, doc.height)

        # Right border
        canvas.line(doc.width, 0, doc.width, doc.height)

        canvas.restoreState()
        
        
class BankPDFGenerator:
    def __init__(self, report_data):
        self.report_data = report_data

    def generate_pdf(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Define custom styles
        custom_styles = self.create_custom_styles()

        # Add header
        header = self.create_header(custom_styles)
        elements.extend(header)  # Use extend to add multiple elements

        # Add form sections
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_one(elements, custom_styles)
        elements.append(Spacer(1, 24))  # Add more space
        #self.add_section_two(elements, custom_styles)
        elements.append(Spacer(1, 24))  # Add more space
        self.add_section_three(elements, custom_styles)

        # Add decorative borders and watermark
        doc.build(elements, onFirstPage=self.add_decorations, onLaterPages=self.add_decorations)

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def create_custom_styles(self):
        # Define custom styles with attractive fonts and colors
        custom_styles = {
            'title': ParagraphStyle(
                'title',
                fontName='Helvetica-Bold',
                fontSize=18,
                textColor=HexColor('#003366'),  # Dark blue
                alignment=1,  # Center alignment
                spaceAfter=12,
            ),
            'header': ParagraphStyle(
                'header',
                fontName='Helvetica-Bold',
                fontSize=14,
                textColor=HexColor('#003366'),  # Dark blue text
                spaceAfter=6,
                spaceBefore=6,
                alignment=1,  # Center alignment
            ),
            'normal': ParagraphStyle(
                'normal',
                fontName='Helvetica',
                fontSize=12,
                textColor=HexColor('#333333'),  # Dark grey text
                spaceAfter=12,  # Add more space after
            ),
            'highlight': ParagraphStyle(
                'highlight',
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=HexColor('#003366'),  # Dark blue text
                spaceAfter=12,  # Add more space after
            ),
        }
        return custom_styles

    def create_header(self, styles):
        # Header with group information
        header_content = [
            Paragraph('PESA MASHINANI', styles['header']),
            Paragraph('Bank Registration Form', styles['header']),
            Spacer(1, 24),  # Add more space
            Spacer(1, 24),  # Add more space
        ]
        return header_content

    def add_section_one(self, elements, styles):
        section_title = Paragraph("Section I: Bank Information", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph(f"Bank Name: <i>{self.report_data['bank_name']}</i>", styles['highlight']))
        elements.append(Paragraph("Sign: <u>____________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>____________________________________</u>", styles['highlight']))
        
        # Ensure the stamp field has enough space
        elements.append(Spacer(1, 12))  # Add space before the stamp box
        elements.append(Paragraph(f"{self.report_data['bank_name']} Official Stamp:", styles['highlight']))
        elements.append(Spacer(1, 2))
        elements.append(StampBox())  # Add the custom stamp box flowable


    def add_section_three(self, elements, styles):
        section_title = Paragraph("Section II:Mashinani Official Use", styles['title'])
        elements.append(section_title)

        # Add labeled lines for user input with highlighted placeholders
        elements.append(Paragraph("Mashinani Registrar Name: <u>________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Sign: <u>________________________________________</u>", styles['highlight']))
        elements.append(Paragraph("Date: <u>________________________________________</u>", styles['highlight']))

        # Ensure the stamp field has enough space
        elements.append(Spacer(1, 12))  # Add space before the stamp box
        elements.append(Paragraph("Mashinani Official Stamp:", styles['highlight']))
        elements.append(Spacer(1, 2))
        elements.append(StampBox())  # Add the custom stamp box flowable
        
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("<b>Note:</b><i>Carry with you this form dully filled while coming for</i>", styles['highlight']))
        elements.append(Paragraph("<i>Registration</i>", styles['highlight']))



    def add_decorations(self, canvas, doc):
        # Add watermark
        canvas.saveState()
        canvas.setFont('Helvetica', 60)
        canvas.setStrokeColor(HexColor('#003366'))  # Dark blue
        canvas.setFillColor(lightgrey)
        canvas.rotate(45)
        canvas.drawString(100, 0, "PESA MASHINANI")
        canvas.restoreState()

        # Add flower-like decorative borders
        self.add_flower_border(canvas, doc)

    def add_flower_border(self, canvas, doc):
        # Define flower color and position
        flower_color = HexColor('#003366')  # Dark blue

        # Draw flowers on corners
        canvas.saveState()
        canvas.setStrokeColor(flower_color)
        canvas.setFillColor(flower_color)

        # Flower pattern coordinates
        flower_size = 10

        # Top-left corner
        canvas.circle(20, doc.height - 20, flower_size, stroke=1, fill=1)

        # Top-right corner
        canvas.circle(doc.width - 20, doc.height - 20, flower_size, stroke=1, fill=1)

        # Bottom-left corner
        canvas.circle(20, 20, flower_size, stroke=1, fill=1)

        # Bottom-right corner
        canvas.circle(doc.width - 20, 20, flower_size, stroke=1, fill=1)

        canvas.restoreState()

        # Add border to the edges of the PDF
        border_color = HexColor('#ff6600')  # Orange color for border
        border_thickness = 2

        # Draw border
        canvas.saveState()
        canvas.setStrokeColor(border_color)
        canvas.setLineWidth(border_thickness)

        # Top border
        canvas.line(0, doc.height, doc.width, doc.height)

        # Bottom border
        canvas.line(0, 0, doc.width, 0)

        # Left border
        canvas.line(0, 0, 0, doc.height)

        # Right border
        canvas.line(doc.width, 0, doc.width, doc.height)

        canvas.restoreState()

class StampBox(Flowable):
    def __init__(self, width=2 * inch, height=1 * inch):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        # Draw the stamp box
        self.canv.setStrokeColor(HexColor('#003366'))  # Dark blue
        self.canv.setFillColor(lightgrey)
        self.canv.rect(0, 0, self.width, self.height, fill=1)



def generate_number():
    """Generate a random 10-character alphanumeric allocation number."""
    letters = string.ascii_uppercase
    digits = string.digits
    allocation_no = ''.join(random.choice(letters + digits) for _ in range(10))
    return allocation_no

def unique_allocation_number():
    """Generate a unique allocation number not already in use."""
    while True:
        allocation_no = generate_number()
        if not Allocation.objects.filter(allocation_no=allocation_no).exists():
            return allocation_no
        
def unique_application_number():
    """Generate a unique application number not already in use."""
    while True:
        application_no = generate_number()
        if not Application.objects.filter(application_no=application_no).exists():
            return application_no

def generate_unique_member_number():
        while True:
            # Generate first 3 uppercase letters
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            # Generate 3 digits
            digits = ''.join(random.choices(string.digits, k=3))
            member_no = letters + digits
            
            # Check if the member number already exists in the Message table
            if not GroupMember.objects.filter(member_no=member_no).exists():
                return member_no
        
def unique_transaction_number():
    """Generate a unique allocation number not already in use."""
    while True:
        transaction_no = generate_number()
        if not Disbursement.objects.filter(transaction_no=transaction_no).exists():
            return transaction_no
        
def unique_payment_number():
    """Generate a unique allocation number not already in use."""
    while True:
        payment_no = generate_number()
        if not Payment.objects.filter(payment_no=payment_no).exists():
            return payment_no
        
        
def generate_borrower_username(email_address):
    # Check if the email ends with @gmail.com or @hotmail.com
    if email_address.endswith('@gmail.com') or email_address.endswith('@hotmail.com') or email_address.endswith('.co.ke') or email_address.endswith('.org.ke'):
        # Split the email address at '@' kcb@group.co.ke
        local_part = email_address.split('@')[0]
        # Generate the new email address ending with '@lender.co.ke'
        new_email_address = f"{local_part}@borrower.co.ke"
        return new_email_address
    
def generate_lender_username(email_address):
    # Check if the email ends with @gmail.com or @hotmail.com
    if email_address.endswith('@gmail.com') or email_address.endswith('@hotmail.com') or email_address.endswith('.co.ke') or email_address.endswith('.org.ke'):
        # Split the email address at '@' kcb@group.co.ke
        local_part = email_address.split('@')[0]
        # Generate the new email address ending with '@lender.co.ke'
        new_email_address = f"{local_part}@lender.co.ke"
        return new_email_address
    
    
def generate_unique_borrower_number(national_id_no, email_address):
    # Split the email address to get the local part (before the '@' symbol)
    local_part = email_address.split('@')[0]
    
    # Get the first 3 digits of the identification number
    first_three_digits = str(national_id_no)[:3]
    
    # Get the current year
    current_year = time.strftime("%Y")
    
    # Generate the unique identifier
    unique_id = f"{local_part}/{first_three_digits}@borrower/{current_year}"
    return unique_id

def generate_unique_lender_number(national_id_no, email_address):
    # Split the email address to get the local part (before the '@' symbol)
    local_part = email_address.split('@')[0]
    
    # Get the first 3 digits of the identification number
    first_three_digits = str(national_id_no)[:3]
    
    # Get the current year
    current_year = time.strftime("%Y")
    
    # Generate the unique identifier
    unique_id = f"{local_part}/00{first_three_digits}@lender/{current_year}"
    return unique_id

def generate_lender_number(email_address):
    # Split the email address to get the local part (before the '@' symbol)
    local_part = email_address.split('@')[0]
    
    # Get the current year
    current_year = time.strftime("%Y")
    
    # Generate the unique identifier
    unique_id = f"{local_part}/001/{current_year}@lender"
    return unique_id

def generate_unique_message_number():
    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=3))
        message_no = letters + digits
        if not Message.objects.filter(message_no=message_no).exists():
            return message_no

def calculate_time_elapsed_in_months(disbursement_date):
    # Get the current date
    current_date = datetime.now().date()
    
    # Calculate the time elapsed in months
    time_elapsed_months = (
        (current_date.year - disbursement_date.year) * 12 +
        (current_date.month - disbursement_date.month)
    )
    
    return time_elapsed_months

def calculate_compound_interest(principal, monthly_rate, number_of_months):
        """
        Calculate compound interest based on principal, annual rate, and number of years.
        
        :param principal: The principal amount (initial loan amount).
        :param monthly_rate: The annual interest rate (in percentage, e.g., 5 for 5%).
        :param number_of_months: The number of years the interest is compounded.
        :return: The compound interest earned.
        """
        # Convert inputs to Decimal
        principal = Decimal(principal)
        monthly_rate = Decimal(monthly_rate)
        number_of_months = Decimal(number_of_months)
        
        # Calculate the amount after interest
        amount = principal * (1 + monthly_rate / 100) ** number_of_months
        
        return amount
    
    
def delete_zero_balance_loans():
    zero_balance_loans = Loan.objects.filter(balance=0)
    zero_balance_loans.delete()
