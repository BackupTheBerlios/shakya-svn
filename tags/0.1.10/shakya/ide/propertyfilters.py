import gobject, gtk


class FilterInfo:
    def __init__(self, name, tab):
        self.name = name
        self.tab = tab
    
    def __repr__(self):
        return '%s, %d' % (self.name, self.tab)


class Filter:
    def __init__(self, klass, infos):
        self.klass = klass
        self.infos = infos

    def __repr__(self):
        return '%s: %s' % (self.klass, self.infos)


builtin_filters = [ 
    Filter('GtkWidget', [
        FilterInfo('name', 0), FilterInfo('sensitive', 0), FilterInfo('visible', 0)
    ]),
    Filter('GtkWindow', [
        FilterInfo('title', 0)
    ]),
    Filter('GtkEntry', [
        FilterInfo('text', 0)
    ])
]

print builtin_filters

#class PropertyFilter:
#    def __init__(self, base, name):
#        self._base = base
#        self._name = name
    
    
