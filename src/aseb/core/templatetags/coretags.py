import datetime
from pprint import pformat
from typing import Any

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(name="pprint")
def pprint_tag(value: Any) -> str:
    if hasattr(value, "__dict__"):
        out = pformat(value.__dict__, indent=2)
    else:
        out = pformat(value, indent=2)

    return mark_safe(
        "\n".join(
            [
                '<pre style="outline: 1px solid orange;">',
                escape(repr(value)),
                "\n",
                escape(out),
                "</pre>",
            ]
        )
    )


@register.simple_tag
def tomorrow(exp: str):
    return (datetime.date.today() + datetime.timedelta(days=1)).strftime(exp)


@register.simple_tag
def nextweek(exp: str):
    return (datetime.date.today() + datetime.timedelta(days=7)).strftime(exp)


@register.simple_tag
def daysfromnow(days: int, exp: str):
    return (datetime.date.today() + datetime.timedelta(days=days)).strftime(exp)
