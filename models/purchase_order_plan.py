from odoo import models, fields, api, _

class PurchaseOrderPlan(models.Model):
    _name = 'purchase.order.plan'
    _description = 'Purchase Order Plan'

    name = fields.Char(string='Plan Name', required=True)
    planned_by = fields.Many2one('res.users', string='Planned By', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    planned_date = fields.Date(string='Planned Date', default=fields.Date.context_today)
    description = fields.Text()
    line_ids = fields.One2many('create.planned.lines', 'plan_id', string="Planned Lines")
    state = fields.Selection([('draft', 'Draft'), ('scheduled', 'Scheduled'), ('done', 'Done')], default='draft')
    count_plans= fields.Integer(default=1)

    def order_plans(self):
        self.count_plans=5
        pass

    def action_schedule(self):
        self.state = 'scheduled'

    def action_done(self):
        self.state = 'done'
    
    def write(self, vals):
        if 'state' in vals:
            for rec in self:
                
                if vals['state'] == 'draft' and rec.state in ('scheduled', 'done'):
                    raise ValidationError(_("Cannot revert to draft once scheduled or done"))
                if vals['state'] == 'scheduled' and rec.state == 'done':
                    raise ValidationError(_("Cannot set to scheduled once done"))
        return super().write(vals)