from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.six import BytesIO
from PIL import Image
import pytest

from django_assessment.forms import AssessmentFormFactory
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

    def test_form_errors(self, db):
        q = f.QuestionFactory.create(
            assessment__title='Test Assessment',
            name='What does Django mean?',
            type__slug='long-text',
            varname='django_question',
            is_required=True
        )
        form = AssessmentFormFactory({}, question=q)

        assert not form.is_valid()
        assert form.errors == {
            'django_question': ['This field is required.']
        }


class TestAssessmentFileFormFactory:
    def _create_image(self, size=(100, 100), image_mode='RGB', image_format='PNG'):
        data = BytesIO()
        Image.new(image_mode, size).save(data, image_format)
        data.seek(0)

        return data

    def test_image_form_valid(self, img_question):
        img = self._create_image()
        v = {'django_question': SimpleUploadedFile('image_file', img.getvalue())}
        form = AssessmentFormFactory({}, v, question=img_question)

        assert form.is_valid(), form.errors

    def test_file_form_valid(self, doc_question):
        v = {'django_question': SimpleUploadedFile('image_file.doc', b'DOC')}
        form = AssessmentFormFactory({}, v, question=doc_question)

        assert form.is_valid(), form.errors
