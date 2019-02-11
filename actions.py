# encoding: utf-8

import gvsig

import os.path

from os.path import join, dirname

from gvsig import currentView
from gvsig import currentLayer

from java.io import File

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator
  
from org.gvsig.tools import ToolsLocator

from quickMapExport import QuickMapExport

class QuickMapExportExtension(ScriptingExtension):
  def __init__(self):
    pass

  def isVisible(self):
    return True

  def isLayerValid(self, layer):
    #if layer == None:
    #  #print "### reportbypointExtension.isLayerValid: None, return False"
    #  return False
    #mode = layer.getProperty("reportbypoint.mode")
    #if mode in ("", None):
    #  # Si la capa no tiene configurado el campo a mostrar
    #  # no activamos la herramienta
    #  return False
    return True
    
  def isEnabled(self):
    #layer = currentLayer()
    #if not self.isLayerValid(layer):
    #  return False
    return True

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "settool-quickmapexport":
      #print "### QuickinfoExtension.execute(%s)" % repr(actionCommand)
      layer = currentLayer()
      if not self.isLayerValid(layer):
        return
      viewPanel = currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      quickmapexport = QuickMapExport()
      quickmapexport.showTool("_Quick_map_export")

def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  quickmapexport_icon = File(gvsig.getResource(__file__,"images","quickmapexport.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.reportbypoint", "action", "tools-quickmapexport", None, quickmapexport_icon)

  quickmapexport_extension = QuickMapExportExtension()
  quickmapexport_action = actionManager.createAction(
    quickmapexport_extension,
    "tools-quickmapexport",   # Action name
    "Quick export map tool",   # Text
    "settool-quickmapexport", # Action command
    "tools-quickmapexport",   # Icon name
    None,                # Accelerator
    1009000000,          # Position
    i18n.getTranslation("_Quick_export_map")    # Tooltip
  )
  quickmapexport_action = actionManager.registerAction(quickmapexport_action)

  # Añadimos la entrada "Quickinfo" en el menu herramientas
  application.addMenu(quickmapexport_action, "tools/"+i18n.getTranslation("_Quick_export_map"))
  # Añadimos el la accion como un boton en la barra de herramientas "Quickinfo".
  application.addSelectableTool(quickmapexport_action, "QuickExportMap")

def main(*args):
  selfRegister()
  