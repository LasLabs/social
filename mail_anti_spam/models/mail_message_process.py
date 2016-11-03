# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from HTMLParser import HTMLParser

from odoo import api, fields, models

import matplotlib.pyplot as plt
import csv
from textblob import TextBlob
import pandas
import sklearn
import cPickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold, cross_val_score, train_test_split 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.learning_curve import learning_curve


class MLStripper(HTMLParser):
    """ It strips HTML from a string
    http://stackoverflow.com/a/925630/861399
    """

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class MailMessageProcess(models.Model):
    """ It provides an interface for Spam pre-processors """

    _name = 'mail.message.process'
    _description = 'Mail Message Processing'

    message_id = fields.Many2one(
        string='Message',
        comodel_name='mail.message',
        required=True,
    )
    clean_body = fields.Text(
        compute='_compute_clean_body',
        store=True,
    )
    is_spam = fields.Boolean(
        compute='_compute_is_spam',
        store=True,
    )
    score = fields.Float()

    @api.multi
    @api.property
    def bow_transformer(self):
        self.ensure_one()
        return CountVectorizer(analyzer=self.create_lemmas).fit(self.clean_body)

    @api.multi
    @api.depends('message_id.body')
    def _compute_clean_body(self):
        """ It preproceses a message and stores the result """
        for rec_id in self:
            stripper = MLStripper()
            rec_id.clean_body = stripper.feed(rec_id.message_id.body)

    @api.multi
    @api.depends('clean_body')
    def _compute_is_spam(self):
        """ It determines whether the message is spam """
        for rec_id in self:
            

    @api.multi
    def create_lemmas(self):
        """ It returns normalized words in their base form & PoS tag

        Returns:
            list of (Word, Part of Speech) string pairs
        """
        self.ensure_one()
        message = unicode(self.clean_body, 'utf8').lower()
        return [word.lemma for word in TextBlob(message).words]
