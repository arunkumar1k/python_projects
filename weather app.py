

import pytz
import ssl
import certifi
import requests
from tkinter import *
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import mysql.connector


# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="arunkumar",
    password="@12345",
    database="weather"
)
cursor = db.cursor()

# Check if the weather_data table exists, if not, create it
# Recreate the table with the modified schema

cursor.execute('DROP TABLE IF EXISTS weather_data')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(255),
        temperature VARCHAR(255),
        description VARCHAR(255),
        pressure VARCHAR(255),
        humidity VARCHAR(255),
        wind_speed VARCHAR(255)
    )
''')

##-----


def insert_weather_data(city, temperature, description, pressure, humidity, wind_speed):
    try:
        query = "INSERT INTO weather_data (city, temperature, description, pressure, humidity, wind_speed) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (city, temperature, description, pressure, humidity, wind_speed)
        cursor.execute(query, data)
        db.commit()
        print("Data successfully inserted into weather_data table!")
        
    except Exception as e:
        db.rollback()
        print(f"Error inserting data into the database: {e}")




##-----

# Tkinter GUI code

root = tk.Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable (False, False)


def getWeather():

    # Declare all values as a global variable
    global city  
    global temp
    global condition
    global description
    global pressure
    global humidity
    global wind_speed
    
    try:
        city=textfield.get()

        # Set the SSL certificate path
        ssl.create_default_context(cafile=certifi.where())
    
        geolocator = Nominatim(user_agent="geoapiexercises")
        location=geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude,lat=location.latitude)


        home=pytz.timezone(result)
        local_time=datetime.now(home)
        current_time=local_time.strftime("%I:%M: %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")


        #weather API
        api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=b0a9bdb1c2297ec43a11056295e27be5"
        
        json_data=requests.get(api).json()
        condition = json_data[ 'weather'][0]["main"]
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp']-273.15)
        pressure=json_data['main']['pressure']
        humidity=json_data['main']['humidity']
        wind_speed=json_data[ 'wind' ]['speed']
 
     
        # Update GUI labels
        t.config(text=(temp,"°C"))
        c.config(text=(condition,"|","FEELS","LIKE", temp,"°C"))
        w.config(text=wind_speed)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

        insert_weather_data(city, temp, description, pressure, humidity, wind_speed)
        
       
    except Exception as e:
        messagebox.showerror("Weather App", "Invalid Entry!!")
       



##search box
Search_image=PhotoImage(file="search.png")
myimage=Label(image=Search_image)
myimage.place(x=20,y=20)

##text field
textfield=tk.Entry(root, justify="center",width=17, font=("poppins", 25, "bold"), bg="#101010", border=0,fg="white")
textfield.place (x=50,y=40)
textfield.focus()

##search icon
Search_icon=PhotoImage (file="search_icon.png")
myimage_icon=Button(image=Search_icon, borderwidth=0, cursor="arrow", bg="#101010",command=getWeather)
myimage_icon.place(x=400, y=34)

##logo
Logo_image=PhotoImage(file="logo.png")
logo=Label(image=Logo_image)
logo.place(x=150, y=100)

##Bottom box
Frame_image=PhotoImage(file="box.png")
frame_myimage=Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

##time
name=Label(root, font=("arial", 15, "bold"))
name.place(x=30,y=100)
clock=Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

##label
label1=Label (root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#17a2d7")
label1.place(x=120, y=400)

label2=Label (root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#17a2d7")
label2.place(x=250, y=400)

label3=Label (root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#17a2d7")
label3.place(x=430, y=400)

label4=Label (root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#17a2d7")
label4.place(x=650, y=400)


t=Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)

c=Label (font=("arial", 15, 'bold'))
c.place(x=400, y=250)

w=Label(text="...", font=("arial", 20, "bold"), bg="#17a2d7")
w.place(x=120, y=430)

h=Label(text="...", font=("arial", 20, "bold"), bg="#17a2d7")
h.place(x=280, y=430)

d=Label(text="... ",font=("arial", 20, "bold"), bg="#17a2d7")
d.place(x=450, y=430)

p=Label(text="...", font=("arial", 20, "bold"), bg="#17a2d7")
p.place(x=670, y=430)


root.mainloop()

# Close the connection when done
db.close()








