from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


CITY_CHOICE = (
    ('bukavu', 'Bukavu'),
    ('bujumbura', 'Bujumbura'),
    ('goma', 'Goma'),
    ('uvira', 'Uvira'),
)


class MyUserManager(UserManager):
    pass


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        unique=True,
        max_length=255,
        blank=False
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=128,
        unique=True,
        help_text=_(
            "Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    profile_picture = models.ImageField(upload_to='Shopper', blank=True, null=True, verbose_name='photo de profil')

    # champ obligatoire par python
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    # is_active = models.BooleanField(default=True)  # obligatoire
    # is_staff = models.BooleanField(default=False)  # obligatoire
    is_admin = models.BooleanField(
        _("admin"),
        default=False,
        help_text=_("Designates whether this user should be treated as admin user. ")
    )

    # zip_code = models.CharField(blank=True, max_length=5)
    # age = models.PositiveIntegerField()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyUserManager()

    # plus besoins comm on herite de permissionmixin
    """
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    """

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Utilisateur'


class Follower(models.Model):
    following = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='following', verbose_name='abonement')
    followed = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='followed', verbose_name='abonné')

    class Meta:
        verbose_name = 'Abonement'


class Address(models.Model):
    customer_user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, verbose_name='Utilisateur')
    number = models.CharField(max_length=8, verbose_name='Numéro')
    street = models.CharField(max_length=128, verbose_name='Rue')
    zip_code = models.CharField(max_length=5, blank=True, verbose_name='Code Postal')
    neighborhood = models.CharField(max_length=128, verbose_name='Quartier')
    commune = models.CharField(max_length=128, verbose_name='Commune')
    city = models.CharField(max_length=128, choices=CITY_CHOICE, default='bukavu', verbose_name='ville')

    class Meta:
        verbose_name = 'Adresse de résidence'

    def __str__(self):
        return f'{self.number} rue {self.street} {self.neighborhood} {self.commune} {self.city}'
