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

print 'starting Shakya IDE...'

import shakya.fw as fw
from mainwindow import MainWindow

#modules = [('propertybrowser', 'PropertyBrowser'),
#           ('mainwindow', 'MainWindow')]
#for entry in modules:
#    code = 'from %s import %s' % entry
#    exec code    
#del modules, entry

def run():
    mainwindow = MainWindow()
    mainwindow.init()
    mainwindow.show()
    fw.Application.run()
