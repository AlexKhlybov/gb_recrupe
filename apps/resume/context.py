from apps.resume.models import ResumeFavorites


def favorite_resume(request):
    """
    Контекстный менеджер, на все страницы по умолчанию загружает кол-во
    не резюме в избранном
    """
    if request.user.is_authenticated:
        resume = ResumeFavorites.get_number_favorite(user=request.user)
        return {"favorite_resume": resume,}
    else:
        return {"favorite_resume": 0}
