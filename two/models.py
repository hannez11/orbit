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
import random, datetime


author = 'Hannes Gerstel'

doc = """
BWL4
"""


class Constants(BaseConstants):
    name_in_url = 'orbit2'
    players_per_group = None
    num_rounds = 1

    lottery_payout = ["0,75 Euro", "1,50 Euro", "0,00 Euro"] # used in the html table template
    lottery_gamble_successrate = [(85 - i) for i in range(0,75, 5)] #[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
    lottery_gamble_failurerate = [(15 + i) for i in range(0,75, 5)]
    # lottery_success = 1.50
    # lottery_failure = 0.00
    # lottery_safe = 0.75

    #subsequent decision bonus
    # success_boni = 9.50
    # failure_boni = 4.50
    # alternative_boni = 7.00

class Subsession(BaseSubsession):
    highlighting = models.StringField() # DA/DA0
    culture = models.StringField() # streng/locker

    # initial_decision_displayorder = models.PositiveIntegerField() #to randomly determine display order of the two options

    def creating_session(self): #automatically executed when session is generated
        # self.initial_decision_displayorder = random.randint(1, 2) # 1: coffee first

        if self.session.config["name"] == "streng_highlighting": #see dict in settings.py
            self.highlighting = "DA1"
            self.culture = "streng"
        elif self.session.config["name"] == "streng_nohighlighting":
            self.highlighting = "DA0"
            self.culture = "streng"
        elif self.session.config["name"] == "locker_highlighting":
            self.highlighting = "DA1"
            self.culture = "locker"
        elif self.session.config["name"] == "locker_nohighlighting":
            self.highlighting = "DA0"
            self.culture = "locker"
        else:
            print("treatment not found")

class Group(BaseGroup):
    pass

def quiz(q, choiceslist):
    return models.IntegerField(verbose_name = q,choices=choiceslist,widget=widgets.RadioSelect) #choiceslist = [[1, "abc"], [2, "def"], ...]

class Player(BasePlayer):
    initial_choices = models.StringField() # records all button clicks on the two initial options of a participant
    initial_decision = models.StringField() # final initial decision
    initial_expectation1=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7])
    initial_expectation2=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7])
    sub_decision = models.IntegerField(label="", min=0, max=100, widget=widgets.Slider(attrs={'step': '1'}, show_value=True)) # from 0 (termination) to 100 (continuation)
    slider_inputs = models.StringField() #store all slider inputs after mouse-release

    #quiz page
    quiz1 = quiz("Im Unternehmen Kitchen World bin ich ...", [[1,"der entscheidungsverantwortliche Manager der Abteilung „Projekte“"], [2,"der Controller der Abteilung „Operatives“"], [3, "der Leiter der Marketingabteilung"]])
    quiz2 = quiz("Meine Aufgabe ist es zunächst ...", [[1,"zwei Innovationsprojekte auszuwählen"], [2, "eine neue Produktidee zu entwickeln"], [3, "eins von zwei potentiellen Innovationsprojekten auszuwählen"]])
    quiz3a = quiz("Was ist der Geschäftsführung von Kitchen World besonders wichtig?", [[1, "Die neue Geschäftsführung möchte überhaupt nichts an der bisherigen strategischen Ausrichtung von Kitchen World ändern"], [2, "Die Geschäftsführung legt großen Wert darauf, dass Mitarbeiter alles dafür tun, um jegliche Fehler zu verhindern"], [3, "Die Geschäftsführung legt großen Wert darauf, dass Mitarbeiter mögliche Fehlentscheidungen akzeptieren und aus diesen lernen"]])
    quiz3b = quiz("Was ist der Geschäftsführung von Kitchen World besonders wichtig?", [[1, "Die neue Geschäftsführung möchte überhaupt nichts an der bisherigen strategischen Ausrichtung von Kitchen World ändern"], [2, "Die Geschäftsführung legt großen Wert darauf, dass Mitarbeiter alles dafür tun, um jegliche Fehler zu verhindern"], [3, "Die Geschäftsführung legt großen Wert darauf, dass Mitarbeiter mögliche Fehlentscheidungen akzeptieren und aus diesen lernen"]])
    quiz4 = models.StringField(label="Wie hoch ist im folgenden Beispiel das Guthaben auf dem Projektkonto nach Abschluss des Projekts (in Mio. Lira)?")
    quiz5 = models.StringField(label="Wie hoch ist die variable Vergütung in Lira, wenn das Guthaben des Projektkontos nach Projektabschluss 5 Mio. Lira beträgt?")
    quiz6 = models.StringField(label="Wie viel Euro entsprechen 35.000 Lira?")
    quiz7 = quiz("Woraus setzt sich Ihre Gesamtvergütung zusammen?", [[1, "Fixe Vergütung + Variable Vergütung aus der Hauptaufgabe + Auszahlung aus der Lotterieaufgabe"], [2,"Fixe Vergütung + Variable Vergütung aus der Hauptaufgabe"], [3, "Fixe Vergütung + Auszahlung aus der Lotterieaufgabe"]])
    quiz8a = quiz("Wie geht die Geschäftsführung mit Projekten um, die keinen Erfolg erzielen?", [[1, "Die Geschäftsführung deutet solche Projektergebnisse als Anzeichen von Inkompetenz, die sich entsprechend negativ auf die jährliche Leistungsbewertung auswirken können"], [2, "Solange Projekte, die keinen Erfolg erzielen, als Lernmöglichkeit genutzt werden, haben diese keinen Einfluss auf die jährliche Leistungsbewertung"], [3,"Es gibt keine Informationen darüber, wie die Geschäfsführung zu Misserfolgen steht"]])
    quiz8b = quiz("Wie geht die Geschäftsführung mit Projekten um, die keinen Erfolg erzielen?", [[3, "Die Geschäftsführung deutet solche Projektergebnisse als Anzeichen von Inkompetenz, die sich entsprechend negativ auf die jährliche Leistungsbewertung auswirken können"], [2, "Solange Projekte, die keinen Erfolg erzielen, als Lernmöglichkeit genutzt werden, haben diese keinen Einfluss auf die jährliche Leistungsbewertung"], [3,"Es gibt keine Informationen darüber, wie die Geschäfsführung zu Projekten steht, die keine Erfolge erzielen"]])

    quiz_totalwronganswers = models.IntegerField(initial=0) #increases, as long as atleast one answers is incorrect when page is submitted

    quiz1_answers = models.StringField(initial="FirstTry") #records all incorrect answers after FirstTry in an array (--> stringfield). stays FirstTry, if first answers chosen is the correct one
    quiz2_answers = models.StringField(initial="FirstTry")
    quiz3_answers = models.StringField(initial="FirstTry") #if Subsession.culture == "streng"
    quiz4_answers = models.StringField(initial="FirstTry")
    quiz5_answers = models.StringField(initial="FirstTry")
    quiz6_answers = models.StringField(initial="FirstTry")
    quiz7_answers = models.StringField(initial="FirstTry")
    quiz8_answers = models.StringField(initial="FirstTry")

    #timers
    timer_instructions = models.StringField()
    timer_quiz = models.StringField() # has to be a stringfield, since multiple attempts are possible which have to be stored in an array. intfields cant easily store arrays
    timer_initialdecision = models.StringField()
    timer_subinfo = models.StringField()
    timer_DA1 = models.IntegerField()
    timer_DA2 = models.IntegerField()
    timer_subdecision = models.StringField()

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



    
