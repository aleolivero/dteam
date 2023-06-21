from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import Players, Answers, Questions, PlayerScore, Event, QuestionsRules
from .forms import FormPlayers, FormAnswersPlayer, FormQuestions, SignUpForm, FormEditAccount, FormProfile, FormSearchQuestions, FormSearchPlayers, FormSearchAnswers,FormQuestionsPlayers,FormAnswers, FormSearchQuestionsRules, FormQuestionsRules, FormSearchEvents,FormEvents
from django.db.models import Q, F, FloatField, ExpressionWrapper, DateField, CharField,Exists, OuterRef, Prefetch, Sum,Subquery, Sum
from django.db.models.functions import Cast, Abs, Coalesce
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

import os
# Create your views here.

def is_staff(user):
    return user.is_authenticated and user.is_staff

def calculateQuestionPoints(questionID, params):
    _points = 0
    _question = Questions.objects.get(id=questionID)
    _rules = _question.question_rule
    
    if params['exact_answer']:
        _points += _rules.bonus_exact_answer
    
    if params['draw']:
        if _rules.allows_draw:
            _points += _rules.points_draw
        else:
            _points = 0
    else:
        _points += _rules.points
    
    return _points

def calculateQuestionResult(questionID):

    params = {}

    _question = Questions.objects.get(id=questionID)

    _answers = Answers.objects.filter(question=_question).annotate(
        closest=ExpressionWrapper( Abs(F('answer') - F('question__correct_answer')), output_field=FloatField())
    ).order_by('closest')
    
    _winner_value = _answers.first().answer if _answers else None
    _answers_winner = _answers.filter(answer=_winner_value)

    _draw = len(_answers_winner) > 1
    _exact_answer = _winner_value == _question.correct_answer

    params['question'] = _question
    params['winner'] = _answers_winner
    params['answers'] = _answers
    params['parameters_result'] = {'draw':_draw,'exact_answer':_exact_answer}

    params['points'] = calculateQuestionPoints(questionID, params['parameters_result'])

    return params

def anotateQuestionResult(params):
    
    for winner in params['winner']:
        _newScore = PlayerScore(
            winner_answer = winner,
            points = params['points']
        )
        _newScore.save()

def dropQuestionResult(id):

    _scores = PlayerScore.objects.filter(winner_answer__question__id = id )

    for _score in _scores:
        _score.delete()

@login_required
def index(request):

    params = {}

    return render(request,'indexPlayer.html',params)

@user_passes_test(is_staff,login_url='/')
def players_view(request):
    params = {}

    if request.method == 'POST':

        form = FormSearchPlayers(request.POST)
        print(request.POST)
        _first_name = request.POST['first_name']
        _last_name = request.POST['last_name']
        _date_birth = request.POST['date_birth']
        _phone = request.POST['phone']
        _adress = request.POST['adress'] 
        _city = request.POST['city']
        _state = request.POST['state']
        _country = request.POST['country']

        params['players'] = Players.objects.filter(
            first_name__icontains = _first_name,
            last_name__icontains = _last_name,
            date_birth__icontains = _date_birth,
            phone__icontains = _phone,
            adress__icontains = _adress,
            city__icontains = _city,
            state__icontains = _state,
            country__icontains = _country,

        ).annotate(date_birth_str=Cast('date_birth', output_field=CharField()),)

        params['form'] = form

        return render(request,'players_view.html',params)
    
    else:
        
        form = FormSearchPlayers()
        
        params['players'] = Players.objects.all().annotate(date_birth_str=Cast('date_birth', output_field=CharField()),)
        params['form'] = form

    return render(request,'players_view.html',params)

