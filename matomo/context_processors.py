from django.utils.safestring import mark_safe
from django.conf import settings
from matomo.tools import utils

def default_tracker(request):
    """
    Provide a default Matomo tracker.
    """
    matomo = utils.Matomo()



def dynamic_tracker(request):
    """
    Basically for testing at the moment.
    """
    matomo = utils.Matomo()
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
    # Normal matomo things
    return {'matomo': matomo, 'default_tracker': mark_safe(matomo.build_script())}