# Weather Lookup GUI using Tkinter
# Author - Srikkanth Govindaraajan

#Python Imports
from Tkinter import *
import urllib2
import json
from ScrolledText import ScrolledText
import tkMessageBox

# Class 
class App:
    # Constructor
    def __init__(self,master):
        
        # Create the Menu for the GUI
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        
        # File Menu with Load location and exit options
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Load location",command=self.save_location)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        
        # Help menu with 'about' option
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)
        
        # We create three frames. Top, main, bottom frames. Some prefer grid manager.
        self.top_frame = Frame(master,bg='#A9A7A6')
        self.top_frame.pack(side=TOP)
        
        # Main frame
        frame = Frame(master,bg='#B9B7B6')
        frame.pack(fill='y', expand=True)
        
        # Bottom frame
        self.bottom_frame = Frame(master,bg='#D5E3ED')
        self.bottom_frame.pack(side=BOTTOM)
        
        # Help text to be displayed always
        help_label = Label(self.top_frame, text="*** If country is US, enter state abbreviation eg. CA, MA, OH.\nElse enter country name: eg. India, UK, Australia\n\n")
        help_label.pack(side=LEFT)
        
        # Label and text box for entering State/country
        state_label = Label(frame,text="STATE / COUNTRY")
        state_label.pack(side=LEFT)
        
        self.state = Entry(frame)
        self.state.pack(side=LEFT)
        
        # Label and text box for entering City
        city_label = Label(frame,text="CITY")
        city_label.pack(side=LEFT)
        
        self.city = Entry(frame)
        self.city.pack(side=LEFT)
        
        # Create Radiobuttons. Another choice would be to use list box.
        R1 = Radiobutton(root, text="Geo Lookup", variable=var, value=1,command=self.show_options)
        R1.pack( anchor = W )
        
        R3 = Radiobutton(root, text="Trip Planner",variable=var, value=3, command=self.show_options)
        R3.pack( anchor = W )
        
        R4 = Radiobutton(root, text="Alerts", variable=var, value=4, command=self.show_label)
        R4.pack( anchor = W )
        
        R5 = Radiobutton(root, text="Astronomy", variable=var, value=5,command=self.show_options)
        R5.pack( anchor = W )
        
        R6 = Radiobutton(root, text="Forecast", variable=var, value=6,command=self.show_options)
        R6.pack( anchor = W )
        
        R7 = Radiobutton(root, text="10 Day Forecast", variable=var, value=7,command=self.show_options)
        R7.pack( anchor = W )
        
        R8 = Radiobutton(root, text="Yesterday weather", variable=var, value=8,command=self.show_options)
        R8.pack( anchor = W )
        
        R2 = Radiobutton(root, text="Almanac", variable=var, value=2,command=self.show_options)
        R2.pack( anchor = W )
        
        R9 = Radiobutton(root, text="Historical weather", variable=var, value=9, command=self.show_options)
        R9.pack( anchor = W )
        
        # Create three buttons
        self.submit = Button(self.bottom_frame,text="Submit",command=self.find_weather)
        self.submit.pack(side=LEFT)
        
        self.save = Button(self.bottom_frame,text="Save Location(s)",command=self.save_location)
        self.save.pack(side=LEFT)
        
        self.quit = Button(self.bottom_frame,text="Quit",command=self.quit_program)
        self.quit.pack(side=LEFT)
        
        # Label and text box for displaying output
        self.output_label = Label(self.bottom_frame,text="\n\n\nWeather output:")
        self.output_label.pack(side=LEFT)
        
        self.output = ScrolledText(self.bottom_frame,bg='#D66B54') # ScrolledText looks better. Can use Text as well.
        self.output['font'] = ('monaco','12')
     
    def show_label(self):
        # Clear any other old labels
        self.clear_labels_and_text()
        if var.get() == 4: # Alerts
            # Display label related to alerts
            self.alert_label = Label(self.bottom_frame,text="**** This feature is only for United States ****")
            self.alert_label.pack(side=TOP)
            
        return
    
    def save_location(self):
        # RFE
        tkMessageBox.showinfo("Note", "This feature has not been implemented yet")
        return
    
    def quit_program(self):
        exit(0)
        return
    
    def about(self):
        # Just a note
        tkMessageBox.showinfo("About Weather lookup app", "This application is for demonstration purposes only. Not intended for commercial use.")
        return
    
    def clear_labels_and_text(self):
        dummy=0 # dummy variable basically for NO OP
        # We have different try-except blocks for different labels.
        # The reason is - at any point of time only one or none of the labels / text fields
        # would be displayed. Hence having one try-except will create problems.
        try:
            # Clear the history date label and text box.
            self.history_date_label.pack_forget()
            self.history_date.pack_forget()
        except AttributeError:
            dummy=1 # Do nothing basically
            
        try:
            # Clear the labels and text boxes associated with the trip planner
            self.from_date.pack_forget()
            self.from_date_label.pack_forget()
          
            self.to_date.pack_forget()
            self.to_date_label.pack_forget()
        except AttributeError:
                dummy=1
        
        try:
            # Clear the alert label for alters
            self.alert_label.pack_forget()
        except AttributeError:
            dummy=1
        
        try:
            # Clear the note label associated with the historical weather
            self.note_label.pack_forget()
        except AttributeError:
            dummy=1
        
        # Delete any output displayed in the textbox
        self.output.delete(1.0,END)
        
        return
        
    
    def show_options(self):
        dummy = 0
        if var.get() == 3: # Trip Planner
            # Clear any other labels or input forms
            self.clear_labels_and_text()
            
            # Display options for trip planner
            self.from_date_label = Label(self.bottom_frame,text="Departure (MMDD):")
            self.from_date_label.pack(side=LEFT)
             
            self.from_date = Entry(self.bottom_frame)
            self.from_date.pack(side=LEFT)
             
            self.to_date_label = Label(self.bottom_frame,text="Return (MMDD):")
            self.to_date_label.pack(side=LEFT)  
             
            self.to_date = Entry(self.bottom_frame)
            self.to_date.pack(side=LEFT)
         
        elif var.get() == 9: # HIstorical Weather
            # Clear any other labels or input forms
            self.clear_labels_and_text()
            
            self.note_label = Label(self.bottom_frame,text="NOTE: Year should be greater than 2000")
            self.note_label.pack(side=TOP)
            
            # Display options for HIstorical Weather
            self.history_date_label = Label(self.bottom_frame,text="Historical date (yyyymmdd):")
            self.history_date_label.pack(side=RIGHT)
            
            self.history_date = Entry(self.bottom_frame)
            self.history_date.pack(side=RIGHT)
        
        else:
            # Clear any other labels or input forms
            self.clear_labels_and_text()
        return
    
    def find_weather(self):
        # Clear any other labels or input forms
        self.clear_labels_and_text()
        
        # If state or city is empty show error message
        if not self.state.get() or not self.city.get():
            tkMessageBox.showerror("Error","Please enter both Country/State and City")
            return
        
        # Convert state / country to uppercase and replaces spaces with %20 for url construction
        state = self.state.get()
        if ' ' in state:
            state = re.sub(' ','%20',state)
        state = state.strip().upper()
        
        # Replace spaces in city with %20 for url construction
        city = self.city.get()
        if ' ' in city:
            city = re.sub(' ','%20',city)
        city = city.strip().lower()
        
        # Base URL with API key
        base_url = 'http://api.wunderground.com/api/' + your_api_key + '/'
        
        # Assign url_suffix for each option
        if var.get() == 1:
            url_suffix = 'geolookup/conditions/q/' + state + '/' + city + '.json'
        
        elif var.get() == 2:
            url_suffix = 'almanac/q/' + state + '/' + city + '.json'
        
        elif var.get() == 3:
            from_date = self.from_date.get()
            to_date = self.to_date.get()
            url_suffix = 'planner_' + from_date + to_date + '/q/' + state + '/' + city + '.json'
        
        elif var.get() == 4:
            url_suffix = 'alerts/q/' + state + '/' + city + '.json'
        
        elif var.get() == 5:
            url_suffix = 'astronomy/q/' + state + '/' + city + '.json'
        
        elif var.get() == 6:
            url_suffix = 'forecast/q/' + state + '/' + city + '.json'
        
        elif var.get() == 7:
            url_suffix = 'forecast10day/q/' + state + '/' + city + '.json'
        
        elif var.get() == 8:
            url_suffix = 'yesterday/q/' + state + '/' + city  + '.json'
        
        elif var.get() == 9: 
            history_date = self.history_date.get()
            url_suffix = 'history_' + history_date + '/q/' + state + '/' + city  + '.json'
        
        try:
            # Send request and get parsed data
            url = base_url + url_suffix
            f = urllib2.urlopen(url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
        except UnboundLocalError:
            # Throw message if none of radiobuttons are selected.
            tkMessageBox.showerror("Invalid Input","Select one of the options")
            return
        
        self.output.delete(1.0,END)
        if var.get() == 1: # Geo Lookup
            # Parse and send output
            try:
                location = parsed_json['location']['city']
                temp_f = parsed_json['current_observation']['temp_f']
                if '%20' in state:
                    state = re.sub('%20',' ',state)
                self.output.text = "Temp for city - " + location + ", " + state + " in F is "+ str(temp_f)
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)
        
        elif var.get() == 2: # Almanac
            # Parse and send output
            try:
                normal_high = parsed_json['almanac']['temp_high']['normal']['F']
                record_high = parsed_json['almanac']['temp_high']['record']['F']
                record_high_year = parsed_json['almanac']['temp_high']['recordyear']
                
                normal_low = parsed_json['almanac']['temp_low']['normal']['F']
                record_low = parsed_json['almanac']['temp_low']['record']['F']
                record_low_year = parsed_json['almanac']['temp_low']['recordyear']
                
                self.output.text = ("NORMAL LOW ---> " + normal_low + " (F)\n"
                + "RECORD LOW ---> " + record_low + " (F)\n"
                + "RECORD LOW YEAR : " + record_low_year + "\n"
                + "NORMAL HIGH ---> " + normal_high + " (F)\n"
                + "RECORD HIGH ---> " + record_high + " (F)\n"
                + "RECORD HIGH YEAR : " + record_high_year) + "\n"
            except KeyError: 
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)

        elif var.get() == 3: # Trip Planner
            # Parse and send output
            try:
                trip_title = parsed_json['trip']['title']
                
                start_date = parsed_json['trip']['period_of_record']['date_start']['date']['pretty']
                end_date = parsed_json['trip']['period_of_record']['date_end']['date']['pretty']
                
                self.output.text = (trip_title + "\n\nPLANNER DATE --> \nFROM: " + start_date + "\nTO: " + end_date)
                
                high_temp1 = parsed_json['trip']['temp_high']['min']['F']
                high_temp2 = parsed_json['trip']['temp_high']['max']['F']
                
                self.output.text = self.output.text + ("\nMax temperature will be in the range ---> " + high_temp1 + " to " + high_temp2 + "(F)\n")
                
                low_temp1 = parsed_json['trip']['temp_low']['min']['F']
                low_temp2 = parsed_json['trip']['temp_low']['max']['F']
                
                self.output.text = self.output.text + ("\nMin temperature will be in the range ---> " + low_temp1 + " to " + low_temp2 + "(F)\n")
                
                chance_of_rain = parsed_json['trip']['chance_of']['chanceofrainday']['percentage']
                
                self.output.text = self.output.text + ("\nChance of rain is " + chance_of_rain + " %\n")
                
                chance_of_hightemp = parsed_json['trip']['chance_of']['tempoverninety']['percentage']
                hot_day_name = parsed_json['trip']['chance_of']['tempoverninety']['name']
                hot_day_description = parsed_json['trip']['chance_of']['tempoverninety']['description']
                
                self.output.text = self.output.text + ("\nChance of " + hot_day_name + "day (" + hot_day_description +") is " + chance_of_hightemp + " %\n")
                
                chance_of_humidity = parsed_json['trip']['chance_of']['chanceofhumidday']['percentage']
                
                self.output.text = self.output.text + ("\nHumidity ---> " + chance_of_humidity + " %\n")
                
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)

        elif var.get() == 4: # Alerts
            # Parse and send output
            try:
                alert_description = parsed_json['alerts'][0]['description']
                alert_expires = parsed_json['alerts'][0]['expires']
                message = parsed_json['alerts'][0]['message']
                
                self.output.text = ("Alert ---> " + alert_description + "\nAlert expires ---> " + alert_expires + "\n" + message)
                
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            except IndexError:
                tkMessageBox.showerror("Error", "Alerts feature applicable only to states in US.")
                self.output.text = "ERROR: state not within the US."
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)

        elif var.get() == 5: # Astronomy
            # Parse and send output
            try:
                self.output.text = ("Current time ---> " + parsed_json['moon_phase']['current_time']['hour'] + ":" + parsed_json['moon_phase']['current_time']['minute']
                                    + "\nSunrise ---> " + parsed_json['moon_phase']['sunrise']['hour'] + ":" + parsed_json['moon_phase']['sunrise']['minute'] 
                                    + "\nSunset ---> " + parsed_json['moon_phase']['sunset']['hour'] + ":" + parsed_json['moon_phase']['sunset']['minute'])
                
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)

        elif var.get() == 6: # Forecast
            # Parse and send output
            self.output.text = "\n"
            try:
                for i in range(0,8):
                    if i == 0:
                        date_and_time = parsed_json['forecast']['txt_forecast']['forecastday'][i]['title'] + " " + parsed_json['forecast']['txt_forecast']['date']
                    else:
                        date_and_time = parsed_json['forecast']['txt_forecast']['forecastday'][i]['title']
                    self.output.text = self.output.text + (date_and_time + " is " + parsed_json['forecast']['txt_forecast']['forecastday'][i]['fcttext'] + "\n\n")
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)

        elif var.get() == 7: # 10DayForcast
            # Parse and send output
            self.output.text = "\n"
            try:
                for i in range(0,10):
                    date_and_time = parsed_json['forecast']['simpleforecast']['forecastday'][i]['date']['pretty']
                    high_temp = parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit']
                    low_temp = parsed_json['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit']
                    conditions = parsed_json['forecast']['simpleforecast']['forecastday'][i]['conditions']
                    snow_allday_inches = parsed_json['forecast']['simpleforecast']['forecastday'][i]['snow_allday']['in']
                    snow_allday_cms = parsed_json['forecast']['simpleforecast']['forecastday'][i]['snow_allday']['cm']
                    max_wind = parsed_json['forecast']['simpleforecast']['forecastday'][i]['maxwind']['mph']
                    avg_wind = parsed_json['forecast']['simpleforecast']['forecastday'][i]['avewind']['mph']

                    self.output.text = self.output.text + ("\t\t** Day " + str(i) + " ---> " + date_and_time + " **\n" 
                                        +"\t\t---------------------------------------------------\n"
                                        + "\t\tHIGH TEMP - " + high_temp + "\t\t LOW TEMP - " + low_temp + "\n"
                                        + "\t\tConditions - " + conditions + "\n")
                    
                    if int(snow_allday_cms) != 0:
                        self.output.text = self.output.text + ("\t\tSnow in centimeters - " + snow_allday_cms + "\n")
                    if int(snow_allday_inches) != 0:
                        self.output.text = self.output.text + ("\t\tSnow in inches - " + snow_allday_inches + "\n")
                    self.output.text = self.output.text + ("\t\tMAX WIND - " + str(max_wind) + "\t\t AVERAGE WIND - " + str(avg_wind) + "\n\n")       
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)
        
        elif var.get() == 8: # Yesterday weather
            # Parse and send output
            try:
                self.output.text = ("Date ---> " + parsed_json['history']['date']['pretty'] 
                                    + "\nTemperature ---> " + parsed_json['history']['observations'][0]['tempi'] + " F"
                                    + "\nTemperature ---> " + parsed_json['history']['observations'][0]['tempm'] + " C")
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0,self.output.text)
                self.output.pack(side=BOTTOM)
        
        elif var.get() == 9: # Historical Weather
            # Parse and send output
            try:
                self.output.text = ("Date ---> " + parsed_json['history']['date']['pretty']
                                    + "\nTemperature ---> " + parsed_json['history']['observations'][0]['tempi'] + " F\n"
                                    + "Temperature ---> " + parsed_json['history']['observations'][0]['tempm'] + " C\n")
                
                rain = parsed_json['history']['observations'][0]['rain']
                snow = parsed_json['history']['observations'][0]['snow']
                if int(rain) != 0:
                    self.output.text = self.output.text + ("Rain ---> " + rain + "\n")
                if int(snow) != 0:
                    self.output.text = self.output.text + ("Snow ---> " + snow + "\n")
            except KeyError:
                self.output.text = "ERROR: please check your input!"
            finally:
                self.output.insert(1.0, self.output.text)
                self.output.pack(side=BOTTOM)

# Create app instance and run
root = Tk()
var = IntVar()
root.wm_title("Weather Lookup")
app = App(root)

root.mainloop()