@user_passes_test(is_staff,login_url='/')
def players_add(request):

    params = {}

    if request.method == 'POST':

        form = FormPlayers(request.POST, request.FILES)

        params['form'] = form
        if form.is_valid():
            _user = form.cleaned_data['user']
            _image = form.cleaned_data['image']
            _first_name = form.cleaned_data['first_name']
            _last_name = form.cleaned_data['last_name']
            _date_birth = form.cleaned_data['date_birth']
            _phone = form.cleaned_data['phone']
            _adress = form.cleaned_data['adress']
            _city = form.cleaned_data['city']
            _state = form.cleaned_data['state']
            _country = form.cleaned_data['country']

            _newPlayer = Players(
                user = _user,
                image = _image,
                first_name = _first_name,
                last_name = _last_name,
                date_birth = _date_birth,
                phone = _phone,
                adress = _adress,
                city = _city,
                state = _state,
                country = _country,
                )

            _newPlayer.save()

            return HttpResponseRedirect('/Coder/players')
        else:
            return render(request,'players_add.html', params)
    
    else:
        form = FormPlayers()
        params['form'] = form
        
        return render(request,'players_add.html', params)

@user_passes_test(is_staff,login_url='/')
def players_edit(request, id):

    params = {}

    _player = Players.objects.get(id = id)

    if request.method == 'POST':

        form = FormPlayers(request.POST, request.FILES)
        form.fields['image'].required = False

        print(request.FILES)
        print(bool(request.FILES))
        
        params['form'] = form

        if form.is_valid():
            if request.FILES:
                _player.image.delete()
                _player.image = form.cleaned_data['image']

            _player.first_name = form.cleaned_data['first_name']
            _player.last_name = form.cleaned_data['last_name']
            _player.date_birth = form.cleaned_data['date_birth']
            _player.phone = form.cleaned_data['phone']
            _player.adress = form.cleaned_data['adress']
            _player.city = form.cleaned_data['city']
            _player.state = form.cleaned_data['state']
            _player.country = form.cleaned_data['country']

            _player.save()

            return redirect(reverse('players_view'))
        else:

            return render(request,'players_edit.html', params)
    
    else:
        form = FormPlayers(instance=_player)
        form.fields['image'].required = False
        params['form'] = form
        
        return render(request,'players_edit.html', params)

@user_passes_test(is_staff,login_url='/')
def players_delete(request,id):

    player = Players.objects.get(id=id)
    player = player.delete()
    
    return redirect(reverse('players_view'))

@user_passes_test(is_staff,login_url='/')
def questions_view(request):
    params = {}

    if request.method == 'POST':

        print(request.POST)
        form = FormSearchQuestions(request.POST)

        _title = request.POST['title']
        _category = request.POST['category']
        _date = request.POST['date']
        _author = request.POST['author']       
        _question = request.POST['question']
        _correct_answer = request.POST['correct_answer']
        _status = request.POST['status']
        _event = request.POST['event']
        _question_rule = request.POST['question_rule']
        _result =  request.POST['result']

        params['questions'] = Questions.objects.filter(
            title__icontains = _title,
            category__icontains = _category,
            date__icontains = _date,
            author__user__id__icontains = _author,
            question__icontains = _question,
            correct_answer__icontains = _correct_answer,
            status__icontains = _status,
            result__icontains = _result,
            event__id__icontains = _event,
            question_rule__id__icontains = _question_rule,
        ).order_by('-date')

        params['form'] = form

        return render(request,'questions_view.html',params)
    
    else:
        
        form = FormSearchQuestions()
        
        params['questions'] = Questions.objects.all().order_by('-date')
        params['form'] = form

    return render(request,'questions_view.html',params)

