# -*- coding: utf-8 -*-

import gtk
import gobject
import shakya.fw as fw

class PropertiesWindow(fw.Widget):
    widgetfile = 'list.ui'
    
    def __init__(self):
        fw.Widget.__init__(self)
        model = gtk.ListStore(str, str)
        for i in gobject.list_properties(self._widget):
            model.append([i.name, gobject.type_name(i)+': '+gobject.type_name(i.value_type)])
        cell = gtk.CellRendererText()
        cell2 = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Name')
        column2 = gtk.TreeViewColumn('Type')
        column.pack_start(cell, True)
        column2.pack_start(cell2, True)
        column.add_attribute(cell, 'text', 0)
        column2.add_attribute(cell2, 'text', 1)
        listview = self._widgets['treeView']
        listview.set_model(model)
        listview.append_column(column)
        listview.append_column(column2)
        
    
    def on_okButton__clicked(self, button, data=None):
        print '%s clicked' % button.name
    
    def on_widgetBrowser__destroy(self, window, data=None):
        fw.Application.quit()
