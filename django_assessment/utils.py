from django.conf import settings


def res_upload_to(instance, filename):
    RES_UPLOAD_TO = getattr(settings, "RES_UPLOAD_TO", None)
    if RES_UPLOAD_TO:
        return RES_UPLOAD_TO(instance, filename)
    return filename
