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
    name_in_url = 'orbitpeq'
    players_per_group = None
    num_rounds = 1 # PEQ template gets looped X times

    lottery_gamble_successrate = [(85 - i) for i in range(0,75, 5)] #[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
    lottery_gamble_failurerate = [(15 + i) for i in range(0,75, 5)]

    #lottery payment
    lottery_success = 1.50
    lottery_failure = 0.00
    lottery_safe = 0.75

    #subsequent decision bonus
    success_boni = 9.50
    failure_boni = 4.50
    alternative_boni = 7.00

    codes_helper = ['0fcb34f', '78d8cf0', '52ce2a4', '1z3db8b']

    lottery_choices_dict = {'4MaBeFr10': 9, '7GüMuFl10': 11, '6SuStSc08': 5, '1DeMuBa06': 10, '6ChJüGi05': 10, '1GaFrSc11': 10, '5MoNaBa05': 8, '0HEREWE05': 11, '6ChAlGi06': 3, '0SuMiGi05': 9, '4AnKaWi04': 3, '7MaMaSc08': 8, '6StMiGi03': 8, '2ElKrDz04': 7, '8AnJöFr06': 3, '9ErPeGi04': 8, '5SaReWe09': 5, '6anraro06': 5, '0AnMiLi02': 4, '6MaViGi12': 5, '6DOACSC04': 6, '2RePeWe03': 9, '8PeRaLi06': 6, '7JuKaSi07': 11, '7HiMiLi08': 5, '3HoAcBa01': 10, '3SaPeBa01': 9, '1HeJüGi02': 4, '2MaZeSe11': 7, '9KaRoGi11': 8, '3RiViLu06': 8, '9SaDiSi10': 6, '8OlPaGr11': 8, '3KiCeHa12': 9, '8SoHeWe05': 8, '5JiJiCh04': 12, '4giwean09': 8, '9RuEdKa01': 8, '6ReAnWe01': 5, '0AdElGu06': 11, '4KaBeFr11': 4, '9JuGeSt08': 8, '4SaNoLi07': 7, '2BiRoHa01': 7, '6IvDiGi06': 8, '8UtJoKa11': 9, '3BeBeLu08': 10, '5GaMiOf04': 8, '1PeKlFu07': 8, '0sijogi01': 8, '4AnMaHü01': 4, '4AnAnWo11': 7, '2ElRuOf02': 8, '7CaReBa06': 9, '9ClMaBa09': 4, '9BeClGi11': 4, '9ChThHa05': 6, '9CHSTMA08': 6, '8RESAGI01': 7, '8HINHLE08': 10, '2SuWaLa02': 4, '1GaHuBr02': 6, '0SaMaBa04': 4, '0ElMaKi05': 3, '2morafr09': 4, '4MaHeCa09': 6, '2PeMaGi12': 5, '6MoBrGi02': 4, '8ThChFr06': 13, '5AnMaGi12': 3, '9DaGrEs12': 5, '3KaMiBü04': 8, '8HaSeDi07': 7, '1BiDiFl04': 5, '1KaDiBa02': 9, '8IrRoHa06': 8, '7FrReBü06': 12, '0JuJeHo07': 9, '7ChDaLi09': 5, '7SiDaKo12': 6, '8CoEbEh09': 9, '3ElThMi08': 8, '0IrMiGi07': 8, '1MaMaLi03': 9, '7PeAlKo10': 9, '3SeAdFr11': 1, '2MaRuFr03': 1, '0veuwfr07': 7,'3ThKhBa12': 10, '6XADADI10': 6, '2AlKlGr01': 1, '2KuBhBa10': 9, '6MaReGi08': 8, '8BiJöWe09': 3, '9HeViWe09': 10, '7ZoSuOf07': 9, '1DaRoSi07': 5, '9DoFrGe04': 11, '1UlHeGü09': 7, '0MaHoAs03': 8, '9SaUwGi12': 4, '4YaMaHa06': 5, '1AnRoQu03': 8, '0ChUwAl12': 4, '9ChNoWe10': 4, '6DaRoSc11': 8, '3MiOlLü12': 6, '3DiMaGi08': 8, '8MiLeBa02': 15, '5SuWeGi06': 5, '9HeFrWe02': 6, '4TaAnFr10': 9, '3ChMiSc01': 7, '3BiCeBa10': 6, '2PiChWi06': 5, '8SuUlMa04': 15, '0KaAnEr07': 9, '5IzJüBa05': 8, '9GiHeGi02': 7, '2ReGeAs01': 8, '4LuAsAd10': 7, '5NuKaVi08': 7, '8ChPeWe11': 12, '0SaThLi05': 6, '1BeArGi12': 6, '6SaSaWe08': 8, '0HeViSp10': 8, '8AnHaGi12': 9, '6KaKaNa11': 9, '0ANHEHO10': 3, '6UtPeUe08': 8, '6SuAlEl08': 7, '9HeUwGi05': 9, '1LaJiDu06': 1, '3SiKlPf09': 13, '9MeArWi09': 9, '3StUdDi09': 4, '2JoChNi09': 10, '2MaEnSe01': 4, '8DaBeFr06': 8, '7MeArWi09': 9, '9VISAWI10': 1, '6BiAzFr07': 7, '0HaSeDi04': 9, '6ZaNaSc08': 12} #lottery choices of participants (need to be manually updated based on the first part of the experiment)

    lottery_choices_dict_insensitve = {key.lower(): value for key, value in lottery_choices_dict.items()} #since some people write in caps

