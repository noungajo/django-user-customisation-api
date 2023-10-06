from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
#from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
# Create your models here.
choix_remuneration = [   ('mensuel', 'mensuel'),
    ('taux horaire', 'taux horaire')]
class AbstractUser(AbstractBaseUser, PermissionsMixin):

    #username_validator = UnicodeUsernameValidator()
    
    full_name = models.CharField(("full name"), max_length=150, blank=False)
    address = models.CharField(("address"), max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(("date of birth"), blank=True, null=True)
    numero_social = models.CharField(max_length=50, null=True, blank=True)
    remuneration = models.CharField(choices=choix_remuneration,max_length=12)
    base_salary = models.IntegerField(default=0)
    telephone = models.CharField(
        ("telephone"), 
        max_length=150, 
        blank=False, 
        #unique=True
    )
    email = models.EmailField(("email address"), blank=True, null=True, unique=True)
   
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    
 
    is_active = models.BooleanField(
        ("active"),
        default=False,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(("date joined"), auto_now_add=True)
    user_image = models.ImageField(upload_to='static/users/images/%Y/%m/%d/', null=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    #EMAIL_FIELD = "telephone"
    USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = ["telephone"]
    """
    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")
        abstract = True
    """
    

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

        
    
class User(AbstractUser):
    pass


class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    phone_number = models.CharField(max_length=30)
    code = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True)
class ResetPasswordModel(models.Model):
    email = models.CharField(max_length=30)
    code = models.CharField(max_length=14)