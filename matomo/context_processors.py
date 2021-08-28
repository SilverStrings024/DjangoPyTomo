from analytics.models import Visitor
from tools import utils
from django.utils.safestring import mark_safe
from django.conf import settings
from .tools.utils import Matomo

def dynamic_tracker(request):
    matomo = Matomo()
    accept_bind = matomo.bind_event(elem_id='accept-tos-btn', callback='setCookie("can_track", "true")')
    reject_bind = matomo.bind_event(elem_id='reject-tos-btn', callback='setCookie("can_track", "false")')
    # Add the event bind loop to listen for consent
    matomo.add_script_piece(accept_bind, onload=True)
    matomo.add_script_piece(reject_bind, onload=True)
    matomo.add_cmd("requireConsent")
    matomo.add_cmd("requireCookieConsent")
    if settings.MATOMO_USE_BEACON:
        matomo.add_cmd("alwaysUseSendBeacon")
    if request.user.is_authenticated:
        matomo.add_cmd("setUserId", [request.user.full_name])
    elif utils.can_track(request):
        ip = utils.get_client_ip(request)
        try:
            visitor = Visitor.objects.get(ip=ip)
        except:
            visitor = Visitor(ip_address=ip)
            visitor.save()
        matomo.add_cmd("setUserId", [f"Visitor #{visitor.id}"])
    # Normal matomo things
    return {'matomo': matomo, 'default_tracker': mark_safe(matomo.build_script())}