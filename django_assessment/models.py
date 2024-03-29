from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property

from .utils import res_upload_to


class Assessment(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def _get_data(self, qs):
        data = {}
        for resp in qs:
            answer = resp.get_answer()
            if resp.question.type.slug == QuestionType.CHECKBOX and answer:
                answer = eval(answer)
            data[resp.question.varname] = answer
        return data

    def get_data_by_user(self, user):
        return self._get_data(self.responses.filter(user=user))

    def get_data_by_key(self, key):
        return self._get_data(self.responses.filter(key=key))


class QuestionType(models.Model):
    CHECKBOX = 'checkbox'
    DROPDOWN = 'dropdown'
    FILE_INPUT = 'file'
    IMAGE_INPUT = 'image'
    LONG_TEXT = 'long-text'
    RADIO_BUTTON = 'radio-button'
    SHORT_TEXT = 'short-text'

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class OptionSet(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    name = models.TextField()
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    varname = models.CharField(
        max_length=64,
        help_text="The name to use in order to build the form field."
    )
    option_set = models.ForeignKey(
        OptionSet, on_delete=models.SET_NULL, blank=True, null=True)
    is_required = models.BooleanField(
        default=False,
        help_text='Check this if question is required.'
    )
    placeholder = models.CharField(max_length=128, blank=True)
    help_text = models.CharField(max_length=256, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('assessment', 'varname')

    def __str__(self):
        return self.name

    @cached_property
    def is_image(self):
        return self.type.slug == QuestionType.IMAGE_INPUT

    @cached_property
    def is_file(self):
        return self.type.slug == QuestionType.FILE_INPUT


class Option(models.Model):
    option_set = models.ForeignKey(
        OptionSet,
        on_delete=models.CASCADE,
        related_name='options'
    )
    text = models.TextField(help_text='"The text of the option.')
    value = models.IntegerField(help_text='"The value of the option.')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    key = models.CharField(max_length=128, db_index=True, blank=True)
    answer = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=res_upload_to, max_length=255)
    file = models.FileField(blank=True, upload_to=res_upload_to, max_length=255)

    def get_answer(self):
        if self.question.is_image:
            return self.image

        if self.question.is_file:
            return self.file

        return self.answer
