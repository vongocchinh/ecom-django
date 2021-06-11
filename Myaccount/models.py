from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    org = models.CharField('Organization', max_length=128, blank=True)

    telephone = models.CharField('Telephone', max_length=50, blank=True)

    mod_date = models.DateTimeField('Last modified', auto_now=True)


    def __str__(self):
        # return "{}'s profile".format(self.user.__str__())

        return self.user.username
        
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False