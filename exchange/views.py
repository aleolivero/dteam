from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import ChatForm
from exchange.models import Chat

# Create your views here.

def exchange_view(request): 
    params = {}

    chats = Chat.objects.all().order_by('date') 
    
    params['chats'] = chats


    if request.method == 'POST': 

        form = ChatForm(request.POST) 
        
        if form.is_valid(): 
            chat = form.save(commit=False) 
            chat.sender = request.user 
            chat.save() 
        
            return redirect('view') 

    else:     

        chats_not_read = Chat.objects.exclude(readers=request.user)
        chats_not_read_ids = [ chat.id for chat in chats_not_read ]

        for chat in chats_not_read:
            chat.readers.add(request.user)
        
        form = ChatForm()
     

    params['form'] = form
    params['chats_not_read_ids_mark'] = chats_not_read_ids

    return render(request, 'exchange_view.html', params)
