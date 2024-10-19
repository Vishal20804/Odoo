from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError
class Requisition(models.Model):

    _name="requisition"

    no=fields.Char("Number ")
    date=fields.Datetime("Date ")
    buyer_order_no=fields.Char("Buyer Order No")
    customer_id=fields.Many2one("res.partner", string="Customer")
    requisition_line=fields.One2many("mannual.requisition.line","requisition_id",string="Requisition_line")
    sale_order_ids=fields.Many2many('sale.order' ,string="Sales")

    def create_line(self):
        for records in self.sale_order_ids:
            sale_order_lines = records.order_line

            for line in sale_order_lines:
                self.env['mannual.requisition.line'].create({
                    'requisition_id': self.id,               
                    'sale_id': records.id,                    
                    'product_id': line.product_id.id,         
                    'description': line.name,                
                    'qty': line.product_uom_qty,            
                    'unit_price': line.price_unit,            
                    'sub_total': line.price_total,            
                   
                })

        

class Mannual_Requisition_line(models.Model):
    _name="mannual.requisition.line"

    requisition_id=fields.Many2one("requisition", string="Requisitio Id")
    sale_id=fields.Many2one('sale.order', string="Sales Id")
    product_id=fields.Many2one("product.product", string="Product")
    image=fields.Binary("Image")
    description=fields.Char("Description")
    qty=fields.Float("Quantity")
    delivered_qty=fields.Float("Deliverd Qty")
    balance_qty=fields.Float("Balance Qty")
    unit_price=fields.Float("Unit Price")
    sub_total=fields.Float("Sub Total")







    @api.onchange('qty','delivered_qty')
    def __onchange_bal(self):
        self.update({
            "balance_qty": self.qty - self.delivered_qty
        })

    @api.onchange("delivered_qty","qty")
    def _onchange_raise_error(self):
        if self.delivered_qty >  self.qty:
            raise UserError("Delivered Qty should be less!!!")


    @api.onchange('delivered_qty','unit_price')
    def __onchange_sub_total(self):
        self.update({
            "sub_total": self.unit_price * self.delivered_qty
        })







