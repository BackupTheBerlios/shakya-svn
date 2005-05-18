############################################################################
#    Copyright (C) 2005 by Eric Jardim                                     #
#    ericjardim@gmail.com                                                  #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import gobject
import gtk
import shakya.fw.property as property

_default_handlers = {}


class PropertyHandler:
    """
    Property handler interface
    """
    
    def __init__(self, owner, info):
        self.info = info
        self.owner = owner
        self._block = False
        
        start = getattr(self, 'init')
        
        #owner.connect("notify", self.on__owner__notify)
        
        if self.init:
            self.init(owner, info, **info.opt)
        
        owner.connect("notify", self.on__owner__notify)

    def get_widget(self):
        return self.widget

    def __del__(self):
        print 'argh....'

    def update(self):
        pass
    
    def on__owner__notify(self, owner, param):
        if self._block: return
        if param.name == self.info.name:
            #print 'notify', owner, param
            self.update()

    def block(self):
        self._block = True
    
    def unblock(self):
        self._block = False



class GParamBoolean_handler(PropertyHandler):    
    def init(self, owner, info, **opt):
        widget = gtk.ToggleButton()
        self.widget = widget
        widget.show()
        widget.set_active(owner.get_property(info.name))
        self.update()
        widget.connect("toggled", self.on__button__toggled)

    def on__button__toggled(self, button):
        name = self.info.name
        owner = self.owner
        
        value = owner.get_property(name)
        self.owner.set_property(name, not value)        

    def update(self):        
        if self.owner.get_property(self.info.name):
            self.widget.set_label('Yes')
        else:
            self.widget.set_label('No')        
    



class GParamString_handler(PropertyHandler):
    def init(self, owner, info, **opt):
        self.widget = gtk.Entry()
        self.widget.show()


class GParamUInt_handler(PropertyHandler):
    pass


class GParamInt_handler(PropertyHandler):
    pass



class GParamFloat_handler(PropertyHandler):
    def init(self, owner, info, **opt):        
        widget = gtk.HScale()
        widget.set_range(opt.get('bottom', 0), opt.get('top', 1))
        widget.set_digits(opt.get('digits', 2))
        widget.set_value(opt.get('value', 0))
        widget.set_increments(opt.get('step', 0.1), opt.get('step', 0.1))        
        widget.show()        
        self.widget = widget
        
        self.update()
        widget.connect("value-changed", self.on__scale__value_changed)

    def on__scale__value_changed(self, scale):
        self.block()
        self.owner.set_property(self.info.name, scale.get_value())
        self.unblock()

    def update(self):
        #print 'update'
        value = self.owner.get_property(self.info.name)
        self.widget.set_value(value)


class GParamDouble_handler(GParamFloat_handler):
    pass

class GParamObject_handler(PropertyHandler):
    pass


def get_default_handler(klass, name):
    properties = gobject.list_properties(klass)    
    for property in properties:
        if property.name == name:
            property_type = gobject.type_name(property)
            break
    
    return _default_handlers[property_type]
    
    
    
# register all handlers and fetchers
for type_id in property._properties:
    handler = eval('%s_handler' % (type_id))    
    print type(handler)
    _default_handlers[type_id] = handler
    
