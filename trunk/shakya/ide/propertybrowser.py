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
#import propertyfilters as filters
#import shakya.fw.property as property


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
    
    def clean(self, size):
        tab = self.child('standard_tab')
        for w in tab.get_children():
            tab.remove(w)
        tab.resize(size+1, 2)
    
    def update(self):
        obj = self.__object
        infos = property.info.fetch(obj)
        print infos
        
        tab = self.child('standard_tab')        
        self.clean(len(infos))
        
        i = 0
        for info in infos:
            label = gtk.Label()
            label.set_text(info.name)
            label.show()
            
            tab.attach(label, 0, 1, i, i+1, yoptions=gtk.SHRINK) 
            
            handler = info.Handler(obj, info)
            widget = handler.get_widget()
            tab.attach(widget, 1, 2, i, i+1, yoptions=gtk.SHRINK)
            i += 1
        
        tab.attach(self.spacer, 1, 2, i, i+1)

    def on_property_browser__delete_event(self, widget, event):
        widget.hide()
        return True


    def on_property_browser__destroy(self, widget):
        print 'ahhh...'