@login_required
def questionsPlayer_view(request):
    params = {}

    if request.method == 'POST':

        print(request.POST)
        form = FormSearchQuestions(request.POST)

        _title = request.POST['title']
        _category = request.POST['category']
        _date = request.POST['date']
        _author = request.POST['author']       
        _question = request.POST['question']
        _correct_answer = request.POST['correct_answer']
        _status = request.POST['status']
        _event = request.POST['event']
        _question_rule = request.POST['question_rule']
        _result =  request.POST['result']

        params['questions'] = Questions.objects.filter(
            title__icontains = _title,
            category__icontains = _category,
            date__icontains = _date,
            author__user__id__icontains = _author,
            question__icontains = _question,
            correct_answer__icontains = _correct_answer,
            status__icontains = _status,
            result__icontains = _result,
            event__id__icontains = _event,
            question_rule__id__icontains = _question_rule,
        ).order_by('-date')

        params['form'] = form

        return render(request,'questionsPlayer_view.html',params)
    
    else:
        
        form = FormSearchQuestions()
        
        params['questions'] = Questions.objects.filter(author__user = request.user).order_by('-date')
        params['form'] = form

    return render(request,'questionsPlayer_view.html',params)

@user_passes_test(is_staff,login_url='/')
def questions_add(request):
    params = {}

    # User sends data to server
    if request.method == 'POST':

        form = FormQuestions(request.POST)

        #Data valid
        if form.is_valid():

            _title = form.cleaned_data['title']
            _category = form.cleaned_data['category']
            _question = form.cleaned_data['question']
            _correct_answer = form.cleaned_data['correct_answer']
            _date = form.cleaned_data['date']
            _author = form.cleaned_data['author']
            # _status = form.cleaned_data['status']
            _event = form.cleaned_data['event']
            _question_rule = form.cleaned_data['question_rule']

            _newQuestion = Questions(
                title = _title,
                category = _category,
                question = _question, 
                correct_answer = _correct_answer,
                date = _date,
                author = _author,
                event = _event,
                question_rule = _question_rule
                )

            _newQuestion.save()

            return HttpResponseRedirect('/Coder/questions')

        
        #Data no valid
        else:
            params['form'] = form

            return render(request,'questions_add.html',params)


    # User asks data to server
    else:
        
        form = FormQuestions()
        
        params['form'] = form

        return render(request,'questions_add.html',params)

@login_required
def questionsPlayer_add(request):
    params = {}

    # User sends data to server
    if request.method == 'POST':

        form = FormQuestionsPlayers(request.POST)

        #Data valid
        if form.is_valid():

            _title = form.cleaned_data['title']
            _category = form.cleaned_data['category']
            _question = form.cleaned_data['question']
            _correct_answer = form.cleaned_data['correct_answer']
            _date = form.cleaned_data['date']
            _author = Players.objects.get(user=request.user)
            # _status = form.cleaned_data['status']
            _event = form.cleaned_data['event']
            _question_rule = form.cleaned_data['question_rule']


            _newQuestion = Questions(
                title = _title,
                category = _category,
                question = _question, 
                correct_answer = _correct_answer,
                date = _date,
                author = _author,
                event = _event,
                question_rule = _question_rule
                )

            _newQuestion.save()

            return redirect(reverse('questionsPlayerView'))

        
        #Data no valid
        else:
            params['form'] = form

            return render(request,'questionsPlayer_add.html',params)


    # User asks data to server
    else:
        
        form = FormQuestionsPlayers()
        
        params['form'] = form

        return render(request,'questionsPlayer_add.html',params)

@user_passes_test(is_staff,login_url='/')
def questions_edit(request, id):

    params = {}
    _question = Questions.objects.get(id=id)

    if request.method == 'POST':

        form = FormQuestions(request.POST)
        
        params['form'] = form

        if form.is_valid():
            _question.title = form.cleaned_data['title']
            _question.category = form.cleaned_data['category']
            _question.question = form.cleaned_data['question']
            _question.correct_answer = form.cleaned_data['correct_answer']
            _question.date = form.cleaned_data['date']
            _question.author = form.cleaned_data['author']
            _question.event = form.cleaned_data['event']
            _question.question_rule = form.cleaned_data['question_rule']
            _question.save()

            return redirect(reverse('questions_view'))
        else:

            return render(request,'questions_edit.html', params)
    
    else:
        form = FormQuestions(instance=_question)
        
        params['form'] = form
        
        return render(request,'questions_edit.html', params)

