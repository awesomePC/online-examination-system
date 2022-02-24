import random
from datetime import timedelta
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from users.models import Student

User = get_user_model()

A = "A"
B = "B"
C = "C"
D = "D"

ANSWER_CHOICES = [
    (A, A),
    (B, B),
    (C, C),
    (D, D),
]


def validate_max_duration(value):
    if value > timedelta(hours=23, minutes=59, seconds=59):
        raise ValidationError(
            "Maximum duration is 23 hours, 59 minutes and 59 seconds."
        )


def validate_min_duration(value):
    if value < timedelta(seconds=1):
        raise ValidationError("Minimum duration is 1 second.")


class Exam(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    duration = models.DurationField(
        default=timedelta(hours=1),
        help_text="In format hh:mm:ss",
        validators=[validate_max_duration, validate_min_duration],
    )
    passing_percentage = models.FloatField(default=0)
    active = models.BooleanField()
    show_result = models.BooleanField()

    class Meta:
        ordering = ("-created",)

    @admin.display(description="no. of questions")
    def get_num_questions(self):
        return self.question_set.filter(deleted=None).count()

    @admin.display(description="max marks")
    def get_max_marks(self):
        marks = 0
        for question in self.question_set.filter(deleted=None):
            marks += question.marks_on_correct_answer
        return marks

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
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, default=A)
    marks_on_correct_answer = models.FloatField(default=1)
    marks_on_wrong_answer = models.FloatField(default=0)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.question


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField(Question)
    created = models.DateTimeField(auto_now_add=True)
    submitted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created",)

    def get_questions(self):
        questions = list(self.exam.question_set.filter(created__lt=self.created))
        questions = [q for q in questions if not q.deleted or q.deleted > self.created]
        rand = random.Random(self.seed)
        rand.shuffle(questions)

        return questions

    @admin.display(description="no. of attempted questions")
    def get_num_attempted_que(self):
        return self.answer_set.all().count()

    @admin.display(description="no. of questions")
    def get_num_total_que(self):
        return len(self.get_questions())

    def get_timeover_timestamp(self):
        return (self.created + self.exam.duration).timestamp()

    @admin.display(description="marks")
    def get_marks(self):
        marks = 0
        for answer in self.answer_set.all():
            marks += answer.get_marks()
        return marks

    @admin.display(description="max marks")
    def get_max_marks(self):
        marks = 0
        for question in self.get_questions():
            marks += question.marks_on_correct_answer
        return marks

    @admin.display(description="pass", boolean=True)
    def get_passing_status(self):
        percentage = self.get_marks() / self.get_max_marks() * 100
        return percentage >= self.exam.passing_percentage

    def __str__(self):
        return self.exam.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, default=A)

    def get_answer_status(self):
        return self.answer == self.question.correct_answer

    def get_marks(self):
        if self.get_answer_status():
            return self.question.marks_on_correct_answer
        return self.question.marks_on_wrong_answer

    def __str__(self):
        return self.answer
