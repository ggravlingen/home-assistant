#!/usr/bin/python
import json, sys, urllib

# Fix for special chars
#sys.setdefaultencoding("utf-8")

# CONFIG
url_playlist = "http://192.168.0.140:5005/kitchen/playlists"
url_favorites = "http://192.168.0.140:5005/favorites"

location_input_select = '/home/hass/.homeassistant/extraconfig/input_select/'
location_shell_command = '/home/hass/.homeassistant/extraconfig/shell_command/sonos/'

exit;

# LOAD PLAYLIST-LIST IN JSON-FORMAT
response_playlists = urllib.urlopen(url_playlist)

exit;

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


## Shell commands
f = open(location_shell_command + "sonos_playlist.yaml","w")
for key in data_playlists:
  keyname = ''.join(e for e in key if e.isalnum()).lower()
  keyvalue = urllib.quote(key)
  f.write("sonos_playlist_" + keyname + ": '/usr/bin/curl +X POST http://192.168.0.140:5005/kitchen/playlist/" + keyvalue + "'\n")
f.close()



f = open(location_shell_command + "sonos_favorites.yaml","w")
for key in data_favorites:
  print ""
  keyname = ''.join(e for e in key if e.isalnum()).lower()
  keyvalue = urllib.quote(key)
  #keyvalue = "aa"
  f.write("sonos_favorite_" + keyname + ": '/usr/bin/curl +X POST http://192.168.0.140:5005/kitchen/favorite/" + keyvalue + "'\n")
f.close()
