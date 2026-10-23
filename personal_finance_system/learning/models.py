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


class QuizQuestion(models.Model):

    ANSWER_CHOICES = [
        ("A", "Option A"),
        ("B", "Option B"),
        ("C", "Option C"),
        ("D", "Option D"),
    ]

    TOPIC_CHOICES = LearningContent.TOPIC_CHOICES

    topic = models.CharField(
        max_length=30,
        choices=TOPIC_CHOICES
    )

    question_text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES
    )

    explanation = models.TextField(
        blank=True,
        help_text="Explain why the answer is correct."
    )

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_questions"
        ordering = ["topic", "id"]

    def __str__(self):
        return self.question_text
