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
import os


class Application:
    __context = {}
    
    def __init__(self, root, context=None):        
        self.__path = os.path.split(root.__file__)[0]+'/'
        print 'root:', self.__path
            
        if context:
            if Application.__context.has_key(context):  
                self = Application.__context[context]
            else:
                Application.__context[context] = self
        else:
            pid = str(os.getpid())            
            if Application.__context.has_key(pid):
                self = Application.__context[pid]
            else:
                Application.__context[pid] = self
        
        print '>>>', self, type(self)
    
    def path(self):
        return self.__path
    
    def run(self):
        init = getattr(self, 'init')
        if init and callable(init):
            init()
        gtk.main()
        print '### pos-main ###' 
    
    #run = staticmethod(run)
    
    def quit(self):
        term = getattr(self, 'term')
        if term and callable(term):
            term()
        gtk.main_quit()
        
    #quit = staticmethod(quit)
    
