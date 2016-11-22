import homeassistant.appapi as appapi
import datetime

class WakeUp(appapi.AppDaemon):
  #initialize() function which will be called at startup and reload
  def initialize(self):
    # Create a time object for 6.15 every morning
    time = datetime.time(06, 15, 0)

    # Schedule a daily callback that will call run_daily() at 6.15 every morning
    self.run_daily(self.run_daily_callback, time)

   # Our callback function will be called by the scheduler every day at 7pm
  def run_daily_callback(self, kwargs):
    # Call to Home Assistant to turn the porch light on
    #self.turn_on("light.porch")

# sla pa lampor
# loopa igenom till radion startar
# sla pa lampa#2
