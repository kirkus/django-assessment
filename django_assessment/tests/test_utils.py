from django.test.utils import override_settings

from django_assessment.utils import res_upload_to
from django_assessment.tests import factories as f


class TestUtils:
    def test_res_upload_to(self, db):
        instance = f.AssessmentFactory.create()
        filename = "file.png"

        assert res_upload_to(instance, filename) == "file.png"

    def test_res_upload_to_override(self, db):
        instance = f.AssessmentFactory.create()
        filename = "file.png"

        def upload_to(_instance, _filename):
            return f'path/to/my/file/{_instance.id}/{_filename}'

        with override_settings(RES_UPLOAD_TO=upload_to):
            assert res_upload_to(instance, filename) == upload_to(instance, filename)
