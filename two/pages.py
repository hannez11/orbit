from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    def vars_for_template(self):
        self.player.get_time("start")
    
    def before_next_page(self):
        self.player.ip_address = self.request.META['REMOTE_ADDR'].split(",")[0]
        self.player.browser = self.request.META['HTTP_USER_AGENT']

class Instructions(Page):
    form_model = "player"
    form_fields = ["timer_instructions"]

class Quiz(Page):
    form_model = "player"

    def get_form_fields(self):
        if self.subsession.culture == "streng": #question 3 answers differ between streng (3a) and locker (3b). all other questions are the same
            return [f"quiz{i}" if i != 3 else f"quiz{i}a" for i in range(1,8)] + ["quiz8a"] + ["timer_quiz"]
        else:
            return [f"quiz{i}" if i != 3 else f"quiz{i}b" for i in range(1,8)] + ["quiz8b"] + ["timer_quiz"]

    def quiz1_error_message(self, value):
        #print('value is', value) #value equals selected radiobutton value of question 1 after submission
        if value != 1:
            self.player.quiz1_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz2_error_message(self, value):
        # print('value is', value)
        if value != 3:
            self.player.quiz2_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz3a_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.quiz3_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz3b_error_message(self, value):
        # print('value is', value)
        if value != 3:
            self.player.quiz3_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz4_error_message(self, value):
        # print('value is', value, type(value))
        if not (value[0:3] == "6,0" or value == "6" or value[0:3] == "6.0"):
            self.player.quiz5_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz5_error_message(self, value):
        # print('value is', value)
        if not (value == "50000" or value == "50000,00" or value == "50000,0" or value == "50.000"):
            self.player.quiz6_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz6_error_message(self, value):
        # print('value is', value)
        if not (value[0:4] == "3,50" or value == "3,5" or value == "3.50" or value == "3.5"):
            self.player.quiz7_answers += ", " + value
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz7_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.quiz4_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz8a_error_message(self, value):
        # print('value is', value)
        if value != 1:
            self.player.quiz8_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'
    def quiz8b_error_message(self, value):
        # print('value is', value)
        if value != 2:
            self.player.quiz8_answers += ", " + str(value)
            self.player.quiz_totalwronganswers += 1
            return 'Bitte korrigieren Sie Ihre Antwort.'

class KitchenWorld1(Page): #InitialInfo
    pass

class KitchenWorld2(Page): #InitialDecision
    form_model = "player"
    form_fields = ["initial_choices", 'timer_initialdecision']

    def before_next_page(self):
        #print(self.player.initial_choices.split(",")[-1]) # final initial decision. initial_choices records all button clicks on the two investment options
        self.player.initial_decision = self.player.initial_choices.split(",")[-1]
        self.participant.vars['initial_decision'] = "Smart " + self.player.initial_decision #global variable for the 2nd app
        # print("self.participant.vars['initial_decision']:",self.participant.vars['initial_decision'])

class KitchenWorld3(Page): #InitialExpectation
    form_model = "player"
    form_fields = ["initial_expectation1", "initial_expectation2"]

    #dynamically set label of expectation question which includes the chosen project
    def vars_for_template(self):
        Qie1a = f"Ich glaube, dass mein gewähltes Projekt Smart {self.player.initial_decision} positiv verlaufen wird."
        Qie1b = f"Ich hatte Bedenken die falsche Entscheidung zu treffen."
        return dict(q_label=[Qie1a,Qie1b])

class KitchenWorld4(Page): #SubIntro
    pass

class KitchenWorld5(Page): #SubInfo
    form_model = "player"
    form_fields = ['timer_subinfo']

class Beratung1(Page): #DA1
    def is_displayed(self):
        return self.subsession.highlighting == "DA1" #page is only displayed on DA1 condition

    form_model = "player"
    form_fields = ["timer_DA1"]

class Beratung2(Page): #DA2
    def is_displayed(self):
        return self.subsession.highlighting == "DA1" #page is only displayed on DA1 condition

    form_model = "player"
    form_fields = ["timer_DA2"]


class KitchenWorld6(Page): #SubDecision
    form_model = "player"
    form_fields = ['sub_decision', "slider_inputs", "timer_subdecision"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.participant.vars['sub_decision'] = self.player.sub_decision #set global so can be used in the next app

        self.player.get_time("end")
        self.player.time_spent()


page_sequence = [Welcome, Instructions, Quiz, KitchenWorld1, KitchenWorld2, KitchenWorld3, KitchenWorld4, KitchenWorld5, Beratung1, Beratung2, KitchenWorld6]
# page_sequence = [Welcome, KitchenWorld2, KitchenWorld6] #short version for peq
