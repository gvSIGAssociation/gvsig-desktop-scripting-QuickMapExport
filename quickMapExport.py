# encoding: utf-8

import gvsig
from org.gvsig.app import ApplicationLocator

from java.io import File
from java.io import FileInputStream

from org.gvsig.tools import ToolsLocator

from org.gvsig.andami import PluginServices
from org.gvsig.tools.swing.api import ToolsSwingLocator
import gvsig
from gvsig.libs.formpanel import FormPanel

def visorPDF(rutaAbsoluta):
    formatManagers = ToolsLocator.getExtensionPointManager().get("HyperLinkAction")
    pdfManager = formatManagers.get("PDF_format").create()
    uri = File(str(rutaAbsoluta)).toURI()
    panel = pdfManager.createPanel(uri)
    windowManager = ToolsSwingLocator.getWindowManager()
    windowManager.showWindow(panel,"Visor PDFs",windowManager.MODE.WINDOW)
    
class QuickMapExport(FormPanel):
  def __init__(self):
    FormPanel.__init__(self,gvsig.getResource(__file__, "quickMapExport.xml"))
    self.txtTitle.setText(gvsig.currentView().getName())
    self.cboFormat.addItem("A4 Horizontal")
  def getQParams(self, *args):
    qparams={
          'format':
              {'type': self.cboFormat.getSelectedItem()},
          'titleparams': 
              {'name':self.txtTitle.getText()},
          'viewparams':
              {'view': gvsig.currentView()},
          'legend':
              {'show':self.chbLegend.isSelected()},
          'grid':
              {'show':self.cbhGrid.isSelected()},
          'scale':
              {'show':self.chbForceScale.isSelected(),
              'number':float(self.txtScale.getText())},
          'image':
              {'option':False}
    }
    return qparams
  def btnPreview_click(self,*args):
    #Guardar pdf en disco temp y mostrarlo visualizdor pdf
    qparams = self.getQParams()
    loadQuickMap(qparams, True)
    
  def btnAccept_click(self,*args):
    qparams = self.getQParams()
    loadQuickMap(qparams)
    
def main(*args):
  m = QuickMapExport()
  m.showTool("_Quick_map_export")
  #qparams={
  #        'titleparams': 
  #            {'name':'Titulo Mapa'},
  #        'viewparams':
  #            {'view': gvsig.currentProject().getView("titu1")}
  #        }
          
def loadQuickMap(qparams, preview=False):
    format = qparams['format']['type']
    if format=="A4 Horizontal":
      templatePath = gvsig.getResource(__file__, "data", "A4Horizontal.gvslt")
    xmlFile = File(templatePath)
    nis = FileInputStream(xmlFile)
    persistenceManager = ToolsLocator.getPersistenceManager()
    persistentState = persistenceManager.loadState(nis)
    layout = persistenceManager.create(persistentState)
    layoutDocument = layout.getDocument()

    ## Configure options
    ## Tags, mTitle, mView, mLegend, mNord, mScale
    cnt = layoutDocument.getLayoutContext()
    allframes = cnt.getAllFFrames()
    for f in allframes:
      print "Tag:", f.getTag(), f
      if f.getTag()=="mTitle":
        params = qparams['titleparams']
        f.clearText()
        f.addText(params['name'])
      elif f.getTag()=="mView":
        params = qparams['viewparams']
        print "Params View: ", params
        f.setView(params['view'])
    
    ## Open it in gvsig
    p = ApplicationLocator.getManager().getProjectManager().getCurrentProject()
    p.addDocument(layoutDocument)
    #layout.getLayoutControl().setTool("layoutselect")
    #lm = layoutDocument.getFactory()
    #layout.setLayoutManager(lm)
    mdi = PluginServices.getMDIManager()
    panel = mdi.addWindow(layout)
    mdi.closeWindow(panel)
    
    if preview:
      print "PREVIEW"
      outtemppath = gvsig.getTempFile("quickmap",".pdf")
      outfile = File(outtemppath)
      print outtemppath
      layout.layoutToPDF(outfile)
      try:
        visorPDF(outtemppath)
      except:
        pass
      return
    layout.layoutToPDF()
      