@login_required
def questionsPlayer_edit(request, id):

    params = {}
    _question = Questions.objects.get(id=id)

    if request.method == 'POST':

        form = FormQuestionsPlayers(request.POST)
        
        params['form'] = form

        if form.is_valid():
            _question.title = form.cleaned_data['title']
            _question.category = form.cleaned_data['category']
            _question.question = form.cleaned_data['question']
            _question.correct_answer = form.cleaned_data['correct_answer']
            _question.date = form.cleaned_data['date']
            _question.author = Players.objects.get(user=request.user)
            _question.event = form.cleaned_data['event']
            _question.question_rule = form.cleaned_data['question_rule']
            _question.save()

            return redirect(reverse('questionsPlayerView'))
        else:

            return render(request,'questionsPlayer_edit.html', params)
    
    else:
        form = FormQuestionsPlayers(instance=_question)
        
        params['form'] = form
        
        return render(request,'questionsPlayer_edit.html', params)

@user_passes_test(is_staff,login_url='/')
def questions_delete(request,id):
    
    question = Questions.objects.get(id=id)
    question = question.delete()
    
    return redirect(reverse('questions_view'))

@login_required
def questionsPlayer_delete(request,id):
    
    question = Questions.objects.get(id=id)
    question = question.delete()
    
    return redirect(reverse('questionsPlayerView'))

@login_required
def questions_determined(request,id):
    
    question = Questions.objects.get(id=id)
    question.result = 'determined'
    question.save()

    params = calculateQuestionResult(id)
    anotateQuestionResult(params)

    if request.user.is_staff:
        return redirect(reverse('questions_view'))

    return redirect(reverse('questionsPlayerView'))

@login_required
def questions_undetermined(request,id):
    
    question = Questions.objects.get(id=id)
    question.result = 'undetermined'
    question.save()
    dropQuestionResult(id)
    
    if request.user.is_staff:
        return redirect(reverse('questions_view'))

    return redirect(reverse('questionsPlayerView'))

@login_required
def questions_closed(request,id):
    
    _question = Questions.objects.get(id=id)
    _question.status = 'closed'
    _question.save()

    list_answers = Answers.objects.filter(question=_question)
  
    if request.user.is_staff:
        return redirect(reverse('questions_view'))

    return redirect(reverse('questionsPlayerView'))

@login_required
def questions_open(request,id):
    
    question = Questions.objects.get(id=id)
    question.status = 'open'
    question.save()
    
    if request.user.is_staff:
        return redirect(reverse('questions_view'))

    return redirect(reverse('questionsPlayerView'))

@login_required
def questionsPlayer_result(request,id):
    
    params = calculateQuestionResult(id)
   
    return render(request,'questionsPlayer_result.html',params)

@user_passes_test(is_staff,login_url='/')
def answers_view(request):
    params = {}

    if request.method == 'POST':

        form = FormSearchAnswers(request.POST)

        _event = request.POST['event']
        # _question = request.POST['question']
        _question_text = request.POST['question_text']
        _answer = request.POST['answer']
        _player = request.POST['player']

        params['answers'] = Answers.objects.filter(
           player__id__icontains = _player ,
           answer__icontains = _answer,
           question__question__icontains = _question_text,
           question__event__id__icontains = _event

        )

        params['form'] = form

        return render(request,'answers_view.html',params)
    
    else:
        
        form = FormSearchAnswers()
        
        params['answers'] = Answers.objects.all().order_by('-id')
        params['form'] = form

    return render(request,'answers_view.html',params)

@user_passes_test(is_staff,login_url='/')
def answers_add(request):
    params = {}

    if request.method == 'POST':

        form = FormAnswers(request.POST)

        if form.is_valid():

            _question = form.cleaned_data['question']
            _answer = form.cleaned_data['answer']
            _player = form.cleaned_data['player']

            _newAnswer = Answers(question = _question, 
                                 answer = _answer, 
                                 player = _player,
                                )

            _newAnswer.save()

            return redirect(reverse('answers_view'))

        else:
            params['form'] = form

            return render(request,'answers_add.html',params)

    else:
        
        form = FormAnswers()
        
        params['form'] = form

        return render(request,'answers_add.html',params)

