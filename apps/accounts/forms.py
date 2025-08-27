from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='RePassword', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'email', 'name', 'family', 'gender')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تکرار آن با هم مغایرت دارند")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
#__________________________________________________________________________________________________
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور روی <a href='../password/'>این لینک</a> کلیک کنید.")
    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'email', 'name', 'family', 'gender','password','is_active','is_admin')
#__________________________________________________________________________________________________

class RegisterUserForm(ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'رمز عبور را وارد کنید'},))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'تکرار رمز عبور را وارد کنید'},))
    class Meta:
        model = CustomUser
        fields= ('mobile_number',)
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'موبایل را وارد کنید'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تکرار آن با هم مغایرت دارند")
        return password2
#__________________________________________________________________________________________________

class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',
                                  error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'کد دریافتی را وارد کنید'}),
                                  )
#__________________________________________________________________________________________________

class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',
                                  error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'شماره موبایل را وارد کنید'}),
                                  )
    password = forms.CharField(label='رمز عبور',
                                    error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را وارد کنید'}),
                                    )
#__________________________________________________________________________________________________

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='رمز عبور',
                                error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را وارد کنید'})
                                )
    password2 = forms.CharField(label='رمز عبور',
                                error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور را وارد کنید'})
                                )
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تکرار آن با هم مغایرت دارند")
        return password2
#__________________________________________________________________________________________________
class RememberPasswordForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',
                                    error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل را وارد کنید'})
                                    )