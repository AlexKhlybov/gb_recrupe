
from django.shortcuts import render

from apps.companies.models import Company
from apps.news.models import News


def main_view(request):
    content = {
        'news': News.objects.all()[:2],
        'partners': Company.objects.filter(is_active=True)[:10],
    }

    return render(request, 'main/index.html', content)


def specification(request):
    return render(request, 'main/specification.html')


def posting_rules(request):
    return render(request, 'main/posting_rules.html')