@user_passes_test(is_staff,login_url='/')
def answers_edit(request, id):
    params = {}
    _answer = Answers.objects.get(pk=id)

    if request.method == 'POST':

        form = FormAnswers(request.POST,)

        if form.is_valid():

            _answer.player = form.cleaned_data['player']
            _answer.question = form.cleaned_data['question']
            _answer.answer = form.cleaned_data['answer']

            _answer.save()

            return redirect(reverse('answers_view'))

        else:
            params['form'] = form

            return render(request,'answers_edit.html',params)

    else:
        
        form = FormAnswers(instance=_answer,)
        
        params['form'] = form

        return render(request,'answers_edit.html',params)

@user_passes_test(is_staff,login_url='/')
def answers_delete(request, id):
    params = {}

    _answer = Answers.objects.get(pk=id)
    _answer.delete()
    
    return redirect(reverse('answers_view'))

@login_required
def answersPlayer_view(request):
    params = {}

    if request.method == 'POST':

        form = FormSearchAnswers(request.POST)
        
        _event = request.POST['event']
        # _question = request.POST['question']
        _question_text = request.POST['question_text']
        _answer = request.POST['answer']
        # _player = request.POST['player']

        params['answers'] = Answers.objects.filter(
           player__user = request.user ,
           answer__icontains = _answer,
           question__question__icontains = _question_text,
           question__event__id__icontains = _event

        )

        params['form'] = form

        return render(request,'answersPlayer_view.html',params)
    
    else:
        
        form = FormSearchAnswers()
        
        params['answers'] = Answers.objects.filter(player__user = request.user)
        params['form'] = form

    return render(request,'answersPlayer_view.html',params)

@login_required
def answersPlayer_add(request, id):
    params = {}
    _question = Questions.objects.get(id=id)

    # User sends data to server
    if request.method == 'POST':


        form = FormAnswersPlayer(request.POST,question=_question)

        #Data valid
        if form.is_valid():

            _question = form.cleaned_data['question']
            _answer = form.cleaned_data['answer']
            _player = Players.objects.get(user=request.user)

            _newAnswer = Answers(question = _question, 
                                 answer = _answer, 
                                 player = _player,
                                )

            _newAnswer.save()

            return redirect(reverse('eventsPlayerView'))

        
        #Data no valid
        else:
            params['form'] = form

            return render(request,'answersPlayer_add.html',params)


    # User asks data to server
    else:
        
        form = FormAnswersPlayer(question=_question)
        
        params['form'] = form

        return render(request,'answersPlayer_add.html',params)

@login_required
def answersPlayer_edit(request, id):
    params = {}
    _answer = Answers.objects.get(pk=id)
    _question = _answer.question
    

    # User sends data to server
    if request.method == 'POST':


        form = FormAnswersPlayer(request.POST,question=_question)

        #Data valid
        if form.is_valid():

            _answer.answer = form.cleaned_data['answer']

            _answer.save()

            return redirect(reverse('eventsPlayerView'))

        
        #Data no valid
        else:
            params['form'] = form

            return render(request,'answersPlayer_edit.html',params)


    # User asks data to server
    else:
        
        form = FormAnswersPlayer(instance=_answer,question=_question)
        
        params['form'] = form

        return render(request,'answersPlayer_edit.html',params)

@login_required
def answersPlayer_delete(request, id):
    params = {}

    _answer = Answers.objects.get(pk=id)
    _answer.delete()
    
    return redirect(reverse('eventsPlayerView'))

