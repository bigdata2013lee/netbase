#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

from products.netUtils.xutils import importClass, zenPath
import sys
import os
import exceptions
import imp
from twisted.spread import pb
import logging
log = logging.getLogger('zen.Plugins')

class PluginImportError(exceptions.ImportError):
    """
    Capture extra data from plugin exceptions
    """

    def __init__(self, plugin='', traceback='' ):
        """
        Initializer

        @param plugin: plugin name
        @type plugin: string
        @param traceback: traceback from an exception
        @type traceback: traceback object
        """
        self.plugin = plugin
        self.traceback = traceback
        # The following is needed for zendisc
        self.args = traceback

class PluginLoader(pb.Copyable, pb.RemoteCopy):
    """
    Class to load plugins
    """

    def __init__(self, package, modPath, lastModName, importer):
        """
        package - '/'-separated absolute path to the root of the plugins
                  modules
        modPath - '.'-spearated module path.  for core plugins, it is rooted
                  at the package.  for zenpack plugins, it starts with
                  'ZenPacks'
        lastModName - name of the last module in modPath that is not part of
                  of the plugin name
        importer - object with an importPlugin method used to import the
                   plugin. the implementation of the import method differs 
                   between core and zenpack plugins
        """
        self.package = package
        self.modPath = modPath
        self.pluginName = modPath.split(lastModName + '.')[-1]
        self.importer = importer
                    
    def create(self):
        """
        Load and compile the code contained in the given plugin
        """
        try:
            try:
                # Modify sys.path (some plugins depend on this to import other
                # modules from the plugins root)
                sys.path.insert(0, self.package)
                pluginClass = self.importer.importPlugin(self.package, 
                                                         self.modPath)
                return pluginClass()
            except (SystemExit, KeyboardInterrupt):
                raise
            except:
                import traceback
                log.debug(traceback.format_exc())
                raise PluginImportError(
                    plugin=self.modPath, traceback=traceback.format_exc() )
        finally:
            try:
                sys.path.remove(self.package)
            except ValueError:
                # It's already been removed
                pass
                
pb.setUnjellyableForClass(PluginLoader, PluginLoader)

def _coreModPaths(walker, package):
    "generates modPath strings for the modules in a core directory"
    for absolutePath, dirname, filenames in walker.walk(package):
        if absolutePath == package:
            modPathBase = []
        elif absolutePath.startswith(package):
            modPathBase = absolutePath[len(package)+1:].split(os.path.sep)
        else:
            log.debug('absolutePath必须以包名开头: '
                      'absolutePath=%s, package=%s', absolutePath, package)
            continue
        for filename in filenames:
            if filename.endswith(".pyc") \
                    and filename[0] not in ('.', "_") \
                    and '#' not in filename \
                    and filename not in ('CollectorPlugin.pyc', 'DataMaps.pyc'):
                yield '.'.join(modPathBase + [filename[:-4]])
                
class OsWalker(object):
    
    def walk(self, package):
        return os.walk(package)
    
class CoreImporter(pb.Copyable, pb.RemoteCopy):
    
    def importPlugin(self, package, modPath):
        # Load the plugins package using its path as the name to 
        # avoid conflicts. slashes in the name are OK when using
        # the imp module.
        plugin_pkg = imp.find_module('.', [package])
        imp.load_module(package, *plugin_pkg)
        # Import the module, using the plugins package
        #
        # Equivalent to, for example: 
        #   from mypackage.zenoss.snmp import DeviceMap
        #
        clsname = modPath.split('.')[-1]
        mod = __import__(package + '.' + modPath, 
                         globals(),
                         locals(),
                         [clsname])
        # get the class
        return getattr(mod, clsname)
        
pb.setUnjellyableForClass(CoreImporter, CoreImporter)

class PackImporter(pb.Copyable, pb.RemoteCopy):
    
    def importPlugin(self, package, modPath):
        # ZenPack plugins are specified absolutely; we can import
        # them using the old method
        return importClass(modPath)
        
pb.setUnjellyableForClass(PackImporter, PackImporter)

class BaseLoaderFactory(object):
    
    def __init__(self, walker):
        self.walker = walker
    
    def genLoaders(self, package, lastModName):
        for coreModPath in _coreModPaths(self.walker, package):
            yield self._createLoader(package, coreModPath, lastModName)
            
class CoreLoaderFactory(BaseLoaderFactory):
    
    def _createLoader(self, package, coreModPath, lastModName):
        return PluginLoader(package, coreModPath, lastModName, CoreImporter())
        
