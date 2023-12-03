import re

from typing import Optional

from .enums import Locale

def as_valid_locale(locale: str) -> Optional[str]:
    """Converts the provided locale name to a name that is valid for use with the API,
    for example by returning ``en-US`` for ``en_US``.
    Returns ``None`` for invalid names.

    .. versionadded:: 2.5

    Parameters
    ----------
    locale: :class:`str`
        The input locale name.
    """
    # check for key first (e.g. `en_US`)
    if locale_type := Locale.__members__.get(locale):
        return locale_type.value

    # check for value (e.g. `en-US`)
    try:
        Locale(locale)
    except ValueError:
        pass
    else:
        return locale

    # didn't match, try language without country code (e.g. `en` instead of `en-US`)
    language = re.split(r"[-_]", locale)[0]
    if language != locale:
        return as_valid_locale(language)
    return None