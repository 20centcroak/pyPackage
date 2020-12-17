import PyInstaller.__main__
import os
from pyPackage import Options
import distutils.file_util as fileutil
import distutils.dir_util as dirutil
from distutils.dist import DistutilsError
import logging
import re


class Package:

    def __init__(self, options: Options, data=None, example_folder=None, doc_folder=None):
        command = []
        version = options.version if options.version else 0.0
        modulename, _ = os.path.splitext(options.package)
        name = os.path.basename(modulename) 
        root_path = '/dist/{}_{}'.format(name,version)

        if options.name:
            command.append('--name={}'.format(options.name))
            name = options.name
            root_path = '/dist/{}_{}'.format(name,version)
        if options.onefile:
            command.append('--onefile')
        if options.no_confirm:
            command.append('--noconfirm')
        if options.console:
            command.append('--console')
        else:
            command.append('--noconsole')
        if options.icon:
            command.append('--icon={}'.format(options.icon))
        if options.distpath:
            root_path = '{}/{}_{}'.format(options.distpath, name, version)
            command.append('--distpath={}'.format(root_path))
        if options.workpath:
            command.append('--workpath={}'.format(options.workpath))
        if options.clean:
            command.append('--clean')
        if options.specpath:
            command.append('--specpath={}'.format(options.specpath))
        if options.paths:
            for path in options.paths:
                command.append('--paths={}'.format(path))
        if options.hiddenimports:
            for module in options.hiddenimports:
                command.append('--hidden-import={}'.format(module))
        if options.additionalhooks:
            for path in options.additionalhooks:
                command.append('--additional-hooks-dir={}'.format(path))
        if options.runtimehooks:
            for path in options.runtimehooks:
                command.append('--runtime-hook={}'.format(path))
        if options.excludemodules:
            for module in options.excludemodules:
                command.append('--exclude-module={}'.format(module))
        if options.binaries:
            for src in options.binaries:
                command.append('--add-binary={}{}{}'.format(src,
                                                            os.path.pathsep, options.binaries[src]))
   
        command.append(options.package)

        self._package(command)

        if data:
            self._copyFilesAndFolders(data, root_path, name)

        if options.bat:
            self._createbat(root_path, name, options.bat)

        if options.sh:
            self._createsh(root_path, name, options.sh)

    def _package(self, command):
        PyInstaller.__main__.run(command)

    def _createbat(self, path, name, parameters):
        file = os.path.join(path, name+'.bat')
        path = parameters['path'] if 'path' in parameters else name
        with open(file, 'w') as f:
            f.write(os.path.join(path, name+'.exe '))
            for key, value in parameters['options'].items():
                f.write('-{} {} '.format(key, value))
            f.write('\nPAUSE')

    def _createsh(self, path, name, parameters):
        file = os.path.join(path, name+'.sh')
        target = '{0}/{1}/{1} '.format(parameters['path'], name)
        with open(file, 'w') as f:
            f.write(target)            
            for key, value in parameters['options'].items():
                f.write('-{} {} '.format(key, value))

    def _copyFilesAndFolders(self, data, root_path, name):
        for dataobj in data:
            src = dataobj['src']
            dest = dataobj['dst'] if 'dst' in dataobj else ''
            root_level = dataobj['root_level']
            dest = os.path.join(root_path, dest) if root_level else os.path.join(root_path, name, dest)
            self._copyFolder(src, dest) if os.path.isdir(src) else self._copyFile(src, dest, dataobj)

    def _copyFolder(self, src, dest):
        if not src:
            return
        try:
            dirutil.copy_tree(src, dest)
            return dest
        except DistutilsError:
            logging.warning("can't copy {} from {}".format(dest, src))

    def _copyFile(self, src, dest, dataobj):
        if not src:
            return
        try:
            target_file = os.path.join(dest, dataobj['rename']) if 'rename' in dataobj else os.path.join(dest, os.path.basename(src))
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            fileutil.copy_file(src, target_file)
            return target_file
        except DistutilsError:
            logging.warning("can't copy {} from {}".format(dest, src))
