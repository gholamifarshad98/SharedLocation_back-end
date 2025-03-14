# api/models.py
from django.db import models
from django.contrib.auth.models import User

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s location at {self.last_updated}"

class SharedUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_users')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    last_viewed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'shared_with')

    def __str__(self):
        return f"{self.owner.username} shares with {self.shared_with.username}"

class AllowedUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allowed_users')
    allowed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allowed_by')
    last_viewed = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('owner', 'allowed_to')

    def __str__(self):
        return f"{self.owner.username} allows {self.allowed_to.username}"