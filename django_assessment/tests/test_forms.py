from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import pytest

from django_assessment.forms import AssessmentFormFactory, ResponseForm
from django_assessment.models import Response
from django_assessment.tests import factories as f


class TestAssessmentFormFactory:
    @pytest.mark.parametrize('q_type_slug', ['checkbox', 'dropdown', 'radio-button'])
    def test_form_valid(self, db, q_type_slug):
        option_set = f.OptionSetFactory.create()
        for i in range(3):
            f.OptionFactory.create(value=i, option_set=option_set)
        q = f.QuestionFactory.create(
            assessment__title='Test Assessment',
            name='What does Django mean?',
            type__slug=q_type_slug,
            varname='django_question',
            option_set=option_set,
            is_required=True
        )
        v = [2] if q_type_slug == 'checkbox' else 2
        form = AssessmentFormFactory({'django_question': v}, question=q)

        assert form.is_valid(), form.errors


class TestAssessmentTextFormFactory:
    @pytest.mark.parametrize('q_type_slug', ['short-text', 'long-text'])
    def test_form_valid(self, db, q_type_slug):
        q = f.QuestionFactory.create(
            assessment__title='Test Assessment',
            name='What does Django mean?',
            type__slug=q_type_slug,
            varname='django_question'
        )
        form = AssessmentFormFactory({'django_question': 'Test'}, question=q)

        assert form.is_valid(), form.errors

    def test_form_errors(self, question):
        form = AssessmentFormFactory({}, question=question)

        assert not form.is_valid()
        assert form.errors == {
            'test_question': ['This field is required.']
        }


class TestAssessmentFileFormFactory:
    def _create_image(self, size=(100, 100), image_mode='RGB', image_format='PNG'):
        data = BytesIO()
        Image.new(image_mode, size).save(data, image_format)
        data.seek(0)

        return data

    def test_image_form_valid(self, img_question):
        img = self._create_image()
        v = {'django_question': SimpleUploadedFile('image_file.png', img.getvalue())}
        form = AssessmentFormFactory({}, v, question=img_question)

        assert form.is_valid(), form.errors

    def test_file_form_valid(self, doc_question):
        v = {'django_question': SimpleUploadedFile('image_file.doc', b'DOC')}
        form = AssessmentFormFactory({}, v, question=doc_question)

        assert form.is_valid(), form.errors


class TestResponseForm:
    def test_form_save(self, question):
        user = f.UserFactory.create()
        assessment = question.assessment
        data = {
            'test_question': 'answer 1',
        }
        form = ResponseForm(data=data, assessment=assessment, user=user)

        assert form.is_valid(), form.errors

        form.save()
        response = Response.objects.first()

        assert response.answer == 'answer 1'
        assert response.user == user
        assert response.assessment == assessment

    def test_form_errors(self, question):
        u = f.UserFactory.create()
        data = {
            'test_question': ''
        }
        form = ResponseForm(data=data, assessment=question.assessment, user=u)

        assert not form.is_valid()
        assert form.errors == [
            {'test_question': ['This field is required.']}
        ]

    def test_form_has_error(self, question):
        u = f.UserFactory.create()
        data = {
            'test_question': ''
        }
        form = ResponseForm(data=data, assessment=question.assessment, user=u)

        assert not form.is_valid()
        assert form.has_error()
