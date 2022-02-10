from apps.main.models import SiteConfiguration
from apps.resume.models import Resume
from apps.vacancies.models import Vacancy


def get_config(request):
    """Пробрасывает конфиг сайта"""
    config = SiteConfiguration.get_solo()
    return {"site_config": config,}

def get_all_complaint(request):
    pass
#     """Пробрасывает конфиг сайта"""
#     return Resume.get_complaint() + Vacancy.get_complaint()