from django.db import models



from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        """
        Creates and saves a User with the given mobile and password.
        """
        if not mobile:
            raise ValueError('The given email must be set')
        # email = self.normalize_email(email)
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, password, **extra_fields)




import uuid
class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), blank=True,unique=True)
    password = models.CharField(_('password'),max_length=90,blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_verified = models.BooleanField(default=True, null=True)
    is_active = models.BooleanField(_('active'), default=True, null=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.name

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }




class ClockIn(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    login_date = models.DateField(null=True)  # user login date store with custom date field
    login_time = models.TimeField(
        auto_now_add=True)  # user login time stores this time will be generating automatically once login into the user page

    def __str__(self):
        return str(self.user) + ': ' + str(self.login_time)



class ClockOut(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    logout_date = models.DateField(null=True)  # user login date storing with cutom date field
    logout_time = models.TimeField(auto_now_add=True,
                                   null=True)  # user logout time stores this time will be generating automatically once login into the user page

    def __str__(self):
        return str(self.user) + ': ' + str(self.logout_time)




class ProductiveHours(models.Model):
    user_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.CharField(max_length=50, null=True, blank=True)
    login_date = models.CharField(max_length=50, null=True, blank=True)
    diiffrences = models.CharField(max_length=90, null=True, blank=True)


    def __str__(self):
        return str(self.user) + ': ' + str(self.diiffrences)
