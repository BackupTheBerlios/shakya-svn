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
import loader
#import gtk.glade as glade


def _parse_signal_handler(handler):
    (widget, signal) = handler.split('__')
    signal = signal.replace('_', '-')
    return (widget, signal)

def hi(widget, data=None):
    print widget.get_name(),': ', widget 


class Widget:
    def __init__(self, ltype=None):
        self.__actions = {}
        
        if ltype:
            self._widget = loader.load_widget(self.uifile)
        else:
            self._widget = loader.load_ui(self.uifile)
        self._find_children()
        self._connect_signals()
        self._widget.connect('destroy', self._byebye)
        for child in self._widgets.values():
            hi(child)

    def _find_children(self):
        stack = self.get_children()
        map = { self.get_name(): self._widget }
        while len(stack) > 0:
            child = stack.pop()
            map[child.get_name()] = child
            if isinstance(child, gtk.Container):
                stack += child.get_children()
                if isinstance(child, gtk.MenuItem):
                    submenu = child.get_submenu()
                    if submenu:
                        print 'submenu', submenu
                        stack += submenu.get_children()
        self._widgets = map
            
        #action_map = self._widget.get_data('shakya:actions')
        #if action_map:
        #    for key, value in action_map.iteritems():
        #        self._widgets[key] = value
        
        actions = self._widget.get_data('shakya:actions')
        if actions:
            for act in actions:
                self._widgets[act.get_name()] = act
        
    
    def _connect_signals(self):
        print self
        for attrib in dir(self):
            print attrib
            connect = None                
            if attrib.startswith('on_'):
                suffix = attrib[3:]
                connect = self._widget.connect
            elif attrib.startswith('after_'):
                suffix = attrib[6:]
                connect = self._widget.connect_after                
            if connect:
                (widget, signal) = _parse_signal_handler(suffix)
                print widget+':', signal
                try:
                    sender = self._widgets[widget]
                    callback = getattr(self, attrib)
                    print sender, callback
                    sender.connect(signal, callback)
                except TypeError:
                    print 'Error: unknown signal "'+signal+'" for widget "'+widget+'"'
                except KeyError:
                    print 'Error: could not bind signal "'+signal+'" to widget "'+widget+'"'

    def child(self, name=None):
        if name is None:
            return self._widgets
        else:
            return self._widgets[name]

    def __getitem__(self, name):
        return self._widgets[name]

    def __getattr__(self, name):
        if hasattr(self._widget, name):
            return getattr(self._widget, name)    
    
    def _byebye(self, window):
        # do some finalization here
        print 'closing: %s' % window.get_name()
    
    def get_width(self):
        #window = self._widget.get_parent_window()
        #return window.get_geometry()[2]
        return self._widget.get_size()[0]
    
    def get_height(self):
        #window = self._widget.get_parent_window()
        #return window.get_geometry()[3]
        return self._widget.get_size()[1]
    
    def instance(self):
        return self._widget
    
    #def __setattr__(self, name, value):
    #    setattr(self._widget, name, value)

