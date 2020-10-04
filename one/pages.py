from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    def vars_for_template(self):
        self.player.get_time("start")
    
    def before_next_page(self):
        self.player.ip_address = self.request.META['REMOTE_ADDR'].split(",")[0]
        self.player.browser = self.request.META['HTTP_USER_AGENT']

class Code(Page):
    form_model = "player"
    form_fields = ["participant_code"]

class Demographics(Page):
    form_model = "player"
    form_fields = ["gender", "age", "study", "semester", "experiments", "qBiasknowledge1"]

class Lottery(Page):
    form_model = 'player'
    form_fields = ['lottery_choice']

    def vars_for_template(self): #to create risk lottery bootstrap table
        list1 = Constants.lottery_gamble_successrate
        list2 = Constants.lottery_gamble_failurerate
        list3 = [f"id_lottery_choice_{i}" for i in range(1,16)]
        data = list(zip(list1,list2,list3))
        return {"data": data} # {% for a,b,c in data %} -> {{ a }} .. .. -> displays 85% .. 15% ..  form.lottery_choice.0

    # def before_next_page(self):
    #     self.participant.vars["lottery_choice"] = self.player.lottery_choice #if payout is needed in another app
    #     print("global_lottery_choice" + str(self.participant.vars["global_lottery_choice"]))

class Questions(Page):
    form_model = "player"
    form_fields = [f"Q{i}" for i in range(1,10)]

class End(Page):
    def vars_for_template(self):
        self.player.get_time("end")
        self.player.time_spent()

page_sequence = [Welcome, Code, Demographics, Lottery, Questions, End]
