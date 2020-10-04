from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class PeqIntro(Page):
    def vars_for_template(self):
        self.player.get_time("start")
        self.player.ip_address = self.request.META['REMOTE_ADDR'].split(",")[0]
        self.player.browser = self.request.META['HTTP_USER_AGENT']
    
class PEQsub(Page):
    form_model = "player"
    form_fields = ["qSub1","qSub2"] #1

    def vars_for_template(self):
        qSub1 = f"Ich sehe es als Fehler an, ursprünglich in das Projekt {self.participant.vars['initial_decision']} investiert zu haben."
        qSub2 = f"Wie hoch schätzen Sie das Risiko ein, dass Ihr Projekt {self.participant.vars['initial_decision']} bei Fortführung insgesamt einen Verlust erwirtschaften wird?"
        PEQsub = {"q_label":[qSub1,qSub2]}

        return PEQsub #get question label from dict

class PEQpsim(Page):
    form_model = "player"
    form_fields = ["qPsIm1", "qPsIm2", "qPsIm3"] #2

class PEQpsc(Page):
    form_model = "player"
    form_fields = ["qPsC1", "qPsC2", "qPsC3"] #3

class PEQda1(Page):
    def is_displayed(self):
        return self.subsession.highlighting == "DA1" #page is only displayed on DA1 condition

    form_model = "player"
    form_fields = ["qDa1", "qDa2", "qDa3"]

class PEQda2(Page):
    def is_displayed(self):
        return self.subsession.highlighting == "DA1" #page is only displayed on DA1 condition

    form_model = "player"
    form_fields = ["qDaCheckAnsw1", "qDa4"]

class PEQmisc1(Page):
    form_model = "player"
    form_fields = ["qMisc1", "qMisc2", "qMisc3", "qMisc4", "qMisc5"] #4

    def vars_for_template(self):
        qMisc1 = "Es war mir wichtig als guter Entscheider wahrgenommen zu werden."
        qMisc2 = "Ich wollte die ursprüngliche Investition in Höhe von 4 Mio. Lira nicht umsonst ausgegeben haben."
        qMisc3 = f"Ich fühle mich für das Ergebnis meines Projekts {self.participant.vars['initial_decision']} verantwortlich."
        qMisc4 = f"Es war mir wichtig das Projekt {self.participant.vars['initial_decision']} zum Abschluss zu bringen."
        qMisc5 = f"Ich wollte vermeiden, dass das Projekt {self.participant.vars['initial_decision']} insgesamt einen Verlust macht."
        PEQmisc = {"q_label":[qMisc1, qMisc2, qMisc3, qMisc4, qMisc5]}
        
        return PEQmisc #get question label from dict

class PEQmisc2(Page):
    form_model = "player"
    form_fields = ["qMisc6", "qMisc7", "qMisc8"] #5

class PEQmisc3(Page):
    form_model = "player"
    form_fields = ["qMisc9", "qMisc10", "qMisc11"] #6

class PEQfin(Page):
    form_model = "player"
    form_fields = ["qBiasknowledge2", "qBiasknowledge3", "qAttention", "qEnvironment"] #8

# class PEQ(Page):
#     form_model = "player"
#     items = [] #put all question items in here which should be looped through. put multiple items on one page into seperate list
    

#     def get_form_fields(self):
#         #self.items[self.round_number - 1] grabs index of list based on current round number. round numer starts at 1
#         if not isinstance(self.items[self.round_number - 1], list): 
#             return [self.items[self.round_number - 1]] #returns only one question item depending on the current round number. item needs to be stored in a list
#         else: #if current round has multiple fields to be displayed on one page, then items are already in list form
#             return self.items[self.round_number - 1]

#     # dynamically set label of expectation question which includes the chosen project
#     def vars_for_template(self):
#         #questions with dynamic label

#         qSub1 = f"Ich sehe es als Fehler an, ursprünglich ins Projekt {self.participant.vars['initial_decision']} investiert zu haben"
#         qSub2 = f"Wie hoch schätzen Sie das Risiko ein, dass das Projekt {self.participant.vars['initial_decision']} insgesamt einen Verlust erwirtschaften wird?"

#         qPd1 = "Ich wollte die ursprüngliche Investition in Höhe von 4 Mio. Lira nicht umsonst ausgegeben haben"
#         qPd2 = "Ich bin zuversichtlich, dass meine persönlichen Analysen zu den richtigen Schlussfolgerungen geführt haben"
#         qPd3 = f"Ich fühle mich für das Ergebnis vom Projekt {self.participant.vars['initial_decision']} verantwortlich"
#         qPd4 = f"Es war mir wichtig das Projekt {self.participant.vars['initial_decision']} zum Abschluss zu bringen"
#         qPd5 = f"Ich wollte unbedingt vermeiden, dass das Projekt {self.participant.vars['initial_decision']} insgesamt einen Verlust macht"

#         items_with_dynamic_label = dict(Q1={"q_label":[qSub1,qSub2]}, Q4={"q_label":[qPd1, qPd2, qPd3, qPd4, qPd5]})
        

#         if f"Q{self.round_number}" in items_with_dynamic_label: #if question uses dynamic label
#             return items_with_dynamic_label.get(f"Q{self.round_number}") #get question label from dict
#         else:
#             pass #use regular model label

