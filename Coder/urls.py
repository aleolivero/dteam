from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from Coder import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),

    # STAFF
    path('players/', views.players_view, name='players_view'),
    path('playersAdd/', views.players_add, name='players_add'),
    path('playersEdit/<id>', views.players_edit, name='players_edit'),
    path('playersDelete/<id>', views.players_delete, name='players_delete'),

    path('answers/', views.answers_view, name='answers_view'),
    path('answersAdd/', views.answers_add, name='answers_add'),
    path('answersEdit/<id>', views.answers_edit, name='answers_edit'),
    path('answersDelete/<id>', views.answers_delete, name='answers_delete'),


    path('eventsClosed/<id>', views.events_closed, name='events_closed'),
    path('eventsOpen/<id>', views.events_open, name='events_open'),

    path('questions/', views.questions_view, name='questions_view'),
    path('questionsAdd/', views.questions_add, name='questions_add'),
    path('questionsEdit/<id>', views.questions_edit, name='questions_edit'),
    path('questionsDelete/<id>', views.questions_delete, name='questions_delete'),

    path('events/', views.events_view, name='events_view'),
    path('eventsAdd/', views.events_add, name='events_add'),
    path('eventsEdit/<id>', views.events_edit, name='events_edit'),
    path('eventsDelete/<id>', views.events_delete, name='events_delete'),

    path('questionRules/', views.questionRules_view, name='questionRules_view'),
    path('questionRulesAdd/', views.questionRules_add, name='questionRules_add'),
    path('questionRulesEdit/<id>', views.questionRules_edit, name='questionRules_edit'),
    path('questionRulesDelete/<id>', views.questionRules_delete, name='questionRules_delete'),
   
    # PLAYERS
    path('answersPlayerAdd/<id>', views.answersPlayer_add, name='answersPlayerAdd'),
    path('answersPlayerEdit/<id>', views.answersPlayer_edit, name='answersPlayerEdit'),
    path('answersPlayerDelete/<id>', views.answersPlayer_delete, name='answersPlayerDelete'),
    path('answersPlayerView/', views.answersPlayer_view, name='answersPlayerView'),

    path('eventsPlayerView/', views.eventsPlayer_view, name='eventsPlayerView'),
    path('eventsPlayerResult/<id>', views.eventsPlayer_result, name='eventsPlayerResult'),
    
    path('winnersPlayerView/', views.winnersPlayer_view, name='winnersPlayerView'),

    path('playerScorePlayerView/', views.playerScorePlayer_view, name='playerScorePlayerView'),

    path('questionsPlayer/', views.questionsPlayer_view, name='questionsPlayerView'),
    path('questionsPlayerAdd/', views.questionsPlayer_add, name='questionsPlayerAdd'),
    path('questionsPlayerEdit/<id>', views.questionsPlayer_edit, name='questionsPlayerEdit'),
    path('questionsPlayerDelete/<id>', views.questionsPlayer_delete, name='questionsPlayerDelete'),
    path('questionsPlayerResult/<id>', views.questionsPlayer_result, name='questionsPlayerResult'),

    path('questionsClosed/<id>', views.questions_closed, name='questions_closed'),
    path('questionsOpen/<id>', views.questions_open, name='questions_open'),
    path('questionsDetermined/<id>', views.questions_determined, name='questions_determined'),
    path('questionsUndetermined/<id>', views.questions_undetermined, name='questions_undetermined'),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('editAccount/', views.editAccount, name='editAccount'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('about/', views.about, name='about'),

    path('questionsPlayer/ajax/responded_players/<int:question_id>/', views.get_responded_players, name='ajax_responded_players'),




] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)