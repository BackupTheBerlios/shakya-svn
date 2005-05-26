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
import xml.sax as sax
import xml.sax.handler as handler
import gobject
import gtk
import property


class Property:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.text = ""

    def set_value(self):
        value = self.to_python(self.text)
        self.owner.set_property(self.name, value)

    def set(self):        
        type_id = property.get_property_type(self.owner, self.name)
        self.to_python = property.get_from_text(type_id)
        self.set_value()
        #print '%s:%s = %s' %(self.name, type_id, self.text)


class ChildProperty(Property):
#    def __init__(self, name, object):
#        Property.__init__(self, name, object)
    
    def set_value(self):
        value = self.to_python(self.text)
        parent = self.owner.get_property('parent')
        parent.child_set_property(self.owner.instance(), self.name, value)

    def set(self):        
        type_id = property.get_child_property_type(self.owner, self.name)
        self.to_python = property.get_from_text(type_id)
        self.set_value()
        #print '%s:%s = %s' %(self.name, type_id, self.text)


class Proxy:
    def __init__(self, instance):
        self._instance = instance        
        self.text = ""
        
    def __getattr__(self, name):
        return getattr(self._instance, name)
    
    def instance(self):
        return self._instance

    def add_group(self, grp):
        groups = self._instance.get_data('shakya:action-groups')
        if groups is None:
            groups = {}
            self._instance.set_data('shakya:action-groups', groups )        
        groups [grp.get_name()] = grp        


class ActionGroup(Proxy):
    def __init__(self, name):
        Proxy.__init__(self, gtk.ActionGroup(name))
        self.name = name
    
    def add_action(self, action):
        self._instance.add_action(action)
        #print '***', action.get_property('action-group')        


def _add_action(act, obj):
    actions = obj.get_data('shakya:actions')
    if actions is None:
        actions = {}
        obj.set_data('shakya:actions', actions)        
    actions[act.get_name()] = act


def _set_parent(child, parent):
    if isinstance(parent, gtk.Box):
        parent.pack_start(child)
        
    elif isinstance(parent, gtk.MenuShell):
        parent.append(child)
        
    elif isinstance(parent, gtk.MenuItem):
        parent.set_submenu(child)
        
    else:
        parent.add(child)


def _create_object(type_id, attrs, root):    
    if type_id == 'GtkMenuItem':
        action_name = attrs.pop('action', None)        
        if action_name:
            action_map = root.get_data('shakya:actions')
            print root, action_map
            action = action_map[str(action_name)]
            item = action.create_menu_item()
            item.set_data('shakya:action', action)
            
        else :
            label = attrs.pop('label', None)
            item = gtk.MenuItem(label=label)
            
        return item
        
    elif type_id == 'GtkToolButton':
        action_name = attrs.pop('action', None)        
        if action_name:
            action_map = root.get_data('shakya:actions')
            print root, action_map
            action = action_map[str(action_name)]
            item = action.create_tool_item()
            item.set_data('shakya:action', action)
            
        else :
            label = attrs.pop('label', None)
            item = gtk.ToolButton()
            
        return item       
    else:
        return gobject.new(type_id)


def _create_action(attrs):
    type_ = attrs.pop('type', None)
    name = str(attrs.pop('name'))
    label = attrs.pop('label')
    tooltip = attrs.pop('tooltip')
    stock_id = str(attrs.pop('stock_id'))
    value = attrs.pop('value', None)
    
    if type_ is None:
        return gtk.Action(name, label, tooltip, stock_id)
        
    elif type_ == 'toggle':
        return gtk.ToggleAction(name, label, tooltip, stock_id)
        
    elif type_ == 'radio':
        return gtk.RadioAction(name, label, tooltip, stock_id, int(value))    
    

