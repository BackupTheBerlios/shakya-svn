from distutils.core import setup

setup(name="shakya",
      version="0.1.10",
      description="Shakya: PyGTK Framework and IDE",
      long_description='Shakya is a Free Software (GPL) framework for easy and quickly building powerfull applications with Python and PyGTK. Besides, there is also an IDE, made with this same framework, thus users can graphically desing Shakya/PyGTK applications.',      
      url='http://shakya.berlios.de',
      license='GPL',
      author='Eric Jardim',
      author_email='ericjardim@gmail.com',
      scripts=['shakya_ide.py'],
      packages=['shakya', 'shakya.fw', 'shakya.ide', 'shakya.ide.property'],
      data_files=[('', ['COPYING', 'AUTHORS', 'CHANGELOG']), 
                  ('shakya/ide', ['shakya/ide/mainwindow.ui'])],
     )
