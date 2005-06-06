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


class SelectDialog(Widget):
    uifile = 'selectdialog.ui'

    def __init__(self):
        Widget.__init__(self)
        self.selected = None        
        self._model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        
        cell1 = gtk.CellRendererText()
        cell2 = gtk.CellRendererText()
        
        column1 = gtk.TreeViewColumn('Widget')
        column2 = gtk.TreeViewColumn('Class')        
        column1.pack_start(cell1, True)
        column2.pack_start(cell2, True)
        column1.add_attribute(cell1, 'text', 0)
        column2.add_attribute(cell2, 'text', 1)
        
        listview = self['listview']        
        listview.set_model(self._model)
        listview.append_column(column1)
        listview.append_column(column2)
    
    def set_options(self, options):
        for option in options:
            self._model.append(option)

    def on_ok_button__clicked(self, button):
        listview = self['listview']        
        selection = listview.get_selection()
        model, iter = selection.get_selected()
        self.selected = model.get_value(iter, 0)
        self.destroy()        

    def on_cancel_button__clicked(self, button):
        self.destroy()        

    
