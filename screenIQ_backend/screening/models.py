from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):
    candidate_name = models.CharField(max_length=255)

    job_description = models.TextField()

    resume = models.TextField()

    ai_score = models.FloatField()

    ai_reasons = models.JSONField(default=list)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_name} - {self.ai_score}"