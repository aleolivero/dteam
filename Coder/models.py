from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from datetime import date
# Create your models here.

class Players(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='players')
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    date_birth = models.DateField(blank=True,null=True, verbose_name="Birth",default=date(2000, 1, 1))
    phone = models.CharField(max_length=100, verbose_name="Phone")
    adress = models.CharField(max_length=100, verbose_name="Adress")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State")
    country = models.CharField(max_length=100, verbose_name="Country")

    def __str__(self,):
        if not self.first_name and not self.last_name:
            
            _str = str(self.user.username)

        else:
            
            _str = str(self.first_name) + ' ' + str(self.last_name)

        return _str


class Event(models.Model):

    STATUS_CHOICES = (
    ('open', 'Open'),
    ('closed', 'Closed'),
    )
    RESULT_CHOICES = (
        ('undetermined', 'Undetermined'),
        ('determined', 'Determined'),
        )

    name = models.CharField(max_length=100, verbose_name="Event Name")
    date = models.DateField(verbose_name="Event Date")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='undetermined')

    def __str__(self):
        return self.name
    
    def winner(self):

        _scores = PlayerScore.objects.filter(winner_answer__question__event__id = self.id)

        return True



class QuestionsRules(models.Model):

    name = models.CharField(max_length=100, verbose_name="Rule Name")
    description = models.TextField(verbose_name="Description")
    points = models.FloatField(verbose_name="Points")
    bonus_exact_answer = models.FloatField(verbose_name="Bonus Exact Answer")
    allows_draw = models.BooleanField(verbose_name="Allows Draw", default=True)
    allows_wildcard = models.BooleanField(verbose_name="Allows Wildcard", default=False)
    points_draw = models.FloatField(verbose_name="Points Draw")

    def __str__(self):
        return self.name


class Questions(models.Model):
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    RESULT_CHOICES = (
        ('undetermined', 'Undetermined'),
        ('determined', 'Determined'),
        )

    title = models.CharField(max_length=1000, verbose_name="Title")
    category = models.CharField(max_length=1000, verbose_name="Category")
    question = models.CharField(max_length=1000, verbose_name="Question")
    date = models.DateField(verbose_name="Date")
    correct_answer = models.CharField(max_length=1000, verbose_name="Correct Answer")
    author = models.ForeignKey(Players,blank=False,null=True,on_delete=models.CASCADE, verbose_name="Player")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='undetermined')
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Event")
    question_rule = models.ForeignKey(QuestionsRules, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Question Rule")

    def statusFormat(self):
        if str(self.status) == 'open':

            return format_html('<span class="badge text-bg-success">{}</span>', str(self.status))

        elif str(self.status) == 'closed':
            return format_html('<span class="badge text-bg-secondary">{}</span>', str(self.status))
        

    def resultFormat(self):
        if str(self.result) == 'determined':

            return format_html('<span class="badge text-bg-success">{}</span>', str(self.result))

        elif str(self.result) == 'undetermined':
            return format_html('<span class="badge text-bg-secondary">{}</span>', str(self.result))


    def __str__(self,):
        return str(self.question)


class Answers(models.Model):

    answer = models.CharField(max_length=1000, verbose_name="Answer")
    player = models.ForeignKey(Players,blank=False,null=True,on_delete=models.CASCADE, verbose_name="Player")
    question = models.ForeignKey(Questions,blank=False,null=True,on_delete=models.CASCADE, verbose_name="Question")

    def __str__(self,):
        return str(self.answer)
    
class PlayerScore(models.Model):
    winner_answer = models.ForeignKey(Answers,blank=False,null=True,on_delete=models.CASCADE, verbose_name="winner_answer")
    points = models.FloatField(verbose_name="Points",default=0)




