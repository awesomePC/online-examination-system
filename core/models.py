import random
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

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

def validate_max_duration(value):
    if value > timedelta(hours=23, minutes=59, seconds=59):
        raise ValidationError('Maximum duration is 23 hours, 59 minutes and 59 seconds.')

def validate_min_duration(value):
    if value < timedelta(seconds=1):
        raise ValidationError('Minimum duration is 1 second.')

class Exam(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    duration = models.DurationField(
        default=timedelta(hours=1),
        help_text='In format hh:mm:ss',
        validators=[validate_max_duration, validate_min_duration]
    )
    active = models.BooleanField()

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
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.question


class Session(models.Model):
    """User's exam session"""
    created = models.DateTimeField(auto_now_add=True)
    submitted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField(Question)

    def get_questions(self):
        questions = list(
            self.exam.question_set.filter(created__lt=self.created)
        )
        questions = [
            q for q in questions
            if not q.deleted or q.deleted > self.created
        ]
        rand = random.Random(self.seed)
        rand.shuffle(questions)

        return questions

    def get_num_correct_ans(self):
        answers = self.answer_set.all()
        num_correct = 0
        for answer in answers:
            if answer.answer == answer.question.correct_answer:
                num_correct += 1

        return num_correct

    def get_num_attempted_que(self):
        return self.answer_set.all().count()

    def get_num_total_que(self):
        return len(self.get_questions())

    def get_timeover_timestamp(self):
        return (self.created + self.exam.duration).timestamp()

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
