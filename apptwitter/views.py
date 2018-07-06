from django.shortcuts import render
from apptwitter.models import Messages


# Сохраняем данные из формы в бaзу данных
def addMessage(request):
    context = articles()
    if request.method == 'POST':
        addMessage = request.POST.get('Textarea1', '')
        if str(addMessage) != '':
            i = Messages.objects.create(text=addMessage)
            i.save()
    else:
        pass
    return render(request, 'user/main.html', context)


# Редактируем данные из базы
def articles():
    y = Messages.objects.values_list().values()
    messageslist = {
        'context_value': y,
    }
    return messageslist
