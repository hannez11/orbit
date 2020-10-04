from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from django import forms
import datetime


author = 'Hannes Gerstel'

doc = """
BWL4
"""


class Constants(BaseConstants):
    name_in_url = 'orbit1'
    players_per_group = 4
    num_rounds = 1

    lottery_payout = ["0,75 Euro", "1,50 Euro", "0,00 Euro"] # used in the html table template
    lottery_gamble_successrate = [(85 - i) for i in range(0,75, 5)] #[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
    lottery_gamble_failurerate = [(15 + i) for i in range(0,75, 5)]


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

def create_q(labelinput):
    return models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label=labelinput)

qBiasknowledge1choices = [["AdC", "Anwendungen des Controllings (Management Control Systems)"], ["BeFin", "Behavorial Finance"], ["Verhaltensökonomik", "Verhaltensökonomik"], ["Financial Decision Making", "Financial Decision Making"], ["Keinen der genannten Kurse", "Keinen der genannten Kurse"]]

class Player(BasePlayer):
    participant_code = models.StringField()

    lottery_choice = models.PositiveIntegerField(choices=[[i, f"Szenario {i}"] for i in range(1,16)], widget=widgets.RadioSelect) #Lottery page; reuse in main experiment to determine payout

    gender = models.StringField(choices=["Männlich", "Weiblich"],widget=widgets.RadioSelectHorizontal, label="Bitte geben Sie ihr Geschlecht an.")
    age = models.IntegerField(choices=[i for i in range(17,51)], label="Bitte geben Sie Ihr Alter an.")
    study = models.StringField(choices=["Wirtschaftswissenschaften (BSc)", "BWL (MSc)", "VWL (MSc)", "Sonstige (BSc)", "Sonstige (MSc)"], label="Bitte geben Sie Ihren Studiengang an.")
    #degree = models.StringField(choices=["Bachelor", "Master"],widget=widgets.RadioSelectHorizontal, label="Welchen Abschluss streben Sie derzeit an?")
    semester = models.IntegerField(choices=[i for i in range(1,20)], label="In welchem Fachsemester befinden Sie sich aktuell? Falls Masterstudium, dann inklusive Bachelor.")
    experiments = models.IntegerField(choices=[i for i in range(1,20)], label="An wie vielen wissenschaftlichen Experimenten haben Sie bereits teilgenommen?")

    # multiplechoice field: choices has to be an iterable and every of its elements has to contain exactly 2 elements.
    qBiasknowledge1 = models.StringField(widget=forms.widgets.CheckboxSelectMultiple(choices=qBiasknowledge1choices), label="Welche der folgenden Kurse haben Sie belegt? Es ist unproblematisch, wenn Sie bisher keinen der Kurse belegt haben.")


    Q1=create_q("Wenn ich ein Vorhaben gestartet habe, dann will ich dieses auch zu Ende bringen.")
    Q2=create_q("Im Alltag nutze ich Fehler generell dazu, um aus ihnen zu lernen.")
    Q3=create_q("Wenn ich mir bei einer Sache sicher bin, dann lege ich wenig Wert auf die Meinung anderer.")
    Q4=create_q("Ich neige dazu emotionale Entscheidungen zu treffen.")
    Q5=create_q("Ich gehe generell davon aus, dass Fehler nicht immer vermeidbar sind.")
    Q6=create_q("Ich habe großen Respekt vor Autoritätsperson.")
    Q7=create_q("Ich habe mich gewöhnlich an Regeln und Vorgaben gehalten, die von meinen Eltern aufgestellt wurden.")
    Q8=create_q("Ich habe kein Problem damit, Fehler offen zuzugeben.")
    Q9=create_q("Ich mache mir oft Gedanken darüber, was andere über mich denken.")

    starttime = models.StringField() #get time of participant when welcome page is loaded
    endtime = models.StringField() #get time of participant when last page is loaded
    def get_time(self, start_or_end):
        if start_or_end == "start":
            self.starttime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        else:
            self.endtime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    timespent = models.StringField() #get time of participant when last page is loaded
    def time_spent(self):
        duration = datetime.datetime.strptime(self.endtime, "%d/%m/%Y %H:%M:%S") - datetime.datetime.strptime(self.starttime, "%d/%m/%Y %H:%M:%S")
        self.timespent = f"{duration.total_seconds():.0f}sec; {float(duration.total_seconds() / 60):.2f}min"

    ip_address = models.StringField()
    browser = models.StringField()