@login_required
def eventsPlayer_view(request):
    params = {}

    _events = Event.objects.all()
    _event_questions = {
        event: Questions.objects.filter(event=event).order_by('-date').annotate(has_answer=Exists(Answers.objects.filter(question=OuterRef('pk'), player__user=request.user))).prefetch_related(Prefetch('answers_set', queryset=Answers.objects.filter(player__user=request.user), to_attr='user_answers'))
        for event in _events
    }


    params['events'] = _events
    params['event_questions'] = _event_questions


    return render(request,'eventsPlayer_view.html',params)

@login_required
def eventsPlayer_result(request, id):
    params = {}
    
    _event = Event.objects.get(pk=id)





    # Creamos una subconsulta que sumará los puntos para un jugador determinado.
    player_scores_subquery = PlayerScore.objects.filter(
        winner_answer__player=OuterRef('pk'),  # Referimos al 'pk' (clave primaria) del jugador en la consulta principal.
        winner_answer__question__event__id=id
    ).values(
        'winner_answer__player'  # Agrupamos por jugador.
    ).annotate(
        total_points=Sum('points')  # Sumamos los puntos.
    ).values('total_points')  # Seleccionamos solo la suma de puntos.

    players_with_points = Players.objects.annotate(
    total_points=Coalesce(
        Subquery(player_scores_subquery),  # Aquí usamos la subconsulta.
        0.0  # Si un jugador no tiene puntos (i.e., la subconsulta no devuelve nada), usamos cero.
    )
    ).order_by('-total_points')

    # _scores = PlayerScore.objects.filter(winner_answer__question__event__id=id).values('winner_answer__player').annotate(total_points=Sum('points')).order_by('-total_points')
    
    # players_with_points = []

    # for score in _scores:
    #     player = Players.objects.get(pk=score['winner_answer__player'])
    #     total_points = score['total_points']
    #     players_with_points.append({'player':player, 'total_points':total_points})


    params['event'] = _event
    params['scores'] = players_with_points
    params['podium'] = players_with_points[0:3]
    

    return render(request,'eventsPlayer_result.html',params)

@login_required
def playerScorePlayer_view(request):
    params = {}

    _events = Event.objects.all()
    _event_scores = {
        event: PlayerScore.objects.filter(winner_answer__question__event=event).order_by('-winner_answer__question__date')
        for event in _events
    }


    params['events'] = _events
    params['event_scores'] = _event_scores


    return render(request,'playerScorePlayer_view.html',params)

@login_required
def editAccount(request):

    params = {}
    user = request.user

    if request.method == 'POST':
        
        form = FormEditAccount(request.POST)

        if form.is_valid():
            
            _user = form.cleaned_data
            
            user.email = _user['email']

            user.password1 = _user['password1']

            user.password2 = _user['password2']

            user.save()

            return redirect(reverse('index'))

        else:

            return render(request,'editAccount.html', params)
            
    
    else:
        form = FormEditAccount(instance=user)
        
        params['form'] = form
        
        return render(request,'editAccount.html', params)

@login_required
def editProfile(request):
    params = {}

    _player = Players.objects.get(user = request.user)

    if request.method == 'POST':

        form = FormProfile(request.POST, request.FILES)
        form.fields['image'].required = False

        params['form'] = form

        if form.is_valid():
            if request.FILES:
                _player.image.delete()
                _player.image = form.cleaned_data['image']

            _player.first_name = form.cleaned_data['first_name']
            _player.last_name = form.cleaned_data['last_name']
            _player.date_birth = form.cleaned_data['date_birth']
            _player.phone = form.cleaned_data['phone']
            _player.adress = form.cleaned_data['adress']
            _player.city = form.cleaned_data['city']
            _player.state = form.cleaned_data['state']
            _player.country = form.cleaned_data['country']

            _player.save()

            return redirect(reverse('index'))
        else:

            return render(request,'editProfile.html', params)
    
    else:
        form = FormProfile(instance=_player)
        form.fields['image'].required = False
        params['form'] = form
        
        return render(request,'editProfile.html', params)

