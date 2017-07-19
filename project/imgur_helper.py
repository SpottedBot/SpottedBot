from imgurpython import ImgurClient
from django.conf import settings
from project.loghandler import LogHandler

logger = LogHandler(__name__).logger


def upload(file_path):
    try:
        client = ImgurClient(settings.IMGUR_CLIENT, settings.IMGUR_SECRET)
        data = client.upload_from_path(file_path, anon=True)
        return {"ok": True, "url": data['link']}
    except Exception as e:
        logger.exception("Erro na API do Imgur")
        return {"ok": False, "error": "Erro na API do Imgur"}
