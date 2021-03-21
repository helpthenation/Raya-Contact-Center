# -*- coding: utf-8 -*-
##############################################################################
#
#    Jupical Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Jupical Technologies Pvt. Ltd.(<http://www.jupical.com>).
#    Author: Jupical Technologies Pvt. Ltd.(<http://www.jupical.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Update Profiles',
    'summary': 'Update profile picture from website',
    'version': '13.0.0.1.0',
    'category': 'Website',
    'author': 'Jupical Technologies Pvt. Ltd.',
    'maintainer': 'Jupical Technologies Pvt. Ltd.',
    'live_test_url': 'http://www.jupical.com/contactus',
    'contributors': ['Anil Kesariya <anil.r.kesariya@gmail.com>'],
    'website': 'http://www.jupical.com ',
    'depends': ['base','website', 'portal','interview_feedback','hr_recruitment','wc_sourcing_extension','wc_ta_extention','wc_hiring_request','hr_recruitment_double_hiring','wc_raya_quality','hr_skill_qualification','wc_interview_checklist'],
    'data': [
        'views/update_profile_template.xml',
        'views/views.xml',
        'views/warning_wizard.xml',
        'ir.model.access.csv'

    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'images': ['static/description/poster_image.png'],
}
