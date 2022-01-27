from django_assessment.tests import factories as f
from django_assessment.utils import res_upload_to
from django.test.utils import override_settings


class TestUtils:
    def test_res_upload_to(self, db):
        def upload_to(instance, filename):
            return f"img/user-media/prj/{instance.id}/{filename}"

        with override_settings(RES_UPLOAD_TO=upload_to):
            u = f.UserFactory.create()
            filename = 'test.png'

            assert res_upload_to(u, filename) == f'img/user-media/prj/{u.id}/test.png'
