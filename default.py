# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon


scriptID = 'plugin.video.alekino'
scriptname = "Films online"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import pLog, settings, Parser
import alekino, alekinoseriale

log = pLog.pLog()

class AlekinoTV:
  def __init__(self):
    log.info('Filmy online www.alekino.tv')
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()

  def showListOptions(self):
    params = self.parser.getParams()
    mode = self.parser.getIntParam(params, "mode")
    name = self.parser.getParam(params, "name")
    service = self.parser.getParam(params, 'service')
    if mode == None and name == None and service == None:
        log.info('Wyświetlam kategorie')
        self.CATEGORIES()
    elif mode == 3 or service == 'alekinoseriale':
        tv = alekinoseriale.alekinoseriale()
        tv.handleService()
    elif mode == 2 or service == 'alekino':
        tv = alekino.alekino()
        tv.handleService()

  def CATEGORIES(self):

        self.addDir("Filmy", 2, False, 'Filmy', False)
        self.addDir("Seriale", 3, False, 'Seriale', False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

  def listsTable(self, table):
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def LIST(self, table = {}):
      valTab = []
      strTab = []
      for num, tab in table.items():
          strTab.append(num)
          strTab.append(tab[0])
	  strTab.append(tab[1])
          valTab.append(strTab)
          strTab = []
      valTab.sort(key = lambda x: x[1])
      for i in range(len(valTab)):
          if valTab[i][2] == '': icon = False
          else: icon = valTab[i][2]
          self.addDir(valTab[i][1], valTab[i][0], False, icon, False)
      xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def addDir(self, name, mode, autoplay, icon, isPlayable = True):
    u=sys.argv[0] + "?mode=" + str(mode)
    if icon != False:
      icon = os.path.join(ptv.getAddonInfo('path'), "images/") + icon + '.png'
    else:
      icon = "DefaultVideoPlaylists.png"
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
    if autoplay and isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)

init = AlekinoTV()
init.showListOptions()
