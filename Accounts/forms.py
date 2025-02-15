from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class' : 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class' : 'form-control'
    }))
    email = forms.EmailField()
    phone_number = forms.CharField()

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
        # fields = '__all__' (for getting all fields from models)


    # To give CSS Properties to the Forms
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name':'Enter First Name',
            'last_name' : 'Enter last Nmae',
            'phone_number' : 'Enter phone Number',
            'email' : 'Enter Email Adress',
        }
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder

        #               (Another way to Save Placeholders)
        # self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'   
        # self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        # self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        # self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # Function To check password and confirm_password is same.
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean() # (can also write) cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data
    
    # Function To check if same email exists in the database. 
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    # Function To check if same phone_number exists in the database.
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        
        if Account.objects.filter(phone_number = phone_number).exists():  
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone_number