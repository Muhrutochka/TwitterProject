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
def listing(request):
    y = Messages.objects.values_list().values()
    paginator = Paginator(y, 4)  # Show 4 contacts per page
    page = request.GET.get('page')
    ml = paginator.get_page(page)
    messageslist = {
        'context_value': ml,
    }
    return messageslist

