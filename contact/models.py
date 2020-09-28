from django.db import models
from users.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    email = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        db_table = "contact"
