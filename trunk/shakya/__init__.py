print 'Loading Shakya module...'


import os
_basedir = os.path.split(__file__)[0]+'/'
print _basedir
del os 

def basedir():
    return _basedir


#import fw
#import ide