class ParticipantCode(Page):
    form_model = "player"
    form_fields = ["participant_code"]

    #determine subsequent decision bonus payments
    def before_next_page(self):
        self.player.board_decision_lottery = random.randint(0,100) # if board_decision_lottery > player.sub_decision, then project is terminated

        population = [0, 1] # 0: project failed ; 1: project succeeded
        weights = [0.67, 0.33] # project fails with 67% probability and succeeds with 33%
        self.player.project_success_outcome = random.choices(population, weights)[0] # returns a list with one entry (0 or 1)

        self.player.lottery_draft = random.randint(1,15) # generate random number between 1 and 15 before session is generated
        self.player.lottery_outcome = random.randint(0,100) # generate random number between 0 and 100 before session is generated
        if self.player.participant_code in Constants.lottery_choices_dict:
            self.player.lottery_choice = Constants.lottery_choices_dict.get(self.player.participant_code) #get lottery choice from the manually updated lottery_choices_dict
        elif self.player.participant_code.casefold() in Constants.lottery_choices_dict_insensitve:
            self.player.lottery_choice = Constants.lottery_choices_dict_insensitve.get(self.player.participant_code.casefold()) #get lottery choice from the manually updated lottery_choices_dict
        else:
            self.player.lottery_choice = 99 #participant entered wrong code that has not been entered in the first experiment before


        def insert(source_str, insert_str, pos): #insert numbers into code to make payment identifiable
            return source_str[:pos]+insert_str+source_str[pos:]
        
        code_calc = random.choice(Constants.codes_helper) #randomly select one of the 5 strings

        # code = "01ffcb34f0"
        # if code[1] == 1:
        #     payment += alternative_boni
        # elif code[1] == 2:
        #     payment += success_boni
        # elif code[1] == 0:
        #     payment += failure_boni
        # if code[-1] == 1:
        #     payment += lottery_safe
        # elif code[-1] == 2:
        #     payment += lottery_success
        # elif code[-1] == 0:
        #     payment += lottery_failure

        # print(f"Current player bonus payoff after subsequent decision: {self.participant.payoff}")
        if self.participant.vars['sub_decision'] == 0: # 0% recommendation to continue
            self.player.board_decision = "termination"
        elif self.participant.vars['sub_decision'] < self.player.board_decision_lottery: # user 20% > board 21% --> termination
            self.player.board_decision = "termination"
        else:
            self.player.board_decision = "continuation" # user 100% >= board 100% --> continuation

        #Each player has a payoff field, which is a CurrencyField. If your player makes money, you should store it in this field. self.participant.payoff is the sum of the payoffs a participant made in each subsession. 
        #Bonus payment based on subsequent decision
        if self.player.board_decision == "continuation":
            if self.player.project_success_outcome == 1: # project succeeded
                self.player.payoff += c(Constants.success_boni)
                code_calc = insert(code_calc, "2", 1) #append 1 at index 2 of the code_calc string
            elif self.player.project_success_outcome == 0: # project failed
                self.player.payoff += c(Constants.failure_boni)
                code_calc = insert(code_calc, "0", 1)
        else:
            self.player.payoff += c(Constants.alternative_boni) #safe payment from alternative
            code_calc = insert(code_calc, "1", 1)

        # print(f"Current player bonus payoff after subsequent decision: {self.participant.payoff}")

        # Lottery payout
        if self.player.lottery_choice == 99: #lottery choice is unknown due to mismatched participant code
            code_calc = insert(code_calc, "9", -1) #9 if code mismatch
        elif self.player.lottery_choice > self.player.lottery_draft: # player chooses 14 and < 14 drafted --> lottery participation
            if self.player.lottery_outcome <= Constants.lottery_gamble_successrate[self.player.lottery_draft - 1]: #lottery participation succeeded
                self.player.payoff += c(Constants.lottery_success)
                code_calc = insert(code_calc, "2", -1)
            else:
                self.player.payoff += c(Constants.lottery_failure) #failed
                code_calc = insert(code_calc, "0", -1)
        else:
            self.player.payoff += c(Constants.lottery_safe) #safe payment
            code_calc = insert(code_calc, "1", -1)
        
        # print(f"Current player bonus payoff after lottery: {self.participant.payoff}")
        self.player.total_payout = self.participant.payoff_plus_participation_fee()
        self.player.uuid = code_calc #check first index for project payment and -2 index for lottery payment

class PayoutProject(Page):
    pass
    # def is_displayed(self):
    #     return Constants.num_rounds == self.round_number #page is only displayed in the last round

class PayoutLottery(Page):
    def vars_for_template(self):
        return dict(scsrate = Constants.lottery_gamble_successrate[self.player.lottery_draft - 1]) #successrate for drafted lotterys


class PayoutTotal(Page):
    def vars_for_template(self):
        return dict(scsrate = Constants.lottery_gamble_successrate[self.player.lottery_draft - 1]) #successrate for drafted lotterys

class End(Page):
    def vars_for_template(self):
        self.player.get_time("end")
        self.player.time_spent()


page_sequence = [PeqIntro, PEQsub, PEQpsim, PEQpsc, PEQda1, PEQda2, PEQmisc1, PEQmisc2, PEQmisc3, PEQfin, ParticipantCode, PayoutProject, PayoutLottery, PayoutTotal, End]
# page_sequence = [PeqIntro, ParticipantCode, PayoutProject, PayoutLottery, PayoutTotal, End]

