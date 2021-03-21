console.log('my ReconciliationRenderer is loaded');

odoo.define('web.FieldSkills', function (require) {
"use strict";

var time = require('web.time');

// var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
// var FieldProgressBar = require('web.basic_fields').FieldProgressBar;
// var ListRenderer = require('web.ListRenderer');
var field_registry = require('web.field_registry');
console.log(field_registry);

// var rpc = require('web.rpc');
// var resume_widget = require('hr_skills.resume_widget').hr_skills;

// console.log(typeof field_registry);
// console.log(Object.entries(field_registry)[0][1]);
//
// function convert(obj) {
//     return Object.keys(obj).map(key => ({
//         name: key,
//         value: obj[key],
//         type: "foo"
//     }));
// }

// console.log(resume_widget);

var core = require('web.core');
var qweb = core.qweb;
// var _t = core._t;
//
// field_registry.hr_skills.include({
//
//
//     groupBy: 'skill_type_id',
//     dataRowTemplate: 'hr_skill_data_row',
//
//
//     _renderValidationIcon: function() {
//         return qweb.render('hr_check_button');
//     },
//
//     _renderRow: function (record) {
//         var $row = this._super(record);
//         // Add progress bar widget at the end of rows
//         var $td = $('<td/>', {class: 'o_data_cell o_skill_cell'});
//         var progress = new FieldProgressBar(this, 'level_progress', record, {
//             current_value: record.data.level_progress,
//             attrs: this.arch.attrs,
//         });
//         progress.appendTo($td);
//         $row.append($td);
//
//         var $validite = $(this._renderValidationIcon());
//         var today = new Date()
//         var nowDate = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
//         var d1 = Date.parse(record.data.validation_date);
//         var d2 = Date.parse(nowDate);
//         if (d1 < d2) {
//             $row.append($validite);
//         }
//
//           console.log('record.data');
//           console.log(record);
//           // console.log($validite.find('validite1'));
//           console.log('record.data');
//
//         return $row;
//     },
//
//     _getCreateLineContext: function (group) {
//         var ctx = this._super(group);
//         return group ? _.extend({ default_skill_type_id: group[0].data[this.groupBy].data.id }, ctx) : ctx;
//     },
//
//     _render: function () {
//         var self = this;
//         return this._super().then(function () {
//             self.$el.find('table').toggleClass('table-striped');
//         });
//     },
// });


});
