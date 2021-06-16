import random
from django.db import models
from django.contrib.auth.models import User

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

class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(
        help_text='UNCHECKING WILL SUBMIT ALL ONGOING SESSIONS OF THIS EXAM.'
    )

    def __str__(self):
        return self.name


class Question(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField(max_length=1000)
    option_A = models.CharField(max_length=200)
    option_B = models.CharField(max_length=200)
    option_C = models.CharField(max_length=200)
    option_D = models.CharField(max_length=200)
    correct_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES,
        default=A
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.question


class Session(models.Model):
    """User's exam session"""
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField(Question)

    def get_questions(self):
        questions = list(
            self.exam.question_set.filter(created__lt=self.created)
        )
        rand = random.Random(self.seed)
        rand.shuffle(questions)

        return questions

    def __str__(self):
        return self.exam.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES,
        default=A
    )

    def __str__(self):
        return self.answer
