# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class job_excel(models.Model):
    _inherit = 'hr.job'

    excel_check = fields.Boolean('Excel Test')
    excel_test = fields.Many2one('hr.excel.test','Excel Tests')

    skill_id = fields.Many2one('hr.skill')
    excel_line_ids =  fields.Many2many('excel.test', 'job_excel_rel', 'job_id', 'excel_id', 'Excel Test')

    total = fields.Integer()


    @api.onchange('excel_test')
    def update_excel_lines(self):
        if self.excel_test:
            self.skill_id = self.excel_test.skill_id.id
            self.excel_line_ids = self.excel_test.excel_line_ids
            self.total = self.excel_test.total

    @api.onchange('excel_line_ids')
    def update_lines(self):
        if self.excel_line_ids:
            sum = 0
            for row in self.excel_line_ids:
                sum += row.mark
            self.total = sum

    def write(self, values):
        res = super(job_excel, self).write(values)
        if self.excel_check:
            sum = 0
            for row in self.excel_line_ids:
                sum += row.mark

        return res


class hr_excel_test(models.Model):
    _name = 'hr.excel.test'

    name = fields.Char()
    skill_id = fields.Many2one('hr.skill')
    excel_line_ids =  fields.One2many('excel.test', 'hr_excel_test_id', 'Excel Test')
    total = fields.Integer()

    @api.onchange('excel_line_ids')
    def update_total(self):
        sum = 0
        if self.excel_line_ids:
            for row in self.excel_line_ids:
                sum += row.mark
            self.total = sum

    def write(self, values):
        res = super(hr_excel_test, self).write(values)
        if self.excel_line_ids:
            sum = 0
            for row in self.excel_line_ids:
                sum += row.mark
            if sum != 100:
                raise ValidationError(_('Exel Test total must equal 100%.'))

        return res

class excel_test(models.Model):
    _name = 'excel.test'
    _description = 'Excel Test'

    question = fields.Char()
    job_id = fields.Many2one('hr.job')
    applicant_id = fields.Many2one('hr.applicant')
    hr_excel_test_id = fields.Many2one('hr.excel.test')

    mark = fields.Integer()
    new_mark = fields.Integer()

class applicant_excel(models.Model):
    _inherit = 'hr.applicant'

    skill_id = fields.Many2one('hr.skill', related='job_id.skill_id')
    skill_level_id = fields.Many2one('hr.skill.level')
    excel_check = fields.Boolean('Excel Test',related="job_id.excel_check")
    excel_line_ids =  fields.One2many('excel.test', 'applicant_id', 'Excel Test')
    total = fields.Integer()
    result_clicked = fields.Boolean()
    @api.onchange('job_id')
    def excel_lines(self):
        if self.job_id:
            self.excel_line_ids = [(5,0,0)]
            lines = []
            for line in self.job_id.excel_line_ids:
                vals = (0, 0, {
                                'question': line.question,
                                'mark': line.mark,
                                'applicant_id':self.id
                                })
                lines.append(vals)

            self.excel_line_ids = lines

    def write(self, values):
        res = super(applicant_excel, self).write(values)
        if self.excel_line_ids:
            for value in self.excel_line_ids:
                if value.new_mark > value.mark:
                    raise ValidationError(_("The mark can't be more than the Benchmark."))
        return res

    @api.onchange('stage_id')
    def excel_lines_check_hired(self):
        if self.stage_id.name == 'Hired':
            if self.excel_line_ids:
                if not self.result_clicked:
                    raise ValidationError(_('You need to click on Excel Test Result.'))

    def compute_level(self):
        if self.excel_check:

            sum = 0
            for row in self.excel_line_ids:
                if row.new_mark > row.mark:
                    raise ValidationError(_('Mark must be less than Benchmark.'))
                sum += row.new_mark

            self.total = sum

            cur_levels = self.job_id.skill_id.skill_type_id.mapped('skill_level_ids').ids
            ids = []
            rel = "("
            for level in cur_levels:
                if level == cur_levels[-1]:
                    rel += str(level) +")"
                else:
                    rel += str(level) +","

            sql = "SELECT level_id from hr_level_to_skills_rel where level_id in" +str(rel)+ " and skill_id = "+ str(self.skill_id.id)+" ;"
            self._cr.execute(sql)
            result = self._cr.fetchall()


            for value in result:
                ids.append(value[0])
                level = self.env['hr.skill.level'].browse(value[0])
                if sum >= level.level_progress and sum <= level.progress_to:
                    self.skill_level_id = level.id
                    self.result_clicked = True
            if not self.skill_level_id:
                raise ValidationError(_('No Level Matching.'))
            self.result_clicked = True

        return True

class employee_excel(models.Model):
    _inherit = 'hr.employee'

    excel_check = fields.Boolean('Excel Test',related="job_id.excel_check")
    skill_id = fields.Many2one('hr.skill', related='job_id.skill_id')

    skill_level_id = fields.Many2one('hr.skill.level')
    excel_line_ids =  fields.One2many('excel.test', 'applicant_id', 'Excel Test')
    total = fields.Integer()
    

