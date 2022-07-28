from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# Create your models here.




class WikiPost(models.Model):
    name = models.CharField('', max_length=20, primary_key=True)
    content = models.TextField('')
    created_at = models.DateTimeField(auto_now_add=True)
    #modify_date = models.DateTimeField(null=True, blank=True)
    #author= models.ForeignKey(User, on_delete=models.CASCADE)
    #changed_by = models.ForeignKey('auth.User')
    changed_by = models.ForeignKey(User, on_delete=models.SET("탈퇴한 사용자"))
    history = HistoricalRecords(cascade_delete_history=True)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
