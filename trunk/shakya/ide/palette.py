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

import gtk
from shakya.widget import Widget

class Palette(Widget):
    """ 
    The palette is a widget that have icons of the components that
    can be used to construct new composite widgets.
    
    Once you click such icon, the widget is created on the current
    User Interface being designed.
    """
    
    def load(self):
        #expander = gtk.Expander()        
        #expander.set_name('expander')
        
        notebook = gtk.Notebook()
        notebook.set_name('notebook')
        #notebook.show() 
        #expander.add(notebook)        
        
        label = gtk.Label('Palette')
        label.show()
        notebook.add(label)
        
        self._widget = notebook

    def init(self, **opt):
        pass

##    def after__expander__activate(self, expander):
##        parent = expander.get_parent()
##        #value = parent.child_get_property(expander, 'expand')
##        #parent.child_set_property(expander, 'expand', not value)
##        value = parent.child_get_property(expander, 'shrink')
##        parent.child_set_property(expander, 'shrink', not value)
##        #expander.set_label(str(value))





