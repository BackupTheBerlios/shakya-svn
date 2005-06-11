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
from shakya import Widget


class WidgetTree(Widget):
    uifile = 'widgettree.ui'

    def init(self):
        # name, class
        self._model = gtk.TreeStore(str, str, object)
        treeview = self['treeview']
        treeview.set_model(self._model)
        treeview.connect("row-activated", self.selected)        
        treeview.connect("cursor-changed", self.changed)
        
        iconCell = gtk.CellRendererPixbuf()
        iconCell.set_property('stock_id', 'gtk-new')
        nameCell = gtk.CellRendererText()
        nameCol = gtk.TreeViewColumn('Name')
        nameCol.pack_start(iconCell)
        nameCol.pack_start(nameCell)
        nameCol.add_attribute(nameCell, 'text', 0)
        nameCol.set_visible(True)
        nameCol.set_resizable(True)
        
        classCell = gtk.CellRendererText()
        classCol = gtk.TreeViewColumn('Class')
        classCol.pack_start(classCell)
        classCol.add_attribute(classCell, 'text', 1)
        classCol.set_visible(True)
        classCol.set_resizable(True)
        
        treeview.append_column(nameCol)
        treeview.append_column(classCol)
        
        self.show_all()

    def changed(self, treeview):
        print 'changed'
        selection = treeview.get_selection()
        model, iter = selection.get_selected()
        #model = self._model
        #iter = model.get_iter(path)
        widget, = model.get(iter, 2)
        self.owner().set_current_widget(widget)
        #self.__widget.show()
    
    def selected(self, treeview, path, view_column):
        print 'selected'

    def set_widget(self, widget):
        self.__widget = widget
        model = self._model
        model.clear()        
        self.append_widget_to_model(widget, None, model)
    
    def append_widget_to_model(self, widget, parent_iter, model):
        iter = model.append(parent_iter, _widget_data(widget))
        if gobject.type_is_a(widget, 'GtkContainer'):
            for child in widget.get_children():
                self.append_widget_to_model(child, iter,  model)
    
    
def _widget_data(widget):
    return widget.get_name(), gobject.type_name(widget), widget
    


