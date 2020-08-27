from django.db import models

# Create your models here.
class Data(models.Model):
    old_data = models.TextField()
    spam_data = models.TextField()

    def stuff(self):
        return [self.old_data, self.spam_data]