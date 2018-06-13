from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import csv

author = 'Shang'

doc = """
IQ Test
"""




class Constants(BaseConstants):
    name_in_url = 'iq_test'
    players_per_group = None

    with open('iq_test/sections.csv') as questions_file:
        questions = list(csv.DictReader(questions_file, delimiter='|'))

    num_rounds = len(questions)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['questions'] = Constants.questions

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = question_data['question']
            p.solution = question_data['solution']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_id = models.IntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(widget=widgets.RadioSelect)
    is_correct = models.BooleanField()

    def current_question(self):
        return self.session.vars['questions'][self.round_number - 1]

    def check_correct(self):
        self.is_correct = (self.submitted_answer == self.solution)