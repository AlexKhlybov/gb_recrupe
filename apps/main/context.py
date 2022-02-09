from apps.main.models import SiteConfiguration


def get_config(request):
    """
    Контекстный менеджер, на все страницы по умолчанию загружает конфиг сайта
    """
    config = SiteConfiguration.get_solo()
    return {"site_config": config,}
