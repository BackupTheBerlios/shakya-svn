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
import shakya 
import shakya.fw as fw 
import property.info 

_tabs = { 0: 'standard_tab', 1: 'common_tab', -1: 'packing_tab', -2: 'signals_tab'}


class PropertyBrowser(fw.Widget):
    uifile = shakya.basedir()+'ide/propertybrowser.ui'
    
    def __init__(self):
        fw.Widget.__init__(self)
        self.__object = None
        self.spacer = gtk.Frame()        
    
    def set_object(self, obj):
        #if object:
        #    print 'Receiving: %s' % object.get_name()
        self.__object = obj
        self.update()
    
    def clean(self):
        for context in _tabs.values():
            tab = self[context]
            
            for w in tab.get_children():
                tab.remove(w)
                w.destroy()
            
            tab.resize(1, 2)

    def add_handler(self, title, handler, context):
        tab = self[_tabs[context]]
        
        row = tab.get_property('n-rows')
        tab.set_property('n-rows', row+1)
        
        label = gtk.Label(title)
        label.show()        
        tab.attach(label, 0, 1, row-1, row, yoptions=gtk.SHRINK, xoptions=gtk.SHRINK)  
        tab.attach(handler, 1, 2, row-1, row, yoptions=gtk.SHRINK, xoptions=gtk.EXPAND|gtk.FILL)
    
    def add_spacers(self):
        for name in _tabs.values():
            tab = self[name]
            row = tab.get_property('n-rows')
            tab.attach(self.spacer, 0, 2, row-1, row)

    def update(self):
        obj = self.__object
        infos = property.info.fetch(obj)
        print infos
        
        self.clean()
        
        for info in infos:
            handler = info.Handler(obj, info)            
            self.add_handler(info.name, handler.get_widget(), info.tab)
        
        self.add_spacers()

    def on_property_browser__delete_event(self, widget, event):
        widget.hide()
        return True


    def on_property_browser__destroy(self, widget):
        print 'ahhh...'
