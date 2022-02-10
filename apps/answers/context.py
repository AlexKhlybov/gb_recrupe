from apps.answers.models import VacancyAnswers
from apps.companies.models import Company


def empoyee_answers(request):
    """Пробрасывает в контекст кол-во откликов (СОИСКАТЕЛЬ)"""
    if request.user.is_authenticated:
        resume = VacancyAnswers.get_number_employee_answers(request.user.id)
        return {"my_answers_count": resume,}
    else:
        return {"my_answers_count": 0}
    
def company_answers(request):
    """Контекстный менеджер, на все страницы по умолчанию загружает кол-во откликов"""
    obj = Company.objects.filter(user=request.user.id)
    if request.user.is_authenticated and len(obj):
        resume = VacancyAnswers.get_number_company_answers(obj[0])
        return {"company_answers_count": resume,}
    else:
        return {"company_answers_count": 0}
    