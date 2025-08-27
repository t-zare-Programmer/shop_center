from django.contrib.messages import success
from django.shortcuts import render, redirect
from  django.views import View
from requests import session

from apps.accounts.forms import RegisterUserForm, VerifyRegisterForm,LoginUserForm,ChangePasswordForm,RememberPasswordForm
import utils
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from  django.contrib.auth.mixins import LoginRequiredMixin

#____________________________________________________________________________________
class RegisterUserView(View):
    template_name = 'accounts_app/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            active_code = utils.create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                active_code=active_code,
                password=data['password1'],

            )
            utils.send_sms(data['mobile_number'], f'کد فعالسازی حساب کاربری شما {active_code} می باشد')
            request.session['user_session'] = {
                'mobile_number': data['mobile_number'],
                'active_code': str(active_code),
                'remember_password': False
            }
            messages.success(request, 'اطلاعات شما ثبت شد. کد فعالسازی را وارد کنید','success')
            return redirect('accounts:verify')
        messages.error(request,'خطا در انجام ثبت نام','danger')
        return render(request, self.template_name, {'form': form})
#____________________________________________________________________________________
class VerifyRegisterCodeView(View):
    template_name = 'accounts_app/verify_register_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = VerifyRegisterForm()
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            if data['active_code'] == user_session['active_code']:
               user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
               if user_session['remember_password'] == False:
                    user.is_active = True
                    user. active_code = utils.create_random_code(5)
                    user.save()
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('main:index')
               else:
                   return redirect('accounts:change_password')
            else:
                messages.error(request, 'کد فعالسازی وارد شده اشتباه می باشد', 'danger')
                return render(request, 'accounts_app/verify_register_code.html', {'form': form})
        messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
        return render(request, 'accounts_app/verify_register_code.html', {'form': form})

# __________________________________________________________________________________________________________________

class LoginUserView(View):
    template_name = 'accounts_app/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
            form = LoginUserForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
            form = LoginUserForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(username=data['mobile_number'], password=data['password'])
                if user is not None:
                    db_user = CustomUser.objects.get(mobile_number=data['mobile_number'])
                    if db_user.is_admin == False:
                        messages.success(request, 'ورود با موفقیت انجام شد', 'success')
                        login(request, user)
                        next_url = request.GET.get('next')
                        if next_url is not None:
                            return redirect(next_url)
                        else:
                            return redirect('main:index')
                    else:
                        messages.error(request, 'کاربر ادمین نمی تواند از اینجا وارد شود', 'warning')
                        return render(request, self.template_name, {'form': form})

                else:
                    messages.error(request, 'اطلاعات وارد شده نادرست است', 'danger')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.error(request, 'اطلاعات وارد شده نامعتبر است', 'danger')
                return render(request, self.template_name, {'form': form})

# __________________________________________________________________________________________________________________
class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_data = request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart'] = session_data
        return redirect('main:index')

# __________________________________________________________________________________________________________________
class ChangePasswordView(View):
    template_name = 'accounts_app/change_password.html'
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            user=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code = utils.create_random_code(5)
            user.save()
            messages.success(request,'رمز عبور شما با موفقیت تغییر کرد','success')
            return redirect('accounts:login')
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمی باشد', 'danger')
            return render(request,self.template_name,{'form':form})

# __________________________________________________________________________________________________________________
class RememberPasswordView(View):
    template_name = 'accounts_app/remember_password.html'
    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                user = CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code = utils.create_random_code(5)
                user.active_code=active_code
                user.save()
                utils.send_sms(data['mobile_number'], f'کد تایید شماره موبایل شما {active_code} می باشد')
                request.session['user_session'] = {
                    'mobile_number': data['mobile_number'],
                    'active_code': str(active_code),
                    'remember_password': True
                }
                messages.success(request,'جهت تغییر رمز عبور خود کد دریافتی را ارسال کنید','success')
                return redirect('accounts:verify')
            except:
                messages.error(request,'شماره موبایل وارد شده موجود نمی باشد')
                return render(request,self.template_name,{'form':form})

# __________________________________________________________________________________________________________________
class UserPanelView(LoginRequiredMixin,View):
    template_name = 'accounts_app/userpanel.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)