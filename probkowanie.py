'''
# run before qt
import sip
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import processing
import numpy as np
import os
from osgeo import gdal
from osgeo import ogr
import code

# initialize Qt resources from file resources.py
import resources
from form import dialogForm


class TestPlugin:

    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        self.dialog = dialogForm()
        self.dialog.on_ok = self.on_ok

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/probkowanie/icon.png"), "Probkowanie plugin", self.iface.mainWindow())
        self.action.setStatusTip("It will do something, eventually")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Home made", self.action)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&Home made", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        # create and show a configuration dialog or something similar
        # print "TestPlugin: run called!"
        self.dialog.show()
        self.create_layer_list()

    def create_layer_list(self):

        self.dialog.chooseCombo.clear()
        self.dialog.chooseCombo_r.clear()

        layers = self.iface.legendInterface().layers()
        print(layers)
        #code.interact(local=dict(globals(), **locals()))
        self.dialog.chooseCombo.addItem('')
        self.dialog.chooseCombo_r.addItem('')
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                self.dialog.chooseCombo.addItem(layer.name(), layer)
            elif layer.type() == QgsMapLayer.RasterLayer:
                self.dialog.chooseCombo_r.addItem(layer.name(), layer)

    def on_ok(self):
        vector = self.dialog.chooseCombo.itemData(self.dialog.chooseCombo.currentIndex())
        raster = self.dialog.chooseCombo_r.itemData(self.dialog.chooseCombo_r.currentIndex())
        vector.startEditing()

        attribute_name = self.dialog.column_choose.text()

        create_new_attribute = True

        for i in vector.attributeList():
            if vector.attributeDisplayName(i) == attribute_name:
                create_new_attribute = False

        if create_new_attribute:
            pr = vector.dataProvider()
            pr.addAttributes([QgsField(attribute_name, QVariant.Double)])
            vector.updateFields()

        features = vector.getFeatures()
        for feature in features:
            point = feature.geometry().asPoint()
            value = raster.dataProvider().identify(point, QgsRaster.IdentifyFormatValue)
            feature.setAttribute(attribute_name, value.results().values()[0])
            vector.updateFeature(feature)
        #code.interact(local=dict(globals(), **locals()))
        vector.commitChanges()
        vector.updateFields()
        _writer = QgsVectorFileWriter.writeAsVectorFormat(vector, self.dialog.chooseField.text(), "utf-8", None, "ESRI Shapefile")
        print(_writer)
        self.dialog.accept()
