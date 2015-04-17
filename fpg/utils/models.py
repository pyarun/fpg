from django.db import models


class Sports(models.Model):
    '''
        Game model for perticular game for which user will be booking slot
    '''
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.name