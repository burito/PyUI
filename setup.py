
from distutils.core import setup

setup(name="PyUI",
      version="0.96",
      description="Python User Interface Library",
      author="Sean Riley",
      author_email="sean@twistedmatrix.com",
      url="http://pyui.sf.net",
      packages=['pyui','pyui.renderers','pyui.themes'],
      data_files=[('Lib/site-packages/pyui/images', ['pyui/images/cursor_drag.png',
                              'pyui/images/cursor_hand.png',
                              'pyui/images/cursor_pointer.png',
                              'pyui/images/cursor_resize.png'])]
      )


