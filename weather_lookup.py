import urllib2
import json
import sys
import re

if len(sys.argv) != 3:
    print "Usage python weatherlookup.py <State> <City>"

def geolookup(parsed_json):
    location = parsed_json['location']['city']
    temp_f = parsed_json['current_observation']['temp_f']
        
    print "Temp for city - " + location + ", " + state + " is "+ str(temp_f) + " F"
    return

def planner(parsed_json):
    trip_title = parsed_json['trip']['title']
    print trip_title
    
    start_date = parsed_json['trip']['period_of_record']['date_start']['date']['pretty']
    end_date = parsed_json['trip']['period_of_record']['date_end']['date']['pretty']
    print "PLANNER DATE --> "
    print "\nFROM: " + start_date
    print "\nTO: " + end_date
    
    high_temp1 = parsed_json['trip']['temp_high']['min']['F']
    high_temp2 = parsed_json['trip']['temp_high']['max']['F']
     
    print "Max temperature will be in the range ---> " + high_temp1 + " to " + high_temp2 + "(F)"
    
    low_temp1 = parsed_json['trip']['temp_low']['min']['F']
    low_temp2 = parsed_json['trip']['temp_low']['max']['F']
    
    print "Min temperature will be in the range ---> " + low_temp1 + " to " + low_temp2 + "(F)"
    
    chance_of_rain = parsed_json['trip']['chance_of']['chanceofrainday']['percentage']
    print "Chance of rain is " + chance_of_rain + " %"
    
    chance_of_hightemp = parsed_json['trip']['chance_of']['tempoverninety']['percentage']
    hot_day_name = parsed_json['trip']['chance_of']['tempoverninety']['name']
    hot_day_description = parsed_json['trip']['chance_of']['tempoverninety']['description']
    print "Chance of " + hot_day_name + "day (" + hot_day_description +") is " + chance_of_hightemp + " %"
    
    chance_of_humidity = parsed_json['trip']['chance_of']['chanceofhumidday']['percentage']
    print "Humidity ---> " + chance_of_humidity + " %"
    return

def alerts(parsed_json):
    alert_description = parsed_json['alerts'][0]['description']
    alert_expires = parsed_json['alerts'][0]['expires']
    message = parsed_json['alerts'][0]['message']
    
    print "Alert ---> " + alert_description
    print "Alert expires ---> " + alert_expires
    print message
    return

def almanac(parsed_json):
    normal_high = parsed_json['almanac']['temp_high']['normal']['F']
    record_high = parsed_json['almanac']['temp_high']['record']['F']
    record_high_year = parsed_json['almanac']['temp_high']['recordyear']
    
    normal_low = parsed_json['almanac']['temp_low']['normal']['F']
    record_low = parsed_json['almanac']['temp_low']['record']['F']
    record_low_year = parsed_json['almanac']['temp_low']['recordyear']
    
    print "NORMAL HIGH ---> " + normal_high + " (F)"
    print "RECORD HIGH ---> " + record_high + " (F)"
    print "RECORD HIGH YEAR : " + record_high_year
    
    print "NORMAL LOW ---> " + normal_low + " (F)"
    print "RECORD LOW ---> " +  record_low + " (F)"
    print "RECORD LOW YEAR : " + record_low_year

    return

def astronomy(parsed_json):
    print "Current time ---> " + parsed_json['moon_phase']['current_time']['hour'] + ":" + parsed_json['moon_phase']['current_time']['minute']
    print "Sunrise ---> " + parsed_json['moon_phase']['sunrise']['hour'] + ":" + parsed_json['moon_phase']['sunrise']['minute']
    print "Sunset ---> " + parsed_json['moon_phase']['sunset']['hour'] + ":" + parsed_json['moon_phase']['sunset']['minute']
    
    return

def forecast(parsed_json):
    for i in range(0,8):
        if i == 0:
            date_and_time = parsed_json['forecast']['txt_forecast']['forecastday'][i]['title'] + " " + parsed_json['forecast']['txt_forecast']['date']
        else:
            date_and_time = parsed_json['forecast']['txt_forecast']['forecastday'][i]['title']

        if i%2 == 0:
            print "\n"
    
        print date_and_time + " is " + parsed_json['forecast']['txt_forecast']['forecastday'][i]['fcttext']
    
    return

