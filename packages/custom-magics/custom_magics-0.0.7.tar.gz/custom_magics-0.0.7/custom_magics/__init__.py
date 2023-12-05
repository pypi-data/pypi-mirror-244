from .custom_magics import MyMagics
__version__ = '0.0.1'
ip = get_ipython()
ip.register_magics(MyMagics)
def load_ipython_extension(ipython):
    ipython.register_magics(MyMagics)