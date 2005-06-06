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

#shakya.ide import ShakyaIDE

import shakya.ide
from shakya.application import Application
from shakya.ide.mainwindow import MainWindow

class ShakyaIDE(Application): 
    def init(self):
        print 'ShakyaIDE:', __file__
        mainwindow = MainWindow(self)
        mainwindow.show()

    def term(self):
        print 'term'


print 'starting Shakya IDE...'
ide = ShakyaIDE(shakya.ide) #, context='shakya-ide')
ide.run()
