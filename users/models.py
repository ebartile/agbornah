import uuid
import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core import validators
from django.utils.translation import gettext_lazy as _

class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django"s Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(_("superuser status"), default=False,
        help_text=_("Designates that this user has all permissions without "
                    "explicitly assigning them."))

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

def get_default_uuid():
    return uuid.uuid4().hex

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.CharField(max_length=32, editable=False, null=False,
                            blank=False, unique=True, default=get_default_uuid)
    username = models.CharField(_("username"), max_length=255, unique=True,
        help_text=_("Required. 30 characters or fewer. Letters, numbers and "
                    "/./-/_ characters"),
        validators=[
            validators.RegexValidator(re.compile(r"^[\w.-]+$"), _("Enter a valid username."), "invalid")
        ])
    email = models.EmailField(_("email address"), max_length=255, null=False, blank=False, unique=True)
    is_active = models.BooleanField(_("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    full_name = models.CharField(_("full name"), max_length=256, blank=True)
    bio = models.TextField(null=False, blank=True, default="", verbose_name=_("biography"))

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]
