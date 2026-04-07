from django import template

register = template.Library()


@register.filter
def split(text, separator):
    """Split a string by separator."""
    return text.split(separator)


@register.filter
def get_user_avatar(user):
    """Get user avatar - profile photo if available, otherwise initials."""
    if user.profile_photo:
        return user.profile_photo.url
    return None


@register.filter
def get_user_initials(user):
    """Get user initials for avatar fallback."""
    return user.get_avatar_initials if hasattr(user, 'get_avatar_initials') else user.full_name[:2].upper()