@login_required
def events_closed(request,id):
    
    _event = Event.objects.get(id=id)
    _event.status = 'closed'
    _event.save()

    return redirect(reverse('eventsPlayerView'))

@login_required
def events_open(request,id):
    
    _event = Event.objects.get(id=id)
    _event.status = 'open'
    _event.save()

    return redirect(reverse('eventsPlayerView'))

def signin(request):
    
    if request.method == 'POST':
        
        params = {}

        form = AuthenticationForm(request, data = request.POST)

        params['form'] = form

        if form.is_valid():

            _data = form.cleaned_data
            
            _username = _data['username']

            _password = _data['password']

            _user = authenticate(username=_username, password = _password)

            if _user is not None:

                login(request,_user)
                
                return redirect(reverse('index'))

            else:
                
                params['message'] = 'User or password incorrect.'

                return render(request, 'signin.html',params)
        
        else:
            params['message'] = 'User or password incorrect.'

            return render(request, 'signin.html',params)
        
    else:
        
        params = {}

        form = AuthenticationForm()
        
        params['form'] = form
        params['signup_success'] = request.GET.get('signup_success', None)

        return render(request,'signin.html', params)

def signup(request):
    if request.method == 'POST':
        
        params = {}

        form = SignUpForm(request.POST)

        params['form'] = form


        if form.is_valid():

            params['signup'] = True

            form.save()

            return redirect(reverse('signin')+ '?signup_success=1')

        
        else:

            return render(request, 'signup.html',params)
        
    else:
        
        params = {}
        
        form = SignUpForm()
        
        params['form'] = form

        return render(request,'signup.html', params)
    
def about(request):

    params = {}

    return render(request,'about.html',params)    


@user_passes_test(is_staff,login_url='/')
def questionRules_view(request):
    params = {}

    if request.method == 'POST':

        form = FormSearchQuestionsRules(request.POST)
        _name = request.POST['name']
        _description = request.POST['description']
        _points = request.POST['points']
        # _bonus_exact_answer = request.POST['bonus_exact_answer']
        # _allows_draw = request.POST['allows_draw']
        # _allows_wildcard = request.POST['allows_wildcard'] 
        # _points_draw = request.POST['points_draw']

        params['questionRules'] = QuestionsRules.objects.filter(
            name__icontains = _name,
            
            description__icontains = _description,
            points__icontains = _points,
            # bonus_exact_answer__icontains = _bonus_exact_answer,
            # allows_draw__icontains = _allows_draw,
            # allows_wild_card__icontains = _allows_wildcard,
            # points_draw__icontains = _points_draw,

        )

        params['form'] = form

        return render(request,'questionRules_view.html',params)
    
    else:
        
        form = FormSearchQuestionsRules()
        
        params['questionRules'] = QuestionsRules.objects.all()
        params['form'] = form

    return render(request,'questionRules_view.html',params)

@user_passes_test(is_staff,login_url='/')
def questionRules_add(request):

    params = {}

    if request.method == 'POST':

        form = FormQuestionsRules(request.POST)

        params['form'] = form

        if form.is_valid():
            _name = form.cleaned_data['name']
            _description = form.cleaned_data['description']
            _points = form.cleaned_data['points']
            _bonus_exact_answer = form.cleaned_data['bonus_exact_answer']
            _allows_draw = form.cleaned_data['allows_draw']
            _allows_wildcard = form.cleaned_data['allows_wildcard']
            _points_draw = form.cleaned_data['points_draw']

            _newQuestionRule = QuestionsRules(
                name = _name,
                description = _description,
                points = _points,
                bonus_exact_answer = _bonus_exact_answer,
                allows_draw = _allows_draw,
                allows_wildcard = _allows_wildcard,
                points_draw = _points_draw,
                )

            _newQuestionRule.save()

            return HttpResponseRedirect('/Coder/questionRules')
        else:
            return render(request,'questionRules_add.html', params)
    
    else:
        form = FormQuestionsRules()
        params['form'] = form
        
        return render(request,'questionRules_add.html', params)

