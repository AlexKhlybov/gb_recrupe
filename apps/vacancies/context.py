from apps.vacancies.models import VacancyFavorites


def favorite_vacancy(request):
    """
    Контекстный менеджер, на все страницы по умолчанию загружает кол-во
    не резюме в избранном
    """
    if request.user.is_authenticated:
        vacancy = VacancyFavorites.get_number_favorite(user=request.user)
        return {"favorite_vacancy": vacancy,}
    else:
        return {"favorite_vacancy": 0}
