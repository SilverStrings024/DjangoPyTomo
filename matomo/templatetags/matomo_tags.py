from django.utils.safestring import mark_safe

from django.template import Library
register = Library()

@register.filter
def add_matomo_cmd(matomo, cmd):
    cmd.strip()
    split = [arg for arg in cmd.split(",")]
    if len(split) > 2:
        matomo.add_cmd(split[0], split[1:])
    else:
        matomo.add_cmd(split[0])
    return ""


@register.filter
def get_updated_tracker(matomo):
    return mark_safe(matomo.build_script())