from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    class Meta:
        db_table = 'action'
        ordering = ["-created"]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="actions", on_delete=models.CASCADE)
    act = models.CharField(max_length=124)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType, related_name="actions", on_delete=models.CASCADE)
    target_id = models.PositiveBigIntegerField()
    target = GenericForeignKey("target_ct", "target_id")
    
    def __str__(self):
        return f'{self.user} {self.act} {self.target}'
