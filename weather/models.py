from django.db import models
from django.utils import timezone

class AICropAdvice(models.Model):
    watering = models.TextField()
    fertilization = models.TextField()
    pest_risk = models.TextField()
    harvest = models.TextField()
    weather_alerts = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def is_fresh(self):
        # consider advice fresh for 1 hour
        return (timezone.now() - self.created_at).seconds < 3600
