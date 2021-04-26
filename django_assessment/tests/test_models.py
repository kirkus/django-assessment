from django_assessment.tests import factories as f
from django.core.files.uploadedfile import SimpleUploadedFile


class TestAssessment:
    def test_str(self):
        a = f.AssessmentFactory.build(title='First Assessment')

        assert str(a) == 'First Assessment'


class TestQuestionType:
    def test_str(self):
        qt = f.QuestionTypeFactory.build(name='Checkbox')

        assert str(qt) == 'Checkbox'



class TestOptionSet:
    def test_str(self):
        os = f.OptionSetFactory.build(name='Yes or No')

        assert str(os) == 'Yes or No'


class TestQuestion:
    def test_str(self, db):
        q = f.QuestionFactory.create(
            assessment__title='Test Assessment',
            name='What does Django mean?',
            type__slug='short-text'
        )

        assert str(q) == 'What does Django mean?'

    def test_is_image(self, img_question):
        assert img_question.is_image

    def test_is_file(self, doc_question):
        assert doc_question.is_file


class TestResponse:
    def test_get_answer(self, db):
        a = f.AssessmentFactory.create()
        q = f.QuestionFactory.create(
            assessment=a,
            name='Test Question',
            type__slug='short-text'
        )
        r = f.ResponseFactory.create(
            question=q,
            assessment=a,
            user=f.UserFactory.create(),
            answer='Test Answer'
        )

        assert r.get_answer() == 'Test Answer'

    def test_get_answer_for_image(self, db):
        a = f.AssessmentFactory.create()
        q = f.QuestionFactory.create(
            assessment=a,
            name='Test Question',
            type__slug='image'
        )
        r = f.ResponseFactory.create(
            question=q,
            assessment=a,
            user=f.UserFactory.create(),
            image=SimpleUploadedFile('image_file.png', b'PNG')
        )

        assert r.get_answer().name == 'image_file.png'

    def test_get_answer_for_file(self, db):
        a = f.AssessmentFactory.create()
        q = f.QuestionFactory.create(
            assessment=a,
            name='Test Question',
            type__slug='file'
        )
        r = f.ResponseFactory.create(
            question=q,
            assessment=a,
            user=f.UserFactory.create(),
            file=SimpleUploadedFile('doc_file.doc', b'DOC')
        )

        assert r.get_answer().name == 'doc_file.doc'
