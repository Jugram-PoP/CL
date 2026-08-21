from django.db import models
from django.conf import settings

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)  # controls display order: 1, 2, 3, 4

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Completion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")  # a user can only complete a given lesson once