class PackLoaderFactory(BaseLoaderFactory):
    
    def __init__(self, walker, modPathPrefix):
        BaseLoaderFactory.__init__(self, walker)
        self.modPathPrefix = modPathPrefix
        
    def _createLoader(self, package, coreModPath, lastModName):
        packModPath = '%s.%s' % (self.modPathPrefix, coreModPath)
        return PluginLoader(package, packModPath, lastModName, PackImporter())
        
class PluginManager(object):
    """
    Manages plugin modules.  Finds plugins and returns PluginLoader instances.
    Keeps a cache of previously loaded plugins.
    """
    
    def __init__(self, lastModName, packPath, productsPaths):
        """
        Adds PluginLoaders for plugins in productsPaths to the pluginLoaders
        dictionary.
        
        lastModName - the directory name where the plugins are found.  this name
                  is appended to the following paths
        packPath - path to the directory that holds the plugin modules inside
                   a zenpack. this path is relative to the zenpack root
        productsPaths - list of paths to directories that hold plugin
                   modules. these paths are relative to $ZENHOME/Products
        
        a 'path', as used here, is a tuple of directory names
        """
        self.pluginLoaders = {} # PluginLoaders by module path
        self.loadedZenpacks = [] # zenpacks that have been processed
        self.lastModName = lastModName
        self.packPath = packPath
        for path in productsPaths:
            package = zenPath(*('Products',) + path + (lastModName,))
            self._addPluginLoaders(CoreLoaderFactory(OsWalker()), package)
                          
    def getPluginLoader(self, packs, modPath):
        """
        Get the PluginLoader for a specific plugin.
        
        packs - list of installed zenpacks (ZenPack instances)
        modPath - the module path of the plugin
        """
        if modPath not in self.pluginLoaders:
            self.getPluginLoaders(packs)
        if modPath in self.pluginLoaders:
            return self.pluginLoaders[modPath]
                                   
    def getPluginLoaders(self, packs):
        """
        Add the PluginLoaders for the packs to the pluginLoaders dictionary.
        Return the values of that dictionary.
        
        packs - list of installed zenpacks (ZenPack instances)
        """
        try:
            for pack in packs:
                if pack.moduleName() not in self.loadedZenpacks:
                    self.loadedZenpacks.append(pack.moduleName())
                    modPathPrefix = '.'.join((pack.moduleName(),) + 
                            self.packPath + (self.lastModName,))
                    factory = PackLoaderFactory(OsWalker(), modPathPrefix)
                    package = pack.path(*self.packPath + (self.lastModName,))
                    self._addPluginLoaders(factory, package)
        except:
            log.error('无法从ZenPacks加载插件.'
                      'ZenPacks中其中一个已经遗失或者损坏')
            import traceback
            log.debug(traceback.format_exc())
        return self.pluginLoaders.values()
        
    def _addPluginLoaders(self, loaderFactory, package):
        log.debug("从: %s加载收集器插件", package)
        try:
            loaders = loaderFactory.genLoaders(package, self.lastModName)
            for loader in loaders:
                self.pluginLoaders[loader.modPath] = loader
        except:
            log.error('从%s加载收集器失败', package)
            import traceback
            log.debug(traceback.format_exc())
            
class ModelingManager(object):
    """
    this class is not intended to be instantiated. instead it is a place to 
    hold a singleton instance of PluginManager without having them call the
    constructor when this module is imported.
    """
    
    instance = None
    
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = PluginManager(
                    lastModName='plugins',
                    packPath=('modeler',),
                    productsPaths=[('DataCollector',), 
                                   ('ZenWin', 'modeler',)])
        return cls.instance

class MonitoringManager(object):
    """
    this class is not intended to be instantiated. instead it is a place to 
    hold a singleton instance of PluginManager without having them call the
    constructor when this module is imported.
    """
    
    instance = None
    
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = PluginManager(
                    lastModName='parsers',
                    packPath=(),
                    productsPaths=[('ZenRRD',)])
        return cls.instance
        
def _loadPlugins(pluginManager, dmd):
    return pluginManager.getPluginLoaders(dmd.ZenPackManager.packs())

def loadPlugins(dmd):
    "Get PluginLoaders for all the modeling plugins"
    return _loadPlugins(ModelingManager.getInstance(), dmd)
    
def loadParserPlugins(dmd):
    "Get PluginLoaders for all the modeling plugins"
    return _loadPlugins(MonitoringManager.getInstance(), dmd)
    
def getParserLoader(dmd, modPath):
    "Get a PluginLoader for the given monitoring plugin's module path"
    return MonitoringManager.getInstance().getPluginLoader(
            dmd.ZenPackManager.packs(), modPath)
