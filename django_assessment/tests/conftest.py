import pytest

from django_assessment.tests import factories as f


@pytest.fixture
def img_question(db):
    q = f.QuestionFactory.create(
        assessment__title='Test Assessment',
        name='What does Django mean?',
        type__slug='image',
        varname='django_question',
        is_required=True
    )

    return q


@pytest.fixture
def doc_question(db):
    q = f.QuestionFactory.create(
        assessment__title='Test Assessment',
        name='What does Django mean?',
        type__slug='file',
        varname='django_question',
        is_required=True
    )

    return q
