from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Application, Post, Comment, ContactFormMessage, Employee, Employer,Admin, Job,CustomUser
from django.forms import ModelForm, TextInput, Textarea, EmailInput, PasswordInput,URLField, IntegerField,ChoiceField, Select,NumberInput,URLInput, ImageField, FileField,FileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from collections import OrderedDict
import requests
# from django.db import transaction

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'firstName'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'lastName'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'email'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class EmployeeForm(forms.ModelForm):
    profession = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'username'}))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'firstName'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'id': 'file1', 'required': 'false'}))

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user']

class AdminForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'id': 'file1', 'required': 'false'}))

    class Meta:
        model = Admin
        fields = ('profile_pic',)
        exclude = ['admin']

COUNTRY_CHOICES = ()
class EmployerForm(forms.ModelForm):
    mobilenumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'username'}))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'firstName'}))
    website = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'lastName'}))
    companyinfo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','id':'lastName'}))
    companyname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'lastName'}))
    city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control','id':'email'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'id': 'file1'}))
    company_logo = forms.ImageField(widget=forms.FileInput(attrs={'id': 'file2'}))

    response = requests.get('https://restcountries.com/v3.1/all').json()
    for x in response:
        COUNTRY_CHOICES += (
            (x['name']['common'],x['name']['common']),
        )
        # print(x['Country'])
        # print(x['name']['common'])
    city = forms.ChoiceField(choices = sorted(COUNTRY_CHOICES),  widget=forms.Select(attrs={'class': 'form-control','id':'country', 'placeholder': 'City'}), required=True)

    class Meta:
        model = Employer
        fields = '__all__'
        exclude = ['user']
        # widgets = {
        #     'profile_pic':       FileInput(attrs={'name':'file'}),           
        # }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['create_at','update_at','employer', 'slug']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content','image',
        'categories','tags')

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password1','placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password2', 'placeholder': 'Password confirm'}))

    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']
        widgets = {
            'username':    TextInput(attrs={'class': 'form-control','id':'username',  'placeholder': 'Username'}),
            'first_name':  TextInput(attrs={'class': 'form-control','id':'firstname', 'placeholder': 'First name'}),
            'last_name':   TextInput(attrs={'class': 'form-control','id':'lastname', 'placeholder': 'Last name'}),
            'email':       EmailInput(attrs={'class': 'form-control','id':'email', 'placeholder': 'Your email'}),           
        }

class SignUpFormEmployee(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password1','placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password2', 'placeholder': 'Password confirm'}))

    class Meta:
        model = Employee
        fields = ['phonenumber','profession']
        widgets = {
            'phonenumber':    TextInput(attrs={'class': 'form-control','id':'username',  'placeholder': 'Username'}),
            'profession':  TextInput(attrs={'class': 'form-control','id':'firstname', 'placeholder': 'First name'}),        
        }



class SignUpFormEmployer(forms.ModelForm):
    response = requests.get('https://restcountries.com/v3.1/all').json()
    for x in response:
        COUNTRY_CHOICES += (
            (x['name']['common'],x['name']['common']),
        )
        # print(x['Country'])
        # print(x['name']['common'])
    city = forms.ChoiceField(choices = sorted(COUNTRY_CHOICES),  widget=forms.Select(attrs={'class': 'form-control','id':'city', 'placeholder': 'City'}), required=True)

    class Meta:
        model = Employer
        fields = ['city','phonenumber','website','companyname']
        widgets = { 
            'phonenumber':   NumberInput(attrs={'class': 'form-control','id':'phonenumber', 'placeholder': 'Your phone number'}),
            'companyname':   TextInput(attrs={'class': 'form-control','id':'companyname', 'placeholder': 'Your company name'}), 
            'website':       URLInput(attrs={'class': 'form-control','id':'website', 'placeholder': 'Your website'}),         
        }



class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows':'4'
    }))
    class Meta:
        model = Comment
        fields = ('content',)


class ContactFormu(forms.ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name':    TextInput(attrs={'id': 'name', 'name':'fullname', 'class': 'form-control', 'placeholder': 'Name & Surname','required':'required'}),
            'subject': TextInput(attrs={'id': 'subject','name':'subject', 'class': 'form-control', 'placeholder': 'Subject','required':'required'}),
            'email':   EmailInput(attrs={'id': 'email', 'name':'email','class': 'form-control', 'placeholder': 'Email Adress','required':'required'}),
            'message': Textarea(attrs={'id': 'message', 'name':'message','class': 'form-control', 'placeholder': 'Your Message', 'rows':'7','required':'required'}),
        }  

class ApplicationFormu(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cv','coverletter']
        widgets = {
            'cv':    FileInput(attrs={'id': 'cv', 'name':'cv', 'class': 'form-control'}),
            'coverletter': Textarea(attrs={'id': 'coverletter', 'name':'coverletter','class': 'form-control cover-leter', 'placeholder': 'Your Cover letter', 'rows':'7','required':'required'}),
        }  






#------------- Change Password -----------------------------

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("New password and repeat doesnt match."),
    }
    new_password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password1','placeholder': 'New Password'}))
    new_password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password2', 'placeholder': 'New Password confirm'}))
    

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if password1 == password2:
                if len(password1)<8:
                    raise forms.ValidationError("Password must consist of min 8 characters.")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Current password is wrong. "
                               "Please write again."),
    })
    old_password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password2', 'placeholder': 'Current Password'}))
    

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)