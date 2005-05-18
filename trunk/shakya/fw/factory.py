import builtin_factories

#print builtin_factories.map.keys()
#print builtin_factories.map.values()

class _WidgetFactory:
    def __init__(self):        
        self._factories = builtin_factories.map
        #print self._factories.keys()
    
    def register(self, class_name, factory):
        self._factories[class_name] = factory    
    
    def build(self, class_name):
        factory = None
        
        try:
            factory = self._factories[class_name]
        except:
            print 'There is no factory for "%s"' % class_name
            raise
        
        return factory()

widgetFactory = _WidgetFactory()
