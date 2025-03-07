# Module 10 Challenge       
          
For this module challenge, we are provided with Resources folder, which contains 2 CSV files (hawaii_measurements.csv,hawaii_stations.csv) and one sqlite file(hawaii.sqlite). These files contails the details of a vacation place, Honolulu, Hawaii. we have to analyze these data and help with the trip planning about the area.          

## Part 1: Analyze and Explore the Climate Data

In this section, we use the SQLAlchemy's **create_engine()** function to connect to our SQLite database.              
We also used the **automap_base()** function to reflect our tables into classes.   
Linked our python application to the database by creating a SQLAlchemy session.    

We have done the Precipitation Analysis and Station Analysis based on the data from the database.      
              
        
## Part 2: Design Your Climate App

In this section, we designed a Flask API based on the queries we developed in the previous analysis. app.py file contains the detailed code.
            






        ![Screenshot_homepage](https://github.com/user-attachments/assets/8655f126-350f-441b-8c4a-1a5dba85212a)


We used **jsonify** function to convert our API data to a valid JSON response object.     

run the code in any VSCode application or on any terminal/git bash.    

If you dont have the dependencies. We might have to install Flask, SQLAlchemy etc according to your settings.     

      
> pip install Flask SQLAlchemy
> pip install psycopg2
> pip install Flask
        
# Acknowledgement
          
I have done this challenge with the help of my Instructor and some internet searches.      






















