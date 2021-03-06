# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#    Copyright (C) 2011-2013 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>).

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp.osv import fields, osv
from osv import osv
from tools.translate import _
from openerp.tools.translate import _
from datetime import datetime

class product_shipment(osv.osv):
    
    _name="product.shipment"
    _columns = {
        'partner_ref':fields.many2one('shipment.shipment', 'Referance'),
        'product_id': fields.many2one('product.product','Product'),
        'product_qty': fields.integer('Product QTY'),
    }
    
product_shipment()


class port_port(osv.osv):
    
    _name = "port.port"
    _columns = {
        'name': fields.char('Port Name', size=64, translate=True, required=True),
        'port_country_id': fields.many2one('res.country', 'Port Country', required=True),
        'address_1':fields.char('Port Address 1', size=64),
        'address_2':fields.char('Port Address 2', size=64),
        'address_3':fields.char('Port Address 3', size=64),
        'city': fields.char('Port City', size=128),
        'state_id': fields.many2one("res.country.state", 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'zip': fields.char('Zip', change_default=True, size=24),
        'phone': fields.char('Phone', size=64),
        'fax': fields.char('Fax', size=64),
  }
    
port_port()

class shipment_type(osv.osv):
    
    _name = "shipment.type"
    _columns = {
        'name':fields.char('Shipment Type', size=64, required=True),
        'method': fields.selection([('ocean_freight','Ocean Freight'),('air_freight','Air Freight'),('courier','Courier')],'Shipment Method',required=True),
        'web_tracking_link' : fields.text('Web Tracking Link'),
        'tracking_auto' : fields.boolean('Tracking Automatically')
   }
    
shipment_type()

class hs_code(osv.osv):
    
    _name = "hs.code"
    _rec_name = 'hs_code'
    _columns = {
        'hs_code':fields.char('HS Code', size=64, required=True),
        'description': fields.text('Description'),
   }
    
hs_code()

class container_type(osv.osv):
    
    _name = "container.type"
    _rec_name = 'container_type'
    _columns = {
        'container_type':fields.char('Container Type', size=64, required=True),
        'description': fields.text('Description'),
    }

container_type()


class shipment_shipment(osv.osv):
    
    _name = "shipment.shipment"
    _rec_name = 'container_no'
    
    def _get_tracking_link(self, cr, uid, ids, name, args, context=None):
        res = {}
        shipment_data = self.browse(cr, uid, ids[0], context=context)
        if shipment_data.shipment_type_id.web_tracking_link:
            if shipment_data.shipment_type_id.tracking_auto:
                if shipment_data.container_no:
                    tracking_name = shipment_data.shipment_type_id.web_tracking_link + shipment_data.container_no
                    res[shipment_data.id] = tracking_name
                else:
                    tracking_name = shipment_data.shipment_type_id.web_tracking_link + ''
            else:
                tracking_name = shipment_data.shipment_type_id.web_tracking_link
                res[shipment_data.id] = tracking_name
        else:
            res[shipment_data.id] = ''
        return res
    
    def _set_tracking_link(self, cr, uid, ids, name, value, arg, context=None):
        shipment_data = self.browse(cr, uid, ids, context=context)
        if not shipment_data.shipment_type_id.tracking_auto:
            return cr.execute("""update shipment_shipment set tracking_link=%s where id=%s""", (value, shipment_data.id))
        
    def _get_tracking_mark(self, cr, uid, ids, name, value, arg, context=None):
        res = {}
        flag = False
        shipment_data = self.browse(cr, uid, ids[0], context=context)
        if shipment_data.shipment_type_id.tracking_auto:
            flag = True
        res[shipment_data.id] = flag
        return res
    
    _columns = {
        'shipment_type_id':fields.many2one('shipment.type', 'Shipment Type', required=True),
        'method': fields.selection([('ocean_freight','Ocean Freight'),('air_freight','Air Freight'),('courier','Courier')],'Shipment Method'),
        'port_of_deprature_id':fields.many2one('port.port', 'Port of departure'),
        'port_of_destination_id':fields.many2one('port.port', 'Port of destination'),
        'origination_address_id':fields.many2one('port.port', 'Origination Address'),
        'destination_address_id':fields.many2one('port.port', 'Destination Address'),
        'ship_origination_address_id' : fields.many2one('res.partner', 'Origination Address'),
        'ship_partner_address_id' : fields.many2one('res.partner', 'Partner Address'),
        'state':fields.selection([('transit','In Transit'), ('received','Received'), ('cancel', 'Cancel')], 'State' ),
        'customer_id':fields.many2one('res.partner', 'Customer', required=True),
        'factory_pickle_date': fields.date(' Factory Pickup Date'),
        'estimated_departure_date': fields.date('Estimated Departure Date'),
        'actual_deprature_date': fields.date('Actual Departure Date'),
        'estimated_arrival_date': fields.date('Estimated Arrival Date'),
        'actual_arrival_date': fields.date('Actual Arrival Date'),
        'container_type_id':fields.many2one('container.type', 'Container Type'),
        'container_no':fields.char('Tracking/Container Number', size=64),
        'container_owner':fields.selection([('customer_soc','Customer (SOC)'), ('return_to_carrier','Return to Carrier')], 'Container Owner'),
        'seal_no':fields.char('Seal Number', size=64),
        'obl_no':fields.char('OBL Number', size=64),
        'weight':fields.char('Weight (kg)', size=64),
        'hs_code_id':fields.many2one('hs.code','HS Code'),
        'description':fields.text('Description of Goods'),
        'tracking_link' : fields.function(_get_tracking_link, fnct_inv=_set_tracking_link, type="char", string="Tracking Link", store=True),
        'shipping_cost':fields.integer('Shipping Cost'),
        'crane_at_factory':fields.integer(' Crane At Factory'),
        'factory_to_port':fields.integer('Factory to Port '),
        'brokerage':fields.integer('Brokerage'),
        'port_to_customer':fields.integer('Port to Customer'),
        'product_ids':fields.one2many('product.shipment','partner_ref','Product'),
        'note':fields.text('Notes'),
        'image':fields.text('Images'),
        'tracking_mark' : fields.function(_get_tracking_mark, type='boolean', string='Tracking Mark', store=True),
        'container' : fields.boolean('Container'),
        'courier' : fields.boolean('Courier'),
   }
    
    _defaults = {
        'state': 'transit'
    }
    
    def on_change_shipment_type_id(self, cr, uid, ids, shipment_type_id):
        res = {}
        shipment_type_obj = self.pool.get('shipment.type')
        shipment_type_data =  shipment_type_obj.browse(cr, uid, shipment_type_id)
        if shipment_type_data.method == 'ocean_freight':
            res.update({'value':{'method' : 'ocean_freight', 'container' : True, 'courier' : False}})
        elif shipment_type_data.method == 'courier':
            res.update({'value':{'method' : 'courier', 'courier' : True, 'container' : False}})
        elif shipment_type_data.method == 'air_freight':
            res.update({'value':{'method' : 'air_freight', 'container' : True, 'courier' : False}})
#        if shipment_type_data.method in ('courier'):
#            if shipment_type_data.method in ('courier'):
#                res.update({'value':{'courier' : True, 'container' : False}})
#            else:
#                res.update({'value':{'container' : True, 'courier' : False}})
#            elif shipment_type_data.method in ('courier', 'Courier'):
#                res.update({'value':{'courier' : True, 'container' : False}})
#            elif shipment_type_data.method not in ('courier', 'Courier','container', 'Container'):
#                res.update({'value':{'courier' : False, 'container' : False}})
#        if shipment_type_data.name in ('container', 'Container','courier', 'Courier'):
#            if shipment_type_data.name in ('container', 'Container'):
#                res.update({'value':{'container' : True, 'courier' : False}})
#            elif shipment_type_data.name in ('courier', 'Courier'):
#                res.update({'value':{'courier' : True, 'container' : False}})
#            elif shipment_type_data.name not in ('courier', 'Courier','container', 'Container'):
#                res.update({'value':{'courier' : False, 'container' : False}})
        return res
    def next_state(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state' : 'received'}, context=context)
    
    def previous_state(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state' : 'transit'}, context=context)
    
shipment_shipment()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: