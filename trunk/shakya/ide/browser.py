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

class Browser(Widget):
    """ 
    The palette is a generic widget that can contain severeal context-sensitive
    sub browsers like project browser, action browser, widget browser and so on.    
    """
    
    def load(self):
        notebook = gtk.Notebook()
        notebook.set_name('notebook')
        
        #label = gtk.Label('Browser')
        #label.show()
        #notebook.add(label)
        
        self._widget = notebook

    def init(self, **opt):
        pass    
