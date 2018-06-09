from imgurpython import ImgurClient
from django.conf import settings
from project.loghandler import LogHandler
from imgurpython.helpers.error import ImgurClientError
from django.forms import ValidationError

logger = LogHandler(__name__).logger


def upload(file_path):
    try:
        client = ImgurClient(settings.IMGUR_CLIENT, settings.IMGUR_SECRET)
        data = client.upload_from_path(file_path, anon=True)
        return_data = {"ok": True, "url": data['link']}
    except ImgurClientError as e:
        if "JSON decoding of response failed" in getattr(e, 'error_message', ""):
            return_data = ValidationError("Erro na API do Imgur. Tente outro anexo.")
        else:
            logger.exception("Erro na API do Imgur")
            return_data = ValidationError("Erro na API do Imgur")
    except Exception as e:
        logger.exception("Erro na API do Imgur")
        return_data = ValidationError("Erro na API do Imgur")
    finally:
        return return_data
