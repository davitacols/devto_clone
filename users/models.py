from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    class Meta:
        permissions = (("can_view_profile", "Can view profile"),)
        unique_together = ('username', 'email')

    # Override groups and user_permissions to add related names
    groups = models.ManyToManyField(
        Group,
        related_name="custom_users",  # Specify a unique related name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_users",  # Specify a unique related name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username
