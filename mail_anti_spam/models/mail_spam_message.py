# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import api, fields, models

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


class MailSpamMessage(models.Model):
    _name = 'mail.spam.message'
    _inherits = {'mail.message': 'message_id'}

    _message_blob = None

    message_id = fields.Many2one(
        string='Message',
        comodel_name='mail.message',
        required=True,
        ondelete='cascade',
    )
    is_spam = fields.Boolean(
        compute='_compute_is_spam_and_score',
        store=True,
    )
    is_training = fields.Boolean(
        help='This is a training message',
    )
    spam_score = fields.Float(
        compute='_compute_is_spam_and_score',
        store=True,
    )
    spam_model_id = fields.Many2one(
        string='Spam Model',
        comodel_name='mail.spam',
    )
    word_lemmas = fields.Serialized(
        compute='_compute_word_lemmas',
        store=True,
    )
    # @TODO: Add vector for parts of speech
    # word_pos = fields.Serialized(
    #     compute='_compute_word_pos',
    #     store=True,
    #     help='Word Parts of Speech Matrix',
    # )

    @property
    @api.multi
    def message_blob(self):
        """ It creates a TextBlob of the processed message body """
        self.ensure_one()
        if not self._message_blob:
            processed = self._preprocess_message()
            self._message_blob = TextBlob(processed)
        return self._message_blob

    @api.multi
    def _compute_is_spam_and_score(self, message):
        """ It determines whether the message is spam """
        for rec_id in self:
            pass

    @api.multi
    @api.depends('message_id.body')
    def _compute_word_lemmas(self):
        for rec_id in self:
            rec_id.word_lemmas = [
                word.lemma for word in rec_id.message_blob.words
            ]

    @api.multi
    def _preprocess_message(self):
        """ It preproceses a message and returns the result """
        self.ensure_one()
        cleaned = html2plaintext(self.message.body)
        return unicode(cleaned, 'utf8').lower()
