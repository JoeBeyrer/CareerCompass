from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError


class RecruiterForm(forms.Form):
    userID = forms.CharField(max_length=15, required=True, validators=[RegexValidator(r'^[a-zA-Z0-9_]*$', message='Only alphanumeric characters and underscore are allowed.')])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    fName = forms.CharField(max_length=20, required=True)
    lName = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=63, required=True)
    company_name = forms.CharField(max_length=20, required=True)
    position = forms.CharField(max_length=20, required=True)
    about_company = forms.CharField(widget=forms.Textarea, required=True)
    about_me = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("The passwords do not match. Please enter the same password in both fields.")

class StudentForm(forms.Form):
    userID = forms.CharField(max_length=15, required=True, validators=[RegexValidator(r'^[a-zA-Z0-9_]*$', message='Only alphanumeric characters and underscore are allowed.')])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    fName = forms.CharField(max_length=20, required=True)
    lName = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=63, required=True)
    university = forms.CharField(max_length=60, required=True)
    degree = forms.CharField(max_length=48, required=True)
    current_year = forms.CharField(max_length=9, required=True)
    expected = forms.DateField(required=True)
    gpa = forms.DecimalField(max_digits=3, decimal_places=2, required=True, validators=[MinValueValidator(0.00), MaxValueValidator(4.00)])
    open_to_work = forms.CharField(max_length=3, required=True)
    about_me = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("The passwords do not match. Please enter the same password in both fields.")

class EditProfileForm(forms.Form):
    userID = forms.CharField(max_length=15, required=False, validators=[RegexValidator(r'^[a-zA-Z0-9_]*$', message='Only alphanumeric characters and underscore are allowed.')])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=False)
    fName = forms.CharField(max_length=20, required=False)
    lName = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(max_length=63, required=False)
    about_me = forms.CharField(widget=forms.Textarea, required=False)

    # Recruiter fields
    company_name = forms.CharField(max_length=20, required=False)
    position = forms.CharField(max_length=20, required=False)
    about_company = forms.CharField(widget=forms.Textarea, required=False)

    # Student fields
    university = forms.CharField(max_length=60, required=False)
    degree = forms.CharField(max_length=48, required=False)
    current_year = forms.CharField(max_length=9, required=False)
    expected = forms.DateField(required=False)
    gpa = forms.DecimalField(max_digits=3, decimal_places=2, required=False, validators=[MinValueValidator(0.00), MaxValueValidator(4.00)])
    open_to_work = forms.CharField(max_length=3, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("The passwords do not match. Please enter the same password in both fields.")

class PostForm(forms.Form):
    Title = forms.CharField(max_length=30, required=True)
    BodyText = forms.CharField(widget=forms.Textarea, required=True)
    Field = forms.CharField(max_length=20, required=True)