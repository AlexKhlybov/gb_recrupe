from dateparser import parse
import re
from django import template
from datetime import timezone, datetime


register = template.Library()


@register.filter(name="date_delta")
def date_delta(input_date: datetime) -> str:
    """
    Считает разницу в днях
    """
    delta = (datetime.now(timezone.utc) - input_date).days
    if delta == 0:
        return 'сегодня'
    elif delta == 1:
        return 'вчера'
    else:
        return input_date.date()
