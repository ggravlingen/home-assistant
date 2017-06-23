#from soco import SoCo

#IP = "192.168.0.85"
#loadSocoData = SoCo(IP)

#model_name = loadSocoData.get_speaker_info()['model_name']
#player_name = loadSocoData.player_name
#state = loadSocoData.get_current_transport_info()['current_transport_state']




home = 0
for entity_id in hass.states.entity_ids('device_tracker'):
    state = hass.states.get(entity_id)
    if state.state == 'Home':
        home = home + 1

hass.states.set('sensor.people_home', home, {
    'unit_of_measurement': 'people',
    'friendly_name': 'People home'
})


#hass.states.set('sensor.sonos_play_1', 1, {
#    'unit_of_measurement': 'State',
#    'friendly_name': 'Sonos play 1'
#})


