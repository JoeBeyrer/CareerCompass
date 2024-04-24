from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError

class CreateStudentForm(forms.Form):
    field1 = forms.CharField(max_length=100)
    field2 = forms.EmailField()


class RecruiterForm(forms.Form):
    userID = forms.CharField(max_length=15, validators=[RegexValidator(r'^[a-zA-Z0-9_]*$', message='Only alphanumeric characters and underscore are allowed.')])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    fName = forms.CharField(max_length=20)
    lName = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=63)
    company_name = forms.CharField(max_length=20)
    position = forms.CharField(max_length=20)
    about_company = forms.CharField(widget=forms.Textarea)
    about_me = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("The passwords do not match. Please enter the same password in both fields.")

class StudentForm(forms.Form):
    userID = forms.CharField(max_length=15, validators=[RegexValidator(r'^[a-zA-Z0-9_]*$', message='Only alphanumeric characters and underscore are allowed.')])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    fName = forms.CharField(max_length=20)
    lName = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=63)
    university = forms.CharField(max_length=60)
    degree = forms.CharField(max_length=48)
    current_year = forms.CharField(max_length=9)
    expected = forms.DateField()
    gpa = forms.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(4.00)])
    open_to_work = forms.CharField(max_length=3)
    about_me = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("The passwords do not match. Please enter the same password in both fields.")


class PostForm(forms.Form):
    Title = forms.CharField(max_length=30)
    BodyText = forms.CharField(widget=forms.Textarea)
    Field = forms.CharField(max_length=20)