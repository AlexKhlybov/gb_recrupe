from apps.notify.models import Notify


def unread_msg(request):
    """
    Контекстный менеджер, на все страницы по умолчанию загружает кол-во
    не прочитанных сообений
    """
    if request.user.is_authenticated:
        unread = Notify.get_number_unread(request.user)
        return {"unread_msg": unread,}
    else:
        return {"unread_msg": 0}
