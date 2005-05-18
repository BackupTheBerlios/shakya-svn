import gtk

map = {}
_types = ['GtkWindow', 'GtkVBox', 'GtkToolbar', 'GtkToolbutton', 'GtkTreeView']

def _convert(class_name):
    if class_name.startswith('Gtk'):
        return 'gtk.' + class_name[3:]
    else:
        raise TypeError

for each in _types:
    exec('def factory_%s(): return %s' % (each, _convert(each)))
    exec('map["%s"] = factory_%s' % (each, each))