def tenday(parsed_json):
    for i in range(0,10):
        date_and_time = parsed_json['forecast']['simpleforecast']['forecastday'][i]['date']['pretty']
        high_temp = parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit']
        low_temp = parsed_json['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit']
        conditions = parsed_json['forecast']['simpleforecast']['forecastday'][i]['conditions']
        snow_allday_inches = parsed_json['forecast']['simpleforecast']['forecastday'][i]['snow_allday']['in']
        snow_allday_cms = parsed_json['forecast']['simpleforecast']['forecastday'][i]['snow_allday']['cm']
        max_wind = parsed_json['forecast']['simpleforecast']['forecastday'][i]['maxwind']['mph']
        avg_wind = parsed_json['forecast']['simpleforecast']['forecastday'][i]['avewind']['mph']
        
        print "\t\t** Day " + str(i) + " ---> " + date_and_time + " **"
        print "\t\t---------------------------------------------------"
        print "\t\tHIGH TEMP - " + high_temp + "\t\t LOW TEMP - " + low_temp
        print "\t\tConditions - " + conditions
        if int(snow_allday_cms) != 0:
            print "\t\tSnow in centimeters - " + snow_allday_cms
        if int(snow_allday_inches) != 0:
            print "\t\tSnow in inches - " + snow_allday_inches
        print "\t\tMAX WIND - " + str(max_wind) + "\t\t AVERAGE WIND - " + str(avg_wind) + "\n\n"
        
    return

def yesterday(parsed_json):
    print "Date ---> " + parsed_json['history']['date']['pretty']
    print "Temperature ---> " + parsed_json['history']['observations'][0]['tempi'] + " F"
    print "Temperature ---> " + parsed_json['history']['observations'][0]['tempm'] + " C"
    
    return

def history(parsed_json):
    print "Date ---> " + parsed_json['history']['date']['pretty']
    print "Temperature ---> " + parsed_json['history']['observations'][0]['tempi'] + " F"
    print "Temperature ---> " + parsed_json['history']['observations'][0]['tempm'] + " C"
    rain = parsed_json['history']['observations'][0]['rain']
    snow = parsed_json['history']['observations'][0]['snow']
    if int(rain) != 0:
        print "Rain ---> " + rain
    if int(snow) != 0:
        print "Snow ---> " + snow
    
    return

def fetch_details_for_weather_type_lookup(url,lookup_type):
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    
    if lookup_type == "geolookup":
         
        geolookup(parsed_json)
        
    elif lookup_type == "planner":
        
        planner(parsed_json)
    
    elif lookup_type == "alerts":
        
        alerts(parsed_json)
    
    elif lookup_type == "almanac":
        
        almanac(parsed_json)
        
    elif lookup_type == "astronomy":
        
        astronomy(parsed_json)
    
    elif lookup_type == "forecast":
        
        forecast(parsed_json)
            
    elif lookup_type == "10day":
        
        tenday(parsed_json)
        
    elif lookup_type == "yesterday":
        
        yesterday(parsed_json)
        
    elif lookup_type == "history":
        
        history(parsed_json)
        
    return

weather_lookup_type = sys.argv[1]
state = sys.argv[2]
list_city = sys.argv[3]
city = str(list_city)

# Format city and state
state=state.upper()
weather_lookup_type = weather_lookup_type.lower()

if ' ' in city:
    city = re.sub(' ','%20',city)

print "Weather lookup type ---> " + weather_lookup_type
print "City is "+ city
print "State is " + state


base_url = 'http://api.wunderground.com/api/' + your_api_key + '/'

if weather_lookup_type == "geolookup":
    url_suffix = 'geolookup/conditions/q/' + state + '/' + city + '.json'

elif weather_lookup_type == "planner":
    from_date=raw_input("Enter the FROM date in format(MMDD) without spaces ---> ")
    to_date=raw_input("Enter the TO date in format(MMDD) without spaces ---> ")
    url_suffix = 'planner_' + from_date + to_date + '/q/' + state + '/' + city + '.json'

elif weather_lookup_type == "alerts":
    print "**** This feature is only for United States ****"
    url_suffix = 'alerts/q/' + state + '/' + city + '.json'
    print "Displaying Alerts for city " + city + " in state/country " + state

elif weather_lookup_type == "almanac":
    url_suffix = 'almanac/q/' + state + '/' + city + '.json'
    print "Almanac for " + city + " in state/country " + state

elif weather_lookup_type == "astronomy":
    url_suffix = 'astronomy/q/' + state + '/' + city + '.json'
    print "Sunrise & Sunset for " + city + " in state/country " + state

elif weather_lookup_type == "forecast":
    url_suffix = 'forecast/q/' + state + '/' + city + '.json'
    print "Forecast for " + city + " in state/country " + state

elif weather_lookup_type == "10day":
    url_suffix = 'forecast10day/q/' + state + '/' + city + '.json'
    print "10 Day Forecast for " + city + " in state/country " + state

elif weather_lookup_type == "yesterday":
    url_suffix = 'yesterday/q/' + state + '/' + city  + '.json'
    print "Yesterday's weather for "+ city + " in state/country " + state

elif weather_lookup_type == "history":
    history_date = raw_input("Enter the date to search weather for: (Format: yyyymmdd) ---> ")
    url_suffix = 'history_' + history_date + '/q/' + state + '/' + city  + '.json'
    print "Historical weather for "+ city + " in state/country " + state

else:
    print "invalid option"

fetch_details_for_weather_type_lookup(base_url+url_suffix,weather_lookup_type)
