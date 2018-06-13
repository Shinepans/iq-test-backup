from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.forms.widgets import _CurrencyInput

class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

class Sections(Page):
    form_model = 'player'
    form_fields = ['submitted_answer']

    def vars_for_template(self):
        qd = self.player.current_question()
        return {
            'set': qd['set'],
            'answer': qd['answer'],
            'link': qd['link']
        }

    def submitted_answer_choices(self):
        qd = self.player.current_question()
        choices = [
            qd['choice1'],
            qd['choice2'],
            qd['choice3'],
            qd['choice4'],
        ]
        if qd['choice5']:
            choices.append(qd['choice5'])
        return choices

    def before_next_page(self):
        self.player.check_correct()


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        questions_correct = sum([p.is_correct for p in player_in_all_rounds])
        iq_test_fee = questions_correct * 10.0
        return {
            'player_in_all_rounds': player_in_all_rounds,
            'questions_correct': sum([p.is_correct for p in player_in_all_rounds]),
            'iq_test_fee': iq_test_fee
        }


page_sequence = [
    Instructions,
    Sections,
    FinalResults
]
