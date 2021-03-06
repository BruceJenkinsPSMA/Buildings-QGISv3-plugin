# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BuildingBeta
                                 A QGIS plugin
 Building Beta API Plugin for QGISv3
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-05-10
        git sha              : $Format:%H$
        copyright            : (C) 2018 by PSMA
        email                : bruce.jenkins@psma.com.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.
 *
 * Note 11/05/2018 : credential import did not work. Expect Python env path
  issues. There are Key Place holders within code, this will be fixed next
  iteration of code.
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .building_beta_dialog import BuildingBetaDialog
import os.path
import requests
import json
import re
#import pprint
#import credentials # file needs to contain API key.
#import credentials # note v3 credentils import does not work. Expect Python Enviromental issue.
key = 'INSERT KEY HERE'
#from qgis.core import QgsMapLayerRegistry #breaks 3



from qgis.core import *
import qgis.utils

class BuildingBeta:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BuildingBeta_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = BuildingBetaDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Building Beta API')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BuildingBeta')
        self.toolbar.setObjectName(u'BuildingBeta')

        #bj 10/5/2018
        self.dlg.lineEdit.clear()
        #self.dlg.pushButton.clicked.connect(self.select_output_file)
        self.dlg.pushButton.clicked.connect(self.embedded_address_search)
        #self.dlg.comboBox.
        self.dlg.pushButton_2.clicked.connect(self.embedded_select_address)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BuildingBeta', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/building_beta/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Building Beta API'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Building Beta API'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def embedded_address_search(self):
        bl_url = 'https://api.psma.com.au/beta/v1/addresses/?addressString=?'

        #key = credentials.API_KEY
        # bl_url = 'https://api.psma.com.au/beta/v1/'

        headers = {
            "Authorization": key,
            "Accept": "application/json"
        }

        address_name = self.dlg.lineEdit.text()
        print(address_name)
        address_name_format = re.sub(' ', '%20', address_name)
        # address_name_format = self.(padAddress)

        ### eg from above.... self.dlg.pushButton.clicked.connect(self.embedded_address_search)



        bl_address_serarch = bl_url + address_name_format  # + '/footprint2d/'

        response = requests.get(bl_address_serarch, headers=headers, verify=False)
        data3 = response.json()
        data2 = json.loads(response.text)

        print("data3")
        print(data3)

        address_limiter = 0
        layer_list = []

        for item in data3['data']:  # .'address_id':
            print (item) # 9th april trace.
            item_id = item['addressId']

            # out on the 9th april to work with links and pageination.


            address_limiter = address_limiter + 1
            #
            print (item_id)
            # print address_formatted
            layer_list.append(item_id)  # + "-" + address_formatted)
            self.dlg.comboBox.addItems(layer_list)

    def embedded_select_address(self):
        index = self.dlg.comboBox.currentIndex()
        print ("index = " + str(index))
        focus_addr = self.dlg.comboBox.currentText()
        print (focus_addr)
        bl_buildingIDs = 'https://api.psma.com.au/beta/v1/addresses/' + focus_addr + '/'

        ###key = credentials.API_KEY
        key = 'InsertKeyHere'
        # bl_url = 'https://api.psma.com.au/beta/v1/'

        headers = {
            "Authorization": key,
            "Accept": "application/json"
        }

        response = requests.get(bl_buildingIDs, headers=headers, verify=False)
        data = response.json()
        print (data)
        # data2 = json.loads(response.text)
        # data2 = json.dumps(data)

        buildings = data['relatedBuildingIds']
        print (buildings)

        layer_list = []
        # self.dlg.listView.setModel(buildings)
        displayInt = 0

        for building in buildings:
            displayInt = displayInt + 1
            item_id = building
            print (item_id)
            # layer_list.append(item_id)
            bl_url = 'https://api.psma.com.au/beta/v1/buildings/'
            key = 'INSERTKEY HERE'
            headers = {
                "Authorization": key,
                "Accept": "application/json"
            }
            building_id = building
            bl_urlBuildingLinks = bl_url + building_id + '/footprint2d/'
            print (bl_urlBuildingLinks)
            response2 = requests.get(bl_urlBuildingLinks, headers=headers, verify=False)
            data2 = response2.json()
            data3 = json.dumps(data2)
            print(data3)
            vlayer = QgsVectorLayer(data3, focus_addr + "_" + building_id, "ogr")
            print(vlayer)###
            #QgsMapLayerRegistry.instance().addMapLayer(vlayer)

            QgsProject.instance().addMapLayer(vlayer)
            # if displayInt == 1: #8/5/2018 removed for demon.
            # canvas = qgis.utils.iface.mapCanvas()
            # canvas.setExtent(vlayer.extent())

        # vLayer = iface.activeLayer()
        # canvas = qgis.utils.iface.mapCanvas()
        # canvas.setExtent(vlayer.extent())

        # vLayer = iface.activeLayer()
        # canvas = iface.mapCanvas()
        # extent = vLayer.extent()
        # canvas.setExtent(extent)


        self.dlg.lineEdit.clear()
        self.dlg.comboBox.clear()

