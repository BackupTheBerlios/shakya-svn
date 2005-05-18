class Object:
    def __init__(self):
        self.children = []
        self.text = ""
        self.attributes = None
        
    def add(self, child):
        self.children.append(child)

    def __repr__(self):
        return '%s: "%s" %s' % (self.name, self.text, zip(self.attributes.keys(), self.attributes.values()) )

class Property:
    def __init__(self, name, object):
        self.name = name
        self.object = object
        self.text = ""
    
    def set(self):
        obj = self.object
        property = None
        for p in gobject.list_properties(obj):
            if p.name == self.name:
                property = p
                break
        
        t = gobject.type_name(property)
        if t == 'GParamString':
            obj.set_property(self.name, self.text)
        elif t == 'GParamBoolean':
            if self.text == 'False' or self.text == '0':
                obj.set_property(self.name, False)
            else:
                obj.set_property(self.name, True)            
        else:
            print 'unknown property type'
        
        print 'set:', self.name, t, self.text
        
    
class Proxy:
    def __init__(self, widget):
        self._widget = widget
        self.text = ""
        
    def __getattr__(self, name):
        return getattr(self._widget, name)
    
    def widget(self):
        return self._widget
    
class TestHandler(handler.ContentHandler):
    def __init__(self):
        self.root = None
        self.list = [] 
        self.stack = [] # root object
    
    def startElement(self, tag, map):
        element = None
        if tag=='object':
            element = Proxy( eval( '%s()' % map['class'] ) )
            if len(self.stack) > 0:
                parent = self.stack[-1]
                if isinstance(parent, gtk.VBox):
                    parent.pack_start(element.widget())
                else:
                    parent.add(element.widget())
            else:
                self.root = element
        elif tag=='property':
            parent = self.stack[-1]
            element = Property(map['name'], parent)
        else:
            pass # unknown tag, ignore sub-context
        self.stack.append(element)        
        
    def characters(self, data):
        element = self.stack[-1]
        element.text += data

    def endElement(self, name):
        if name=='property':
            property = self.stack[-1]
            property.set()
            #element.parent.set_property(element.name, element.text)
        
        self.list.append(self.stack.pop())


class Loader:
    def __init__(self):
        pass
        
    def parse(self, filename):
        parser = sax.make_parser()
        handler = TestHandler()
        parser.setContentHandler(handler)
        parser.parse(filename)
        for each in handler.list:
            print each
        return handler.list[-1]