class XMLWidgetHandler(handler.ContentHandler):
    def __init__(self):
        self.root = None
        self.list = [] 
        self.stack = []
    
    def startElement(self, tag, attrs):
        print '<%s>' % tag
        attrs = dict(attrs)
        element = None
        if tag == 'object' or tag == 'window':
            print attrs.items()
            type_id = str(attrs.pop('class'))
            element = Proxy(_create_object(type_id, attrs, self.root))
            if len(self.stack) > 0:
                parent = self.stack[-1]
                _set_parent(element.instance(), parent.instance())
            else:
                self.root = element
            
        elif tag == 'action-group':
            parent = self.stack[-1]
            element = ActionGroup(attrs['name'])
            self.root.add_group(element.instance())            
            #parent.add_action(element)
            
        elif tag == 'action':
            parent = self.stack[-1]
            element = Proxy(_create_action(attrs))
            parent.add_action(element.instance())
            _add_action(element.instance(), self.root.instance())
            
        elif tag == 'property':
            parent = self.stack[-1]
            element = Property(attrs['name'], parent)        
            
        elif tag=='child-property':
            parent = self.stack[-1]
            element = ChildProperty(attrs['name'], parent)             
            
        else:
            pass # unknown tag, ignore sub-context
            
        self.stack.append(element)        
        
    def characters(self, data):
        element = self.stack[-1]
        element.text += data

    def endElement(self, tag):
        element = self.stack.pop()
        if tag == 'property' or tag == 'child-property':
            property = element
            property.set()
            #element.parent.set_property(element.name, element.text)
            
        else:
            self.list.append(element.instance())


def load_widget(filename):
    parser = sax.make_parser()
    handler = XMLWidgetHandler()
    parser.setContentHandler(handler)
    parser.parse(filename)
    #for each in handler.list:
    #    print each
    return handler.root.instance() #handler.list[-1]

################################################################################

class UILoader:
    def __init__(self):
        self._doc = None
        self.dic = {}
        self.grp_list = []
        self.act_list = []    
    
    def load(self, filename):
        doc = self._doc        
        doc = dom.parse(filename)
        doc.loader = self
        
        doc_node = doc.getElementsByTagName('shakya-ui')[0]        
        action_node, data_node, widget_node = _parse_sections(doc_node)
        
        _read_actions(action_node)        
        #_read_data(data_node)
        #_read_widgets(widget_node)
        
        wnode = _get_first_child(widget_node, 'object')        
        obj = _build_object(wnode)
        
        # set the action list
        obj.set_data('shakya:actions', self.act_list)
        obj.set_data('shakya:action-groups', self.grp_list)
        
        return obj


def _parse_sections(node):
    anode = _get_first_child(node, 'action-section')
    dnode = _get_first_child(node, 'data-section')
    wnode = _get_first_child(node, 'widget-section')    
    return anode, dnode, wnode


def _get_first_child(node, tag):
    for child in node.childNodes:
        if child.nodeType is dom.Node.ELEMENT_NODE and child.tagName == tag:
            #print '<s:%s>' % tag
            return child
    return None


def _top_node(node):
    while node.parentNode:
        node = node.parentNode
    return node
    

def _text(node):    
    text = ''
    for child in node.childNodes:
        if child.nodeType is child.TEXT_NODE:
            text += child.data
    return text


def _elements(node, tag=None):
    if node and node.childNodes:
        if not tag:
            return [child for child in node.childNodes 
                    if child.nodeType is dom.Node.ELEMENT_NODE]
        else:
            return [child for child in node.childNodes 
                    if child.nodeType is dom.Node.ELEMENT_NODE and child.tagName == tag]
    else:
        return []

def _children(node):   
    return _elements(node, 'object')

def _properties(node):
    return _elements(node, 'property')


def _add_child(parent, child):
    if parent is None:
        return
        
    elif isinstance(parent, gtk.Box):
        parent.pack_start(child)
        
    elif isinstance(parent, gtk.MenuShell):
        parent.append(child)
        
    elif isinstance(parent, gtk.MenuItem) and isinstance(child, gtk.MenuShell):
        parent.set_submenu(child)
        
    else:
        parent.add(child)


def _conly_properties(node, owner_type):     
    att = {}
    # TODO: this could be optimized
    # just a dummy object to get the property type
    dummy = gobject.new(owner_type)
    for prop in _elements(node, 'property'):
        if prop.getAttribute('construct-only') == 'True': 
            name = prop.getAttribute('name')
            type_name = property.get_property_type(dummy, name)
            from_text = property._from_text[type_name]
            value = from_text(_text(prop))
            att[name] = value
    return att
    

