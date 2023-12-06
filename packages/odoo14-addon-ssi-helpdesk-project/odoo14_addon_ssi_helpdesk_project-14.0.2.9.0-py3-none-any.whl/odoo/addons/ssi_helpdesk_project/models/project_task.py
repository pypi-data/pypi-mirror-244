# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = [
        "project.task",
    ]

    ticket_ids = fields.Many2many(
        string="Tickets",
        comodel_name="helpdesk_ticket",
        relation="rel_helpdesk_ticket_2_task",
        column1="task_id",
        column2="ticket_id",
    )

    @api.depends(
        "ticket_ids",
        "ticket_ids.date_deadline",
        "ticket_ids.state",
    )
    def _compute_ticket_deadline(self):
        for record in self:
            if record.ticket_ids:
                ticket_deadline = (
                    record.ticket_ids.filtered(
                        lambda x: x.date_deadline is not False
                        and x.state not in ["cancel", "done", "rejected"]
                    )
                    .sorted("date_deadline")
                    .mapped("date_deadline")
                )
                if ticket_deadline:
                    record.ticket_deadline = ticket_deadline[0]
                else:
                    record.ticket_deadline = False
            else:
                record.ticket_deadline = False

    ticket_deadline = fields.Date(
        string="Ticket Deadline",
        compute="_compute_ticket_deadline",
        store=True,
    )
