import factory
from django.contrib.auth.models import User

from django_assessment.models import (
    Assessment,
    Option,
    OptionSet,
    Question,
    QuestionType,
    Response
)


class AssessmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Assessment

    title = factory.Sequence(lambda n: f'Assessment-{n}')
    slug = factory.Sequence(lambda n: f'title-slug-{n}')


class QuestionTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = QuestionType

    name = factory.Sequence(lambda n: f'Question Type-{n}')
    slug = factory.Sequence(lambda n: f'question-type-{n}')


class OptionSetFactory(factory.DjangoModelFactory):
    class Meta:
        model = OptionSet

    name = factory.Sequence(lambda n: f'Option Set-{n}')


class OptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Option

    text = factory.Sequence(lambda n: f'Option-{n}')
    value = 1


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    assessment = factory.SubFactory(AssessmentFactory)
    name = factory.Sequence(lambda n: f'Test Question-{n}')
    type = factory.SubFactory(QuestionTypeFactory)
    varname = factory.Sequence(lambda n: f'question_{n}')


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "Test User"
    username = factory.Sequence(lambda n: f'username_{n}')
    email = factory.Sequence(lambda n: f'test{n}@example.com')
    password = 'sekret'


class ResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Response

    question = factory.SubFactory(QuestionFactory)
    assessment = factory.SubFactory(AssessmentFactory)
    user = factory.SubFactory(UserFactory)
