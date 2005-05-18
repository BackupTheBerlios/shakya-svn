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

_cash = {}
_from_text = {}
_to_text = {}
_handler = {}


# Register functions:
def register_from_text(type_id, func):
    _from_text[type_id] = func

def register_to_text(type_id, func):
    _to_text[type_id] = func


# Query funtions
def get_from_text(type_id):
    return _from_text[type_id]

def get_to_text(type_id):
    return _to_text[type_id]



# Type discovering functions
def get_property_type(owner, name):
    for property in gobject.list_properties(owner):
        if property.name == name:
            return gobject.type_name(property)
    raise TypeError

def get_child_property_type(owner, name):
    parent = owner.get_property('parent')
    for property in gtk.container_class_list_child_properties(parent):
        if property.name == name:
            return gobject.type_name(property)
    raise TypeError


    
# GParamBoolean
def GParamBoolean_from_text(text):
    if text == 'True':
        return True
    elif text == 'False':
        return False
    else:
        raise TypeError
    
def GParamBoolean_to_text(value):
    if value is True:
        return 'True'
    else:
        return 'False'

    

# GParamString    
def GParamString_from_text(text):
    return text

def GParamString_to_text(value):
    if value is None:
        return ''
    else:
        return value



# GParamUInt    
def GParamUInt_from_text(text):
    return int(text)

def GParamUInt_to_text(value):
    return '%u' % value



# GParamInt    
def GParamInt_from_text(text):
    return int(text)

def GParamInt_to_text(value):
    return '%d' % value
    
    

# GParamFloat
def GParamFloat_from_text(text):
    return float(text)

def GParamFloat_to_text(value):
    return '%f' % value



# GParamDouble
def GParamDouble_from_text(text):
    return float(text)

def GParamDouble_to_text(value):
    return '%g' % value
    
    
    
# GParamObject
def GParamObject_from_text(text):
    if text == '':
        return None
    else:     
        return int(text)

def GParamObject_to_text(value):
    if value is None:
        return ''
    else:
        return '%d' % id(value)
    


# list of known supported properties
_properties = ['GParamBoolean', 
               'GParamString', 
               'GParamUInt', 
               'GParamInt', 
               'GParamFloat', 
               'GParamDouble', 
               'GParamObject']

for type_id in _properties:
    exec( '_from_text["%s"]=%s_from_text' % (type_id, type_id) )
    exec( '_to_text["%s"]=%s_to_text' % (type_id, type_id) )


