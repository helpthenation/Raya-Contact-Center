from itertools import groupby
from odoo.osv import expression
from odoo import api, fields, models , _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang
from datetime import date, timedelta

class blacklist_warning_wizard(models.Model):
    _name = 'blacklist.warning.wizard'
    _description = 'Blacklist !?'

    def do_blacklist(self):
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        applicant = self.env['hr.applicant'].browse(active_ids)
        return applicant.do_blacklist()


class unblacklist_warning_wizard(models.Model):
    _name = 'unblacklist.warning.wizard'
    _description = 'Unblacklist !?'

    def do_un_blacklist(self):
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        applicant = self.env['hr.applicant'].browse(active_ids)
        return applicant.do_un_blacklist()
