from .models import Chat

def chats_not_read(request):
    
    if request.user.is_authenticated:

        chats_not_read = Chat.objects.exclude(readers=request.user)
        chats_not_read_ids = len([chat.id for chat in chats_not_read])
        
        return {'chats_not_read_ids': chats_not_read_ids}
    
    else:
        
        return {}