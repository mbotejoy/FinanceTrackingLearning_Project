from django.db import models


class LearningContent(models.Model):

    TOPIC_CHOICES = [
        ("budgeting", "Budgeting"),
        ("saving", "Saving"),
        ("debt", "Debt Management"),
        ("spending", "Responsible Spending"),
        ("fraud", "Financial Fraud and Scams"),
        ("investing", "Introduction to Investing"),
    ]

    title = models.CharField(max_length=200)

    topic = models.CharField(
        max_length=30,
        choices=TOPIC_CHOICES
    )

    description = models.TextField(
        help_text="A short summary of the lesson."
    )

    content = models.TextField(
        help_text="The full financial education lesson."
    )

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "learning_content"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title