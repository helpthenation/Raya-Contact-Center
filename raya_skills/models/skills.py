# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class employee_enhancement_hr_skill_type(models.Model):
    _inherit = 'hr.skill.type'

    skill_type = fields.Selection([('language','Language'),('technical','Technical'),('non_technical','Non-Technical')])

class employee_enhancement_hr_skill(models.Model):
    _inherit = 'hr.skill'

    expiry_skill = fields.Boolean()


class employee_enhancement_hr_skill_level(models.Model):
    _inherit = 'hr.skill.level'

    def _damin_skills(self):
        skills = self.env['hr.skill'].search([('skill_type_id','=',self.env.context.get('default_skill_type_id'))])
        return [('id','in', skills.ids)]
    skills_ids = fields.Many2many('hr.skill', 'hr_level_to_skills_rel', 'level_id', 'skill_id', domain=_damin_skills)

    progress_to = fields.Integer('Progress To (%)')


class employee_enhancement_hr_employee_skill(models.Model):
    _inherit = 'hr.employee.skill'
    
    current_degree=fields.Integer(string="Test Degree")
    @api.onchange('skill_id')
    def _update_levels_domain(self):

        if self.skill_level_id.id == False:
            if self.skill_type_id.id and self.skill_id.id:
                cur_levels = self.skill_type_id.mapped('skill_level_ids').ids
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

                return {
                    'domain': {
                        'skill_level_id': [('id', 'in', ids)],
                    }
                }
    expiry_skill = fields.Boolean(related="skill_id.expiry_skill")

    validation_date = fields.Date('')

    employee_lang_id =fields.Many2one('hr.employee')
    employee_tech_id =fields.Many2one('hr.employee')
    employee_non_tech_id =fields.Many2one('hr.employee')




class employee_enhancement_hr_employee(models.Model):
    _inherit = 'hr.employee'

    employee_lang_skill_ids = fields.One2many('hr.employee.skill', 'employee_lang_id', string="Language")
    employee_tech_skill_ids = fields.One2many('hr.employee.skill', 'employee_tech_id', string="Technical")
    employee_non_tech_skill_ids = fields.One2many('hr.employee.skill', 'employee_non_tech_id', string="Non-Technical")

    def open_update_validity(self):

        return {
            'name': _('Update'),
            'view_mode': 'form',
            'res_model': 'validate.skills',
            'view_id': self.env.ref('raya_skills.validate_skills_wizard_form').id,
            'type': 'ir.actions.act_window',
            'context': {
                        'hr_employee_id': self.id,
                        'skill_ids':self.employee_skill_ids.filtered(lambda x:x.expiry_skill == True).mapped('skill_id').ids,
                        },
            'target': 'new',
        }
class employee_enhancement_validate_skills(models.Model):
    _name = 'validate.skills'

    validate_lines = fields.One2many('validate.skills.line','validation_id')
    def update_validity(self):
        hr_employee_id = self.env['hr.employee'].browse(self.env.context.get('hr_employee_id'))

        for new in self.validate_lines:
            for emp in hr_employee_id.employee_skill_ids:
                if emp.skill_id == new.skill_id:
                    msg = "Hello, Mr " + (self.env.user.name) +"\n updated Skill "+str(emp.skill_id.name)
                    if new.level_id:
                        msg += " Level "+str(emp.skill_level_id.name)+" to "+str(new.level_id.name)
                        emp.skill_level_id = new.level_id.id
                    if new.date:
                        if new.level_id:
                            msg += "and Date "+str(emp.validation_date)+" to "+str(new.date)
                        else:
                            msg += " Date "+str(emp.validation_date)+" to "+str(new.date)

                        emp.validation_date = new.date


                    hr_employee_id.message_post(body=msg)


class employee_enhancement_validate_skills(models.Model):
    _name = 'validate.skills.line'

    @api.onchange('skill_id')
    def update_vals(self):
        self.skill_type_id = self.skill_id.skill_type_id
        if self.level_id.id == False:
            if self.skill_type_id :
                cur_levels = self.skill_type_id.mapped('skill_level_ids').ids
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

                # return ['id','in', ids]
                return {
                    'domain': {
                        'level_id': [('id', 'in', ids)],
                    }
                }


    def _skill_id_domain(self):
        skill_ids = self.env.context.get('skill_ids', [])
        return [('id', 'in', skill_ids)]

    skill_id = fields.Many2one('hr.skill', string="Skill", domain=_skill_id_domain, required=True )
    level_id = fields.Many2one('hr.skill.level', string="New level")
    date = fields.Date("Validation Date")
    employee_id = fields.Many2one('hr.employee')
    validation_id = fields.Many2one('validate.skills')

    skill_type_id = fields.Many2one('hr.skill.type')
