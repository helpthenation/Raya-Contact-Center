from odoo import models, fields, api,_


class screening_questions(models.Model):
    _name = 'screening_questions'
    _description = 'screening_questions'

    name = fields.Char(compute="_compute_name")
    question=fields.Char(string="Question")
    @api.onchange('question')
    def _compute_name(self):
        for this in self:
            if this.question:
                this.name = this.question
    answer=fields.Selection([('0','No'),('1','Yes')],string="Yes & No")



class screening_application(models.Model):
    _name = 'screening_application'

    linker=fields.Many2one('hr.applicant')
    question=fields.Char(string="Question")
    answer=fields.Selection([('0','No'),('1','Yes')],string="Yes & No")
    note = fields.Char()




class Job(models.Model):
    _inherit = "hr.job"

    screening_check = fields.Boolean('Screening Question')
    question=fields.Many2many('screening_questions','question')
    answer=fields.Selection([('0','No'),('1','Yes')],string="Yes & No")
class Applicant(models.Model):
    _inherit='hr.applicant'

    black_listed = fields.Boolean()
    screening_check = fields.Boolean('Screening Question', related="job_id.screening_check")
    question=fields.One2many('screening_application','linker')
    is_initial=fields.Boolean(compute='get_is_initial',sorted=True)
    is_final=fields.Boolean(compute='get_is_final',sorted=True)
    @api.onchange('stage_id')
    def get_is_final(self):
        for this in self:
            this.is_final=this.stage_id.is_final
    @api.onchange('stage_id')
    def get_is_initial(self):
        for this in self:
            self.is_initial=this.stage_id.is_initial
    def read(self, fields=None, load='_classic_read'):
        res = super(Applicant, self).read(fields, load)
        for this in self:
            question_ids = self.env['hr.job'].search([('id','=',this.job_id.id)],limit=1)
            lines = []
            if len(this.question)>0:
                pass
            else:
                for line in question_ids.question:
                    vals = (0, 0, {
                    'question': line.question,
                    'answer': line.answer,
                    'linker':this.id
                    })
                    lines.append(vals)
                this.question=lines
        return res
