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
import handler


_infos = {}


class Info:
    """
    A property info. This object contains information of how
    a property of an GObject should be treated on the Property Browser
    """
    
    def __init__(self, name, tab, Handler=None, **opt):
        """
        name: the property name
        tab: the property context (tab number) on the Property Browser
        Handler: the property handler class 
        opt: optional handler parameters
        """        
        
        self.name = name
        self.tab = tab
        self.Handler = Handler
        self.opt = opt


    def __repr__(self):
        return 'Info %s: %d %s %s' % (self.name, self.tab, self.Handler, self.opt)



def register(klass, info):
    """
    Register a property info. One can extend the IDE with new property infos.
    This is useful when you have new properties on PyGTK or custom objects that
    you might want to add to the IDE.
    
    klass: a string with the GObject base class to associate with the 
           info (ex: 'GtkWidget')
    info: the info to register to that base class
    """
    
    if not _infos.has_key(klass):
        _infos[klass] = []

    if not info.Handler:
        info.Handler = handler.get_default_handler(klass, info.name)

    info.klass = klass
    
    _infos[klass].append(info)



def _get_property(name, lst):
    for p in lst:
        if p.name == name:
            lst.remove(p)
            return p
    


def fetch(obj):
    """
    Fetch properties info of an object. This is used in the Property Browser
    to get all the editable properties of that object.
    """
    
    result = []
    
    properties = list(gobject.list_properties(obj))
    for klass, infos in _infos.iteritems():
        if gobject.type_is_a(obj, klass):
            for info in infos:
                info.property = _get_property(info.name, properties)
                result.append(info)
    
    return result



__builtin = { 
    'GtkWidget': [
        Info('name', 0), 
        Info('sensitive', 1, inert=True, value=True), Info('visible', 1, inert=True, value=True),
        Info('can-focus', 1), Info('has-focus', 1),
        Info('can-default', 1), Info('receives-default', 1), Info('has-default', 1)
    ], 
    'GtkWindow': [
        Info('title', 0)
    ],
    'GtkMisc': [
        Info('xalign', 0, value=0.5, bottom=0, top=1, step=0.01, digits=2),
        Info('yalign', 0, value=0.5, bottom=0, top=1, step=0.01, digits=2)
    ],
    'GtkLabel': [
        Info('angle', 0, value=0, bottom=0, top=360, step=1, digits=0),
        Info('label', 0)
    ],
    'GtkEntry': [
        Info('text', 0)
    ]
}
print 'builtin infos:', __builtin

# register builtin infos
for klass, infos in __builtin.iteritems():
    for info in infos:
        register(klass, info)







