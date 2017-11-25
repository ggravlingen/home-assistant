#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, sys, urllib

# Fix for special chars
#sys.setdefaultencoding("utf-8")

# CONFIG
url_playlist = "http://192.168.0.140:5005/living%20room/playlists"
url_favorites = "http://192.168.0.140:5005/favorites"

location_input_select = '/home/homeassistant/.homeassistant/extraconfig/input_select/'
location_shell_command = '/home/homeassistant/.homeassistant/extraconfig/shell_command/sonos/'


# LOAD PLAYLIST-LIST IN JSON-FORMAT
response_playlists = urllib.urlopen(url_playlist)
data_playlists = json.loads(response_playlists.read())


response_favorites = urllib.urlopen(url_favorites)
data_favorites = json.loads(response_favorites.read())


# START CREATING CONFIG-FILES

f = open(  location_input_select + "sonos_playlists.yaml","w")
f.write("sonos_playlist:" + "\n")
f.write("  name: Sonos Playlists" + "\n")
f.write("  options:" + "\n")
f.write("   - 'Pick one'\n")
for key in data_playlists:
  write_key = key.encode('utf-8')
  f.write("   - '" + write_key + "'\n")
f.write("  initial: 'Pick one'" + "\n")
f.write("  icon: 'mdi:playlist-check'" + "\n")
f.close()


f = open( location_input_select + "sonos_favorites.yaml","w")
f.write("sonos_favorites:" + "\n")
f.write("  name: Sonos Favorites" + "\n")
f.write("  options:" + "\n")
f.write("   - 'Pick one'\n")
for key in data_favorites:
  write_key = key.encode('utf-8')
  f.write("   - '" + write_key + "'\n")
f.write("  initial: 'Pick one'" + "\n")
f.write("  icon: 'mdi:playlist-check'" + "\n")
f.close()


def fileWriter(location_shell_command, outputfile, sonosCommand, dataArray):
  f = open(location_shell_command + outputfile + ".yaml","w")
  for key in dataArray:
    keyname = ''.join( e for e in key if e.isalnum() ).lower()
    keyvalue = urllib.quote(key.encode("utf-8"))
    try:
      # for backwards compatibility
      writeString = outputfile + "_" + keyname + ": /usr/bin/curl +X POST http://192.168.0.140:5005/living%20room/" + sonosCommand + "/" + keyvalue + "\n"
      f.write(writeString)
      writeString = outputfile + "_" + keyname + "_livingroom: /usr/bin/curl +X POST http://192.168.0.140:5005/living%20room/" + sonosCommand + "/" + keyvalue + "\n"
      f.write(writeString)
      writeString = outputfile + "_" + keyname + "_bathroom: /usr/bin/curl +X POST http://192.168.0.140:5005/bathroom/" + sonosCommand + "/" + keyvalue + "\n"
      f.write(writeString)
    except:
      print("")

f.close()

fileWriter(location_shell_command, "sonos_playlist", "playlist" ,data_playlists)
fileWriter(location_shell_command, "sonos_favorites", "favorite" ,data_favorites)
