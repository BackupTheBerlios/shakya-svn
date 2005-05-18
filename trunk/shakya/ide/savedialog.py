import gtk

class SaveDialog:
    def __init__(self, parent):        
        dialog = gtk.FileChooserDialog('Save file', parent, 
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
        
        filters = [("User Interface files (*.ui)", "*.ui"),
                    ("Python modules (*.py)", "*.py"),
                    ("All files", "*")]
        
        for name, pattern in filters:
            filter = gtk.FileFilter()
            filter.set_name(name)
            filter.add_pattern(pattern)
            dialog.add_filter(filter)
        
        dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        
        self._dialog = dialog
        
    
    def __getattr__(self, name):
        return getattr(self._dialog, name)
