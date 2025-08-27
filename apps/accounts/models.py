from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,UserManager
from django.utils import timezone
from utils import FileUpload
#______________________________________________________________________________
class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,email="",name="",family="",active_code=None,gender=None,password=None):
        if not mobile_number:
            raise ValueError('شماره موبایل باید وارد شود')
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    #________________________________________
    def create_superuser(self,mobile_number,email,name,family,active_code=None,gender=None,password=None):
        user = self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            password=password,
            active_code=active_code,
            gender=gender,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#______________________________________________________________________________
class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=11, unique=True,verbose_name='شماره موبایل')
    email = models.EmailField(max_length=200 ,blank=True)
    name = models.CharField(max_length=50, blank=True,default="")
    family = models.CharField(max_length=50, blank=True, null=True)
    GENDER_CHOICES = (('True', 'مرد'),('False', 'زن'))
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='True', blank=True,null=True)
    register_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    active_code = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    username = None

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['email', 'name','family']

    objects = CustomUserManager()
    def __str__(self):
        return self.name+" "+self.family

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

#______________________________________________________________________________
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    file_upload = FileUpload('images', 'customer')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر پروفایل',null=True,blank=True)

    def __str__(self):
        return f"{self.user}"