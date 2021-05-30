from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    active = models.BooleanField()

    def __str__(self):
        return self.name

class MCQ(models.Model):

    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'

    ANSWER_CHOICES = [
        (A, A),
        (B, B),
        (C, C),
        (D, D),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField(max_length=1000)
    option_A = models.CharField(max_length=200)
    option_B = models.CharField(max_length=200)
    option_C = models.CharField(max_length=200)
    option_D = models.CharField(max_length=200)
    answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES,
        default=A
    )

    def __str__(self):
        return self.question