@user_passes_test(is_staff,login_url='/')
def questionRules_edit(request, id):

    params = {}

    _questionRule = QuestionsRules.objects.get(id = id)

    if request.method == 'POST':

        form = FormQuestionsRules(request.POST)

        params['form'] = form

        if form.is_valid():

            _questionRule.name = form.cleaned_data['name']
            _questionRule.description = form.cleaned_data['description']
            _questionRule.points = form.cleaned_data['points']
            _questionRule.bonus_exact_answer = form.cleaned_data['bonus_exact_answer']
            _questionRule.allows_draw = form.cleaned_data['allows_draw']
            _questionRule.allows_wildcard = form.cleaned_data['allows_wildcard']
            _questionRule.points_draw = form.cleaned_data['points_draw']

            _questionRule.save()

            return redirect(reverse('questionRules_view'))
        else:

            return render(request,'questionRules_edit.html', params)
    
    else:
        form = FormQuestionsRules(instance=_questionRule)
        params['form'] = form
        
        return render(request,'questionRules_edit.html', params)

@user_passes_test(is_staff,login_url='/')
def questionRules_delete(request,id):

    questionRule = QuestionsRules.objects.get(id=id)
    questionRule = questionRule.delete()
    
    return redirect(reverse('questionRules_view'))

@user_passes_test(is_staff,login_url='/')
def events_view(request):
    params = {}

    if request.method == 'POST':

        form = FormSearchEvents(request.POST)
        _name = request.POST['name']
        _date = request.POST['date']
        _status = request.POST['status']
        _result = request.POST['result']


        params['events'] = Event.objects.filter(
            name__icontains = _name,
            date__icontains = _date,
            status__icontains = _status,
            result__icontains = _result,

        )

        params['form'] = form

        return render(request,'events_view.html',params)
    
    else:
        
        form = FormSearchEvents()
        
        params['events'] = Event.objects.all()
        params['form'] = form

    return render(request,'events_view.html',params)

@user_passes_test(is_staff,login_url='/')
def events_add(request):

    params = {}

    if request.method == 'POST':

        form = FormEvents(request.POST)

        params['form'] = form

        if form.is_valid():
            _name = form.cleaned_data['name']
            _date = form.cleaned_data['date']
            _status = form.cleaned_data['status']
            _result = form.cleaned_data['result']

            _newEvent = Event(
                name = _name,
                date = _date,
                status = _status,
                result = _result,
                )

            _newEvent.save()

            return HttpResponseRedirect('/Coder/events')
        else:
            return render(request,'events_add.html', params)
    
    else:
        form = FormEvents()
        params['form'] = form
        
        return render(request,'events_add.html', params)

@user_passes_test(is_staff,login_url='/')
def events_edit(request, id):

    params = {}

    _event = Event.objects.get(id = id)

    if request.method == 'POST':

        form = FormEvents(request.POST)

        params['form'] = form

        if form.is_valid():

            _event.name = form.cleaned_data['name']
            _event.date = form.cleaned_data['date']
            _event.status = form.cleaned_data['status']
            _event.result = form.cleaned_data['result']
            _event.save()

            return redirect(reverse('events_view'))
        else:

            return render(request,'events_edit.html', params)
    
    else:
        form = FormEvents(instance=_event)
        params['form'] = form
        
        return render(request,'events_edit.html', params)

@user_passes_test(is_staff,login_url='/')
def events_delete(request,id):

    _event = Event.objects.get(id=id)
    _event = _event.delete()
    
    return redirect(reverse('events_view'))


from django.http import JsonResponse

def get_responded_players(request, question_id):
    # Suponiendo que tienes un modelo Question y un modelo Player
    if request.method == 'GET':

        answers = Answers.objects.filter(question_id=question_id)
        players = [answer.player.__str__() for answer in answers]

        return JsonResponse(players, safe=False)
