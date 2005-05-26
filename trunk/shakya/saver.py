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

import xml.dom.minidom as dom
import gobject
import gtk
import property


def save_ui(filename, root_object):
    print 'saving "%s" on %s:' % (root_object, filename)
    
    saver = UISaver(root_object)
    saver.save(filename)
    

class UISaver:
    def __init__(self, root_object):
        self._doc = None
        self._root_object = root_object

    def save(self, filename):
        # create the dom.Document 
        doc = dom.Document()
        doc_node = doc.createElement('shakya-ui')
        doc.appendChild(doc_node)
        self._doc = doc
    
        # write the action section
        gnode, anode = self._write_actions(self._root_object)
        section_node = doc.createElement('action-section')
        section_node.appendChild(gnode)
        section_node.appendChild(anode)
        doc_node.appendChild(section_node)    
    
        # write the widget section
        node = self._object_to_xml(self._root_object)
        section_node = doc.createElement('widget-section')
        section_node.appendChild(node)
        doc_node.appendChild(section_node)
        
        # save the dom.Document to the file
        #print doc.toprettyxml(indent='  ')
        outfile = open(filename, 'w')
        outfile.write(doc.toxml())
        #outfile.write(doc.toprettyxml(indent='  '))
        outfile.close()        

    def _filter_children(self, children):
        return children

    def _object_to_xml(self, obj, parent_node=None):
        doc = self._doc
        
        # create the object node
        node = doc.createElement('object')
        node.setAttribute('class', gobject.type_name(obj))
        node.setAttribute('id', '%d'%id(obj))
        if isinstance(obj, gtk.MenuItem) or isinstance(obj, gtk.ToolItem):
            act = obj.get_data('shakya:action')
            if act:
                node.setAttribute('action', '%d' % id(act))
        
        # write the object properties
        prop_node = doc.createElement('properties')
        self._write_properties(prop_node, obj)
        node.appendChild(prop_node) 
        
        # write the widget child-properties        
        if gobject.type_is_a(obj, 'GtkWidget'):
            parent = obj.get_parent()
            if parent and gobject.type_is_a(parent, 'GtkContainer'):
                childprop_node = doc.createElement('child-properties')
                self._write_child_properties(childprop_node, obj)
                node.appendChild(childprop_node) 
        
        # write container widget children     
        if isinstance(obj, gtk.Container):
            act = None
            
            if isinstance(obj, gtk.MenuItem) or isinstance(obj, gtk.ToolItem):
                act = obj.get_data('shakya:action')
            
            if not act:
                children_node = doc.createElement('children')
                for child in self._filter_children(obj.get_children()):
                    child_node = self._object_to_xml(child, children_node)
                node.appendChild(children_node)
        
        # write menuitem submenus        
        if isinstance(obj, gtk.MenuItem):
            submenu_node = doc.createElement('submenu')
            submenu = obj.get_submenu()
            if submenu:
                menu_node = self._object_to_xml(submenu, submenu_node)
            node.appendChild(submenu_node)
        
        # link child node with parent
        if parent_node:
            parent_node.appendChild(node)
        
        return node
    
    
    def _write_actions(self, obj):
        doc = self._doc
        
        groups = obj.get_data('shakya:action-groups')
        actions = obj.get_data('shakya:actions')
    
        gnode = doc.createElement('action-groups')
        anode = doc.createElement('actions')
    
        if groups:
            for grp in groups.values():
                node = self._object_to_xml(grp)
                gnode.appendChild(node)
    
        if actions:
            for act in actions.values():
                node = self._object_to_xml(act)
                anode.appendChild(node)  
        
        return gnode, anode

    def _filter_properties(self, properties):
        res = []
        for prop in properties:
            type_name = gobject.type_name(prop)
            if property._to_text.has_key(type_name):
                if (prop.flags & gobject.PARAM_READABLE) and \
                   (prop.flags & gobject.PARAM_WRITABLE):
                       res.append(prop)
        return res

    def _write_properties(self, owner_node, owner):
        doc = self._doc
        
        # TODO: we need a smart property fetcher here
        properties = gobject.list_properties(owner)
        
        for prop in self._filter_properties(properties):
            node = self._property_to_xml(owner, prop, 'normal')
            owner_node.appendChild(node)

    def _write_child_properties(self, owner_node, owner):
        doc = self._doc
        
        # TODO: we need a smart property fetcher here
        parent = owner.get_parent()
        properties = gtk.container_class_list_child_properties(parent)
        
        for prop in self._filter_properties(properties):
            node = self._property_to_xml(owner, prop, 'child')
            owner_node.appendChild(node)

    def _property_to_xml(self, owner, prop, ptype):
        doc = self._doc
        
        node = doc.createElement('property')
        node.setAttribute('name', prop.name)
        
        type_name = gobject.type_name(prop)
        to_text = property._to_text[type_name]
        
        if ptype == 'normal':
            value = owner.get_property(prop.name)
        elif ptype == 'child':
            parent = owner.get_parent()
            value = parent.child_get_property(owner, prop.name)
        else:
            raise TypeError    
        
        if gobject.type_name(prop.value_type) == 'GtkActionGroup':
            print '***', value
        
        #print '%s: %s' % (prop.name, type_name)
        text = doc.createTextNode(to_text(value))
        node.appendChild(text)
        if (prop.flags & gobject.PARAM_CONSTRUCT_ONLY):    
            node.setAttribute('construct-only', 'True')
        
        return node
        
        #if not (prop.flags & gobject.PARAM_CONSTRUCT_ONLY):    
        #    text = doc.createTextNode(to_text(value))
        #    node.appendChild(text)
        #    return node
        #else:
        #    return None
    

