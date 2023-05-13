from django import forms
from django.forms import ModelForm
from Coder.models import Players, Questions, Answers, Event, QuestionsRules
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormPlayers(ModelForm):
    class Meta:
        model = Players
        fields = [
            'user',
            'image',
            'first_name', 
            'last_name', 
            'date_birth' ,
            'phone',
            'adress', 
            'city',
            'state', 
            'country', 
        ]
        widgets = {
            'date_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(FormPlayers, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class FormSearchPlayers(ModelForm):
    class Meta:
        model = Players
        fields = [
            # 'user',
            'image',
            'first_name', 
            'last_name', 
            'date_birth' ,
            'phone',
            'adress', 
            'city',
            'state', 
            'country', 
        ]
        widgets = {
            'date_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormSearchPlayers, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class FormQuestions(ModelForm):
    class Meta:
        model = Questions
        fields = [
            'title',
            'category',
            'question', 
            'date',
            'correct_answer', 
            'author',
            'event',
            'question_rule'
            # 'status',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class FormQuestionsPlayers(ModelForm):
    class Meta:
        model = Questions
        fields = [
            'title',
            'category',
            'question', 
            'date',
            'correct_answer', 
            # 'author',
            'question_rule',
            'event',
            # 'status',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        open_events = Event.objects.filter(status='open')
        self.fields['event'].queryset = open_events

class FormSearchQuestions(ModelForm):
    class Meta:
        model = Questions
        fields = [
            'title',
            'category',
            'date',
            'author',
            'question', 
            'correct_answer', 
            'event',
            'question_rule',
            'status',
            'result',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),

        }
    def __init__(self, *args, **kwargs):
        super(FormSearchQuestions, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class FormAnswers(ModelForm):
    class Meta:
        model = Answers
        fields = [
            'player',
            'question', 
            'answer',
        ]

class FormAnswersPlayer(ModelForm):
    
    question_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'readonly': True}),
        required=False,
        label="Question"
    )


    class Meta:
        model = Answers
        fields = [
            'question_text',
            'question', 
            'answer',
        ]
        widgets = {
            'question': forms.HiddenInput(attrs={'class': 'form-control','readonly': True}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)

        super(FormAnswersPlayer, self).__init__(*args, **kwargs)
        if question is not None:
            self.fields['question'].initial = question
            self.fields['question'].label = ""
            self.fields['question_text'].initial = str(question)

class FormSearchAnswers(ModelForm):

    event = forms.ModelChoiceField(queryset=Event.objects.all())
    question_text = forms.CharField(label='Question')
    class Meta:
        model = Answers
        fields = [
            'event',
            # 'question', 
            'question_text',
            'player', 
            'answer',
        ]
    def __init__(self, *args, **kwargs):
        super(FormSearchAnswers, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class SignUpForm(UserCreationForm):
    
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class FormEditAccount(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password1','password2']

class FormProfile(ModelForm):
    class Meta:
        model = Players
        fields = [
            'image',
            'first_name', 
            'last_name', 
            'date_birth' ,
            'phone',
            'adress', 
            'city',
            'state', 
            'country', 
        ]
        widgets = {
            'date_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class FormSearchQuestionsRules(ModelForm):
    description = forms.CharField(
        widget=forms.TextInput(),
        required=False,
        label="Description"
    )
    class Meta:
        model = QuestionsRules
        fields = [
            'name',
            'description',
            'points', 
            # 'bonus_exact_answer',
            # 'allows_draw', 
            # 'allows_wildcard',
            # 'points_draw',
        ]
    def __init__(self, *args, **kwargs):
        super(FormSearchQuestionsRules, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False



class FormQuestionsRules(ModelForm):
    class Meta:
        model = QuestionsRules
        fields = [
            'name',
            'description',
            'points', 
            'bonus_exact_answer',
            'allows_draw', 
            'allows_wildcard',
            'points_draw',
        ]

class FormSearchEvents(ModelForm):
    class Meta:

        model = Event
        fields = [
            'name',
            'date', 
            'status', 
            'result'
        ]
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}),}

    def __init__(self, *args, **kwargs):
        super(FormSearchEvents, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False



class FormEvents(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'date', 
            'status', 
            'result'
        ]
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}),}