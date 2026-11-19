import json
import urllib.request
import urllib.parse
from django.conf import settings


def verify_recaptcha(response_token, remote_ip=None):
    if not response_token:
        return False, "Iltimos, robot emasligingizni tasdiqlang (reCAPTCHA)."

    secret_key = getattr(
        settings,
        'RECAPTCHA_SECRET_KEY',
        '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    )
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = urllib.parse.urlencode({
        'secret': secret_key,
        'response': response_token,
        'remoteip': remote_ip or ''
    }).encode('utf-8')

    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('success'):
                return True, None
            return False, "reCAPTCHA tasdiqlanmadi. Qayta urinib ko‘ring."
    except Exception:
        # Test kaliti bilan DEBUG rejimida internet uzilsa yoki xatolik bo'lsa
        if settings.DEBUG and secret_key == '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe':
            return True, None
        return False, "reCAPTCHA serveriga ulanishda xatolik yuz berdi."
