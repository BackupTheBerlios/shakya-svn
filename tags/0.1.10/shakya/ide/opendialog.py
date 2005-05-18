import gtk

class OpenDialog:
    def __init__(self, parent, filters=None):
        dialog = gtk.FileChooserDialog('Open file', parent, 
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
        for name, pattern in filters:
            filter = gtk.FileFilter()
            filter.set_name(name)
            filter.add_pattern(pattern)
            dialog.add_filter(filter)
        
        dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        
        self._dialog = dialog
        
    
  
    def __getattr__(self, name):
        return getattr(self._dialog, name)
