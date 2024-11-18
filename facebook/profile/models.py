from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    bio = models.TextField(
        _("Bio"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_("Tell us something about yourself (max 500 characters)."),
    )
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ["user__date_joined"]  

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"
