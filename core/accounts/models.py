from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

from django_tenants.models import TenantMixin, DomainMixin




class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for multi-tenant SaaS platform."""

    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name or self.email

    def get_short_name(self):
        return self.full_name.split(" ")[0] if self.full_name else self.email





class Tenant(TenantMixin):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Tenant configuration
    auto_create_schema = True
    auto_drop_schema = True  # Drop schema when tenant is deleted
    
    # Custom tenant settings
    max_users = models.IntegerField(default=10)
    plan_type = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('premium', 'Premium'),
            ('enterprise', 'Enterprise'),
        ],
        default='basic'
    )
    
    class TenantMeta:
        ordering = ['name']  # Default ordering

    def __str__(self):
        return self.name

    @property
    def is_premium(self):
        return self.plan_type == 'premium'

    def deactivate(self):
        """Deactivate tenant"""
        self.is_active = False
        self.save()

class Domain(DomainMixin):
    is_primary = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"
    
    def __str__(self):
        return self.domain