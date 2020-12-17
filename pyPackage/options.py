from enum import Enum
from pyBaseApp import Settings

class Options(Settings):
    """https://pyinstaller.readthedocs.io/en/stable/usage.html"""

    loglevels = Enum('loglevel', 'TRACE DEBUG INFO WARN ERROR CRITICAL')

    def __init__(self, settings):

        self.name = None
        self.onefile=False
        self.console=True
        self.binaries = dict()
        self.icon = None
        self.distpath = None
        self.workpath = None
        self.specpath = 'pyinstaller'
        self.paths = []
        self.clean = True
        self.loglevel = self.loglevels.DEBUG.name
        self.hiddenimports = []
        self.additionalhooks = []
        self.runtimehooks = []
        self.excludemodules = []
        self.package = None
        self.no_confirm = True
        self.version = None
        self.sh = None
        self.bat = None


        self.setProperties(settings)

        if not self.package:
            raise ValueError('no package provided to build exe file')

    def addBinary(self, src, dst):
        self.binaries[src] = dst

    def addPath(self, path):
        self.paths.append(path)
