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
import gtk.glade as glade
import shakya 
from shakya import Widget, Application
from shakya import loader
from shakya import saver
from propertybrowser import PropertyBrowser
from opendialog import OpenDialog
from savedialog import SaveDialog
from selectdialog import SelectDialog
from objectbrowser import WidgetTree


default_locations = { 'main_window': (0, 0),
                      'property_browser': (-1, 0) 
                    }


class MainWindow(Widget):
    uifile = 'mainwindow.ui'

    def init(self):
        # get screen
        win = self['main_window']
        screen = win.get_screen()
        print screen.get_width(), screen.get_height()
        
        self.current_window = None
        
        self.move(0,0)
        #print self.get_position()
       
        browser = PropertyBrowser(self)
        browser.show()
        self.browser = browser
        
        self.tree = WidgetTree(self)
        self.tree.show()
        self.tree.move(0, self.get_height()+60)
        
        self['toolbar'].set_style(gtk.TOOLBAR_ICONS)
        
        w, h = browser['property_browser'].get_size()
        browser['property_browser'].move(screen.get_width()-w, self.get_height()+60)
        

    #def on_main_window__show(self, widget):
    
    def set_current_window(self, window):
        self.current_window = window
        window.hide()
        window.set_position(gtk.WIN_POS_CENTER)
        w, h = window.get_default_size()
        if w > 0 and h > 0:
            window.resize(w, h)
        window.show()
        self.tree.set_widget(window)
    
    
#    def on_import_ui__activate(self, action):
#        filters = [("User Interface files (*.ui)", "*.ui"),
#                   ("All files", "*")]
#        dialog = OpenDialog(self['main_window'], filters)
#        res = dialog.run()
#        
#        if res == gtk.RESPONSE_OK:
#            filename = dialog.get_filename()
#            window = loader.load_widget(filename)
#            self.set_current_window(window)
#        
#        dialog.destroy()

    def on_import_glade__activate(self, action):
        filters = [("Glade files (*.glade)", "*.glade"),
                   ("All files", "*")]
        dialog = OpenDialog(self['main_window'], filters)
        res = dialog.run()
        
        if res == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            print filename
            
            seldialog = SelectDialog(self)
            widgets = loader.get_glade_widgets(filename)
            seldialog.set_options(widgets)
            seldialog.set_transient_for(self['main_window'])
            seldialog.connect("destroy", self.import_glade, seldialog, filename)
            seldialog.set_position(gtk.WIN_POS_CENTER)
            seldialog.show()
            
        dialog.destroy()
    
    def import_glade(self, window, seldialog, filename):
        widget = seldialog.selected
        if widget:
            xml = glade.XML(filename, widget)
            window = xml.get_widget(widget)
            self.set_current_window(window)

    def on_open__activate(self, action):
        filters = [("User Interface files (*.ui)", "*.ui"),
                   ("Python modules (*.py)", "*.py"),
                   ("All files", "*")]
        dialog = OpenDialog(self['main_window'], filters)
        res = dialog.run()
        
        if res == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            window = loader.load_ui(filename)
            self.set_current_window(window)
        
        dialog.destroy()

    def on_save__activate(self, action):
        dialog = SaveDialog(self['main_window'])
        res = dialog.run()
        
        if res == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            print filename
            saver.save_ui(filename, self.current_window)
        
        dialog.destroy()

    def on_quit__activate(self, action):
        self.quit()

    def on_main_window__destroy(self, window):
        self.quit()

    def quit(self):
        print 'ending Shakya IDE'
        self.app().quit()

    def set_current_widget(self, widget):
        self.browser.set_object(widget)

#browser.set_object(window)
#window.connect('set-focus', on_focus, browser)    

def on_focus(window, widget, browser):
    browser.set_object(widget)
    
    if widget is None:
        print 'No focus'
    else:
        print 'focus: %s' % widget