def _create_new_object(type_name, pnode):
    att = {}
    obj = None
    
    print 'new:', type_name
    isAction = gobject.type_is_a(type_name, 'GtkAction')
    isActionGroup = gobject.type_is_a(type_name, 'GtkActionGroup')
    isMenuItem = gobject.type_is_a(type_name, 'GtkMenuItem')
    isToolItem = gobject.type_is_a(type_name, 'GtkToolItem')

    if isAction or isActionGroup:
        att = _conly_properties(pnode, type_name) 
        
    elif isMenuItem or isToolItem:
        _id = node = pnode.parentNode.getAttribute('action')
        if not _id == '':
            dic = _top_node(pnode).loader.dic
            act = dic[int(_id)]
            
            if isMenuItem:
                obj = act.create_menu_item()
            elif isToolItem:
                obj = act.create_tool_item()
            
            obj.set_data('shakya:action', act)
    
    if not obj:  
        obj = gobject.new(type_name, **att)
        if gobject.type_is_a(obj, gtk.Widget):
            obj.hide()
    
    return obj


def _set_property(owner, prop):
    if prop.getAttribute('construct-only') == 'True':
        return
    
    name = prop.getAttribute('name')
    type_name = property.get_property_type(owner, name)
    text = _text(prop)

    from_text = property._from_text[type_name]
    value = from_text(text)
    if type_name == 'GParamObject':
        dic = _top_node(prop).loader.dic        
        if dic.has_key(value) and not name == 'parent':
            owner.set_property(name, dic[value])
        else:
            print 'Ignoring', name, value
    else:
        owner.set_property(name, value)


def _set_child_property(parent, owner, prop):
    name = prop.getAttribute('name')
    type_name = property.get_child_property_type(owner, name)
    from_text = property._from_text[type_name]
    value = from_text(_text(prop))
    if type_name == 'GParamObject':
        dic = _top_node(prop).loader.dic
        if dic.has_key(value):
            parent.child_set_property(owner, name, dic[value])
        else:
            print 'Ignoring', name, value
    else:
        parent.child_set_property(owner, name, value)

def _build_object(node, parent=None):
    pnode = _get_first_child(node, 'properties')
    cpnode = _get_first_child(node, 'child-properties')
    cnode = _get_first_child(node, 'children')
    #print pnode, cpnode, cnode    

    _id = int(node.getAttribute('id'))
    type_name = str(node.getAttribute('class'))    
    obj = _create_new_object(type_name, pnode); print obj
    _add_child(parent, obj)

    # store a reference on the dictionary
    dic = _top_node(node).loader.dic
    dic[_id] = obj

    # setup the properties
    for prop in _properties(pnode):
        _set_property(obj, prop)

    # setup the child-properties
    if parent and gobject.type_is_a(parent, 'GtkContainer'):
        for prop in _properties(cpnode):
            _set_child_property(parent, obj, prop)

    # recursively create children
    if gobject.type_is_a(obj, 'GtkContainer'):
        for child in _children(cnode):
            _build_object(child, obj)
    
    # create submenus
    if gobject.type_is_a(obj, 'GtkMenuItem'):
        submenu = _get_first_child(node, 'submenu')
        #print '*** menuitem', submenu
        if submenu:
            child = _get_first_child(submenu, 'object')
            if child:
                _build_object(child, obj)
    
    return obj


def _read_actions(node):
    loader = _top_node(node).loader

    gnode = _get_first_child(node, 'action-groups')
    anode = _get_first_child(node, 'actions')
    
    for grp in _elements(gnode, 'object'):
        loader.grp_list.append(_build_object(grp)) 
    print loader.grp_list
    
    for act in _elements(anode, 'object'):
        loader.act_list.append(_build_object(act))
    print loader.act_list


def _read_widgets(node):
    loader = _top_node(node).loader

    wnode = _get_first_child(node, 'object')
    
#    for obj in _elements(gnode, 'object'):
#        loader.grp_list.append(_build_object(grp)) 
    print loader.grp_list


    
def load_ui(filename):
    print 'Loading: %s...' % filename    
    loader = UILoader()
    obj = loader.load(filename)
    print obj    
    if gobject.type_is_a(obj, 'GtkWindow'):
        w, h = obj.get_default_size()
        obj.resize(w, h)
    
    return obj


def get_glade_widgets(filename):
    doc = dom.parse(filename)
    wl = [(str(each.getAttribute('id')), str(each.getAttribute('class'))) for each in _elements(doc.documentElement)]
    return wl






