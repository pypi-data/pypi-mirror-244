from typing import Union

from PyQt5.QtWidgets import QAction, QDockWidget, QWidget

from huza.ribbon.RibbonPane import RibbonPane
from huza.ribbon.RibbonTab import RibbonTab


def get_extra(mainui):
    return mainui.extra


def get_action(mainui, action_name: str) -> QAction:
    if action_name in mainui.actions:
        return mainui.actions.get(action_name)
    return None


def get_dock(mainui, dock_name: str) -> QDockWidget:
    if dock_name in mainui.docks:
        return mainui.docks.get(dock_name)
    return None


def get_dock_current_ui(mainui, dock_name: str):
    if dock_name in mainui.docks:
        widget = mainui.docks.get(dock_name).widget()
        if widget is None:
            return None
        return widget.ui()
    return None


def get_dock_ui(mainui, dock_name: str, uiname: str):
    if dock_name in mainui.dockviews:
        dockviews = mainui.dockviews.get(dock_name)
        if uiname in dockviews:
            return dockviews.get(uiname).ui()
    return None


def get_ui(mainui, uiname: str):
    for k, v in mainui.dockviews.items():
        for ui_name, ui_f in v.items():
            if uiname == ui_name:
                return ui_f.ui()
    return None

def get_tab_name(mainui, tabname) -> Union[RibbonTab, None]:
    tabwidget = mainui.get_ribbon_tab()
    for i in range(tabwidget.count()):
        txt = tabwidget.tabText(i)
        if txt == tabname:
            return tabwidget.widget(i)
    return None

def get_panel_name(mainui, tabwidget: RibbonTab, panelname: str) -> Union[RibbonPane, None]:
    for i in range(tabwidget.layout().count()):
        panel: RibbonPane = tabwidget.layout().itemAt(i).widget()
        if hasattr(panel, '_panelname') and panel._panelname == panelname:
            return panel
    return None

def get_all_dock(mainui):
    return mainui.docks


def get_all_action(mainui):
    return mainui.actions


def get_all_dockview(mainui):
    return mainui.dockviews


def del_dock_ui(mainui, dock_name: str, uiname: str):
    if dock_name in mainui.dockviews:
        dockviews = mainui.dockviews.get(dock_name)
        if uiname in dockviews:
            w = dockviews[uiname]
            dock = mainui.docks.get(dock_name).widget()
            if dock == w:
                get_dock(mainui, dock_name).setWidget(QWidget())
            return dockviews.pop(uiname)
