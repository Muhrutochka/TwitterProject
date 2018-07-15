from django.shortcuts import render
from apptwitter.models import Messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings

# Сохраняем данные из формы в бaзу данных
def addMessage(request):
    context = listing(request)
    user = request.user
    if request.method == 'POST':
        addMessage = request.POST.get('Textarea1', '')
        if len(addMessage) < 250:
            i = Messages.objects.create(text=addMessage, user=user.id)
            i.save()
        else:
            messages.info(request, 'Вы превысили максимальный размер сообщения, он не должен быть больше 250 символов.')
    else:
        pass
    return render(request, 'user/main.html', context)

def retweet(request, id):
    message = Messages.objects.values_list().filter(id=id).values()
    user = request.user
    i = Messages.objects.create(text=message.text, user=user.id, parent=message.id)
    i.save()
    context = listing(request)
    return render(request, 'user/main.html', context)

# Формируем список для вывода на экран
def listing(request, *args):
    # Если запрашиваем список для пользователя то применяем фильтрацию
    if args:
        messages = Messages.objects.values_list().filter(user=args[0]).values()
    else:
        # messages = Messages.objects.values_list().values()
        messages = Messages.objects.values('id', 'user_id', 'user__first_name', 'text', )
        # qs = Messages.objects.get(id=1).user.first_name
        qs = Messages.objects.values('id', 'user_id', 'user__first_name')
        # print(qs)
        print(messages)
    paginator = Paginator(messages, 4)  # Show 4 items per page
    page = request.GET.get('page')
    ml = paginator.get_page(page)
    messageslist = {
        'context_value': ml,
    }
    # print(settings.AUTH_USER_MODEL)
    # print(messages)
    return messageslist


# Редактируем данные определенного пользователя
def userPage(request, user):
    context = listing(request, user)
    context['user'] = int(user)
    if request.method == 'POST':
        if request.POST.get('change'):
            pass # change()
        if request.POST.get('save'):
            # addMessage = request.POST.get('Textarea1', '')
            if str(addMessage) != '':
                i = Messages.objects.create(text=addMessage)
                i.save()
    else:
        pass
    return render(request, 'user/userpage.html', context)


def profileEdit(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        template = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        nickname = request.POST.get('save', '')
        errors = 0
        if nickname[0] in list('0123456789'):
            errors = errors + 1
        for letter in nickname:
            if not letter in template:
                errors = errors + 1
        if errors == 0:
            user.first_name = request.POST.get('save', '')
            print(nickname, request.user.id, user, user.first_name)
            user.save()
        print(errors)
    return render(request, 'user/profile.html')
