from django.shortcuts import render
from apptwitter.models import Messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Сохраняем данные из формы в бaзу данных
def addMessage(request):
    context = listing(request)

    if request.method == 'POST':
        addMessage = request.POST.get('Textarea1', '')
        if str(addMessage) != '':
            i = Messages.objects.create(text=addMessage)
            i.save()
    else:
        pass
    return render(request, 'user/main.html', context)


# Формируем список для вывода на экран
def listing(request, *args):
    # Если запрашиваем список для пользователя то применяем фильтрацию
    if args:
        messages = Messages.objects.values_list().filter(userid=args[0]).values()
    else:
        messages = Messages.objects.values_list().values()
    paginator = Paginator(messages, 4)  # Show 4 items per page
    page = request.GET.get('page')
    ml = paginator.get_page(page)
    messageslist = {
        'context_value': ml,
    }
    return messageslist


# Редактируем данные определенного пользователя
def userPage(request, userid):
    context = listing(request, userid)
    context['user_id'] = int(userid)
    if request.method == 'POST':
        if request.POST.get('change'):
            change()
        if request.POST.get('save'):
            addMessage = request.POST.get('Textarea1', '')
            if str(addMessage) != '':
                i = Messages.objects.create(text=addMessage)
                i.save()
    else:
        pass
    return render(request, 'user/userpage.html', context)

