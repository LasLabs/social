# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import api, fields, models
from odoo.tools.mail import html2plaintext

_logger = logging.getLogger(__name__)

try:
    from nltk import word_tokenize, pos_tag
except ImportError:
    _logger.warning('Cannot import nltk')

try:
    from textblob import TextBlob
except ImportError:
    _logger.warning('Cannot import textblob')

try:
    from sklearn.feature_extraction.text import CountVectorizer
except ImportError:
    _logger.warning('Cannot import sklearn')


class MailSpam(models.Model):
    """ It provides an interface for Spam pre-processors and training """

    _name = 'mail.spam'
    _description = 'Mail Spam'

    _count_vectorizer = None
    _word_vector = None

    sample_size = fields.Integer(
        default=2000,
        required=True,
    )
    trained_message_ids = fields.Many2many(
        string='Trained Messages',
        comodel_name='mail.message.spam',
        compute='_compute_trained_message_ids',
        store=True,
    )
    trained_model = fields.Serialized(
        compute='_compute_trained_model',
        store=True,
    )
    tested_message_ids = fields.Many2many(
        string='Tested Messages',
        comodel_name='mail.message.spam',
    )
    processed_message_ids = fields.One2many(
        string='Processed Messages',
        comodel_name='mail.message.spam',
    )
    active = fields.Boolean()
    date_trained = fields.Datetime(
        compute='_compute_date_trained',
        store=True,
    )
    date_expired = fields.Datetime(
        compute='_compute_date_expired',
        store=True,
    )

    @property
    @api.model_cr
    def count_vectorizer(self):
        if not self._count_vectorizer:
            self._count_vectorizer = CountVectorizer(
                analyzer='word',
                preprocessor=self._preprocess_message,
                tokenizer=self._get_lemmas,
            )

    @property
    @api.multi
    def word_vector(self):
        self.ensure_one()
        if not self._word_vector:
            self._word_vector = self._count_vectorizer.fit_transform(
                self.trained_message_ids.mapped('body')
            )
        return self._word_vector

    @api.multi
    @api.depends('sample_size')
    def _compute_trained_message_ids(self):
        for rec_id in self:
            rec_id.cr.execute("""
                SELECT id
                  FROM mail_spam
                 WHERE is_training = true
                 ORDER BY random()
                 LIMIT %d
            """,
                (rec_id.sample_size)
            )
            res = rec_id.cr.fetchall()
            self.trained_message_ids = [
                (6, 0, (_id for (_id,) in res))
            ]

    @api.multi
    @api.depends('trained_message_ids')
    def _compute_trained_model(self):
        for rec_id in self:
            

    @api.model
    def load_training_data(self, file_handler, spam=True):
        """ """

    @api.model
    def train_new(self, sample_size=None):
        

    @api.model_cr
    def _get_lemmas(self, message_body):
        message_blob = TextBlob(message_body)
        return [word.lemma for word in message_blob.words]

    @api.model_cr
    def _preprocess_message(self, message_body):
        """ It preproceses a message and returns the result """
        cleaned = html2plaintext(message_body)
        return unicode(cleaned, 'utf8').lower()
