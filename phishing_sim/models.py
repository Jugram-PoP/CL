from django.db import models
from django.conf import settings

class Scenario(models.Model):
    subject = models.CharField(max_length=200)
    sender = models.CharField(
        max_length=255, 
        help_text="e.g. 'IT Support <it-support@university.edu>'"
    )
    body = models.TextField()
    is_phishing = models.BooleanField()
    red_flags = models.JSONField(
        default=list,
        blank=True,
        help_text="Structured list of red flag explanations"
    )
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.subject


class Attempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="phishing_attempts"
    )
    scenario = models.ForeignKey(
        Scenario, 
        on_delete=models.CASCADE,
        related_name="attempts"
    )
    marked_as_phishing = models.BooleanField()
    is_correct = models.BooleanField(editable=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "scenario"], 
                name="unique_user_scenario_attempt"
            )
        ]
        indexes = [
            models.Index(fields=["user", "is_correct"]),
        ]

    def save(self, *args, **kwargs):
        # Automatically compute correctness on save
        if self.scenario_id:
            self.is_correct = (self.marked_as_phishing == self.scenario.is_phishing)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} — {self.scenario} ({'Correct' if self.is_correct else 'Incorrect'})"