class Subsession(BaseSubsession):
    highlighting = models.StringField() # DA/DA0
    culture = models.StringField() # streng/locker

    codes = models.StringField(initial=Constants.codes_helper)
    # codes = ['0fcb34f', '78d8cf0', '52ce2a4', '1z3db8b'] #[str(uuid.uuid4())[0:8] for i in range(3)]
    # if termination, then "1" is added at index 1
    # if continuation and project is succesful, then "2" is added at index 1
    # if continuation and project failes, then "0" is added at index 1
    # if safe payment from lottery, then "1" is added at index -1 (second last position)
    # if lottery participation and success, then "2" is added at index -1
    # if lottery participation and failure, then "0" is added at index -1
    # calc payment based on code in email and compare with given total_payout
    # payment = 0
    # code = "01fcb342f"
    # if code[1] == 1:
    #     payment += alternative_boni
    # elif code[1] == 2:
    #     payment += success_boni
    # elif code[1] == 0:
    #     payment += failure_boni
    # if code[-2] == 1:
    #     payment += lottery_safe
    # elif code[-2] == 2:
    #     payment += lottery_success
    # elif code[-2] == 0:
    #     payment += lottery_failure
    # print(payment, self.player.total_payout)

    def creating_session(self): #automatically executed when session is generated (is executed for each new round)
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

def create_q(labelinput):
    return models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label=labelinput)

class Player(BasePlayer):

    qSub1=create_q("Ich sehe es als Fehler an, ursprünglich ins Projekt XX investiert zu haben.")
    qSub2=create_q("Wie hoch schätzen Sie das Risiko ein, dass das Projekt XX insgesamt einen Verlust erwirtschaftet?")

    qPsIm1=create_q("Ich hatte Bedenken eine falsche Empfehlung an die Geschäftsführung abzugeben.")
    qPsIm2=create_q("Falls die Geschäftsführung meine Arbeitsleistung bewerten würde, befürchte ich dabei eine schlechte Evaluation zu bekommen.")
    qPsIm3=create_q("Ich hätte Bedenken bei zukünftigen Kitchen World Projekten Verantwortung zu übernehmen.")

    qPsC1=create_q("In meiner Rolle als Manager im Unternehmen Kitchen World hatte ich Bedenken Risiken einzugehen.")
    qPsC2=create_q("Ich habe das Gefühl, dass im Unternehmen Kitchen World bei Fehlern zunächst nach einem Schuldigen gesucht wird.")
    qPsC3=create_q("Im Unternehmen Kitchen World werden Fehler als Chance gesehen, um daraus für die Zukunft zu lernen.")

    #seperate page
    qDa1=create_q("Die Infos des Berater-Teams haben meine Empfehlung an die Geschäftsführung wie folgt beeinflusst:")
    qDa2=create_q("Ich fand es gut, dass das Berater-Team mir die Gefahren meines Projekts aufgezeigt hat.")
    qDa3=create_q("Wenn ich die Wahl gehabt hätte, ob ich die Beratungsleistung in Anspruch nehmen möchte, hätte ich mich dafür entschieden.")

    #seperate page
    qDaCheckAnsw1 = models.IntegerField(verbose_name = "Die Aufgabe des Berater-Teams war es:",choices=[[1, "Negative Aspekte meines Projekts hervorzuheben"], [2,"Positive Aspekte meines Projekts hervorzuheben"]],widget=widgets.RadioSelect)
    qDa4=create_q("Ich sehe die Arbeit des Berater-Teams als Angriff gegen meine ursprüngliche Entscheidung an.")

    qMisc1=create_q("Ich wollte die ursprüngliche Investition in Höhe von 4 Mio. Lira nicht umsonst ausgegeben haben.")
    qMisc2=create_q("Es war mir wichtig als guter Entscheider wahrgenommen zu werden.")
    qMisc3=create_q("Ich fühle mich für das Ergebnis meines Projekts XX verantwortlich.")
    qMisc4=create_q("Es war mir wichtig das Projekt XX zum Abschluss zu bringen.")
    qMisc5=create_q("Ich wollte unbedingt vermeiden, dass das Projekt XX insgesamt einen Verlust macht.")

    qMisc6=create_q("Ich habe meine Entscheidung ausschließlich auf Grundlage zahlenmäßiger (quantitativer) Informationen getroffen.")
    qMisc7=create_q("Wenn das von mir ausgewählte Projekt am Ende einen Verlust macht, bedeutet das, dass ich ein(e) schlechte(r) Entscheider(in) bin.")
    qMisc8=create_q("Es war mir wichtig zu vermeiden, dass ich meine Empfehlung an die Geschäftsführung später bedauern werde.")

    qMisc9=create_q("Bei der Empfehlung an die Geschäftsführung habe ich mich besonders auf diejenigen Aspekte des Projekts konzentriert, die gut gelaufen sind.")
    qMisc10=create_q("Ich bin zuversichtlich, dass meine persönlichen Analysen zu den richtigen Schlussfolgerungen geführt haben.")
    qMisc11=create_q("Es war mir wichtig eine möglichst hohe Vergütung zu erzielen.")

    qBiasknowledge2=models.StringField(widget=widgets.RadioSelect, label="Ich habe bereits von der Thematik „Biases“ und deren Rolle in Entscheidungsprozessen gehört.", choices=['Ja', "Nein"])
    qBiasknowledge3=models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4,5,6,7], label="Ich kenne mich gut mit der Thematik „Biases“ aus.")
    qAttention=create_q("Wie aufmerksam haben Sie das Experiment bearbeitet? (Ihre Antwort hat keine Auswirkung auf Ihre Vergütung)")
    qEnvironment = models.StringField(choices=["Zu Hause (alleine)", "Zu Hause (in Anwesenheit anderer Personen)", "In der Öffentlichkeit (bspw. Bahn oder in der Uni)", "Sonstige"], label="An welchem Ort haben Sie das Experiment bearbeitet?")

    total_payout = models.CurrencyField()
    participant_code = models.StringField() #ParticipantCode page
    uuid = models.StringField() #unique ID; index 1 determines project payout; -1 determines lottery payout

    lottery_choice = models.PositiveIntegerField() #to determine drafted scenario
    lottery_draft = models.PositiveIntegerField() #to determine drafted scenario
    lottery_outcome = models.PositiveIntegerField() #to determine outcome in case of lottery participation

    board_decision = models.StringField() # if board_decision_lottery > player.sub_decision, then project is terminated
    project_success_outcome = models.PositiveIntegerField() #to determine outcome (best/worst case) of the chosen project
    board_decision_lottery = models.PositiveIntegerField() #to determine whether recommendation is followed

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