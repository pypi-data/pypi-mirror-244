from PyQt5 import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

from huza.ribbon.qss.ribbonsmallbuttonqss import ribbonsmallbuttonqss
from huza.ribbon.qss.ribbosbutton import ribbonbuttonqss
from huza.ribbon.scale import gui_scale


class RibbonButton(QToolButton):
    def __init__(self, owner, action, is_large):
        QPushButton.__init__(self, owner)
        # sc = 1
        sc = gui_scale()
        self._actionOwner = action
        self.update_button_status_from_action()
        self.clicked.connect(self._actionOwner.trigger)
        self._actionOwner.changed.connect(self.update_button_status_from_action)

        if is_large:
            self.setMaximumWidth(120 * sc)
            self.setMinimumWidth(60 * sc)
            self.setMinimumHeight(75 * sc)
            self.setMaximumHeight(80 * sc)
            self.setStyleSheet(ribbonbuttonqss)
            self.setToolButtonStyle(3)
            self.setIconSize(QSize(32 * sc, 32 * sc))
        else:
            self.setToolButtonStyle(2)
            self.setMaximumWidth(120 * sc)
            self.setMinimumHeight(25 * sc)
            self.setIconSize(QSize(20 * sc, 20 * sc))
            self.setStyleSheet(ribbonsmallbuttonqss)

    def update_button_status_from_action(self):
        self.setText(self._actionOwner.text())
        self.setStatusTip(self._actionOwner.statusTip())
        self.setToolTip(self._actionOwner.toolTip())
        self.setIcon(self._actionOwner.icon())
        self.setEnabled(self._actionOwner.isEnabled())
        self.setCheckable(self._actionOwner.isCheckable())
        self.setChecked(self._actionOwner.isChecked())
