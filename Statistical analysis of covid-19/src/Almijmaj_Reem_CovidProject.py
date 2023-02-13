# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 17:04:33 2021

@author: lenovo
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import sys
import csv 
import numpy as np
import matplotlib.pyplot as plt


def State_names():
    
    State_name = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA",
                          "MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD",
                          "TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    #return the abbrivation of US states, because after scraping the data a full state name was giving, so I needed something to transform the state name
    return State_name


# I define this outside because the variable all_body is used in other function to create square mile varible 
access = requests.get('https://statesymbolsusa.org/symbol-official-item/national-us/uncategorized/states-size')  #requesting the webpage
content = access.content #taking only the source code
s = BeautifulSoup(content, 'html.parser')  # parse the source code
all_body = s.find_all('tr')

def abbrev_to_us_state():

    us_state_to_abbr = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY"}
        
    #invert the dictionary
    abbrev_to_us_state = dict(map(reversed, us_state_to_abbr.items()))
    # the function help to reverse what I have recive from the web - scraping, the full name state into its abbreviation 
    return abbrev_to_us_state
 
def default_function():
    
    # accessing the website to get the state name and its sqaure miles ( area size )
    access = requests.get('https://statesymbolsusa.org/symbol-official-item/national-us/uncategorized/states-size')  #requesting the webpage
    content = access.content #taking only the source code
    s = BeautifulSoup(content, 'html.parser')  # parse the source code
    all_body = s.find_all('tr')
    
    
    # create a dictionry to help with my analysis 
    Square_M = dict ()
    # create list so i can create a panda data frame from it and orgainze my data clearly
    State_Name = []
    Square_Miles = []
    # Create a dictionary for state name as key and square mile as value
    for i in all_body[1:]:     
        state_nam = i.find_all('td')[1].text #taking only tags that are td and the first element and extract only the text, that is located in there
        square_mile = i.find_all('td')[2].text.replace(',','') # remove , from the square mile becasue i need to devide the number and treated as int instead of string. 
        Square_M[state_nam]  =  square_mile  # assigning square mile as values to the dictionary
        state_name = i.find_all('td')[1].text
        if state_name in State_Name: continue  # so I DO not have duplicated state names each time I run the code
        else:
            State_Name.append(state_name) # only append unmentioned states name
            square_miles = i.find_all('td')[2].text
            Square_Miles.append(square_miles) # append corresponding square mile

    abbrev_us_state = abbrev_to_us_state() #call a function to channge the state names into its abbreviation 
    for key, value in abbrev_us_state.items(): # change the states name that are stored inside the list to its abbreviation 
        for i in range (len(State_Name)):
            if value == State_Name[i]:
                State_Name[i] = key #swap the state name with its abbrivation 
    
    #Changing the state name into its abbreviation for the dictionary variable! 
    for key, value in abbrev_us_state.items():
        Square_M[key] = Square_M.pop(value) #deleting the old key and replace it with the new one
    #SquareMiles
    data = {
        'StateName':State_Name,
        'SquareM':Square_Miles}
    
    # create a panda data frame 
    Sates_size_df = pd.DataFrame(data)
    # Exporting Pandas DataFrame to CSV file 
    Sates_size_df.to_csv('Sates_size.csv',index = False)
    print ('\n Sample of web scraping data for the name of the US states and its area size in square mile \n')
    print (Sates_size_df.head())


   ######################################################
   
    # US_covid
    # accessing the api for taking data about US related to COVID-19
    req = requests.get('https://api.covidtracking.com/v1/us/daily.json')# reponse = reponse.json()
    jason_doc = req.json()  #put it into a jason format
    US_df = pd.DataFrame(jason_doc) # create a panda data frame from the jason file
    US_df['date'] = pd.to_datetime(US_df['date'], format='%Y%m%d') #change the date formate from string into date time 
    subset_US_df = US_df[["date", "positiveIncrease","deathIncrease"]].copy() # taking the relevant columns that i need from the panda fram and store it into a panda data frame 
    def delete_negative(x):
        if x < 0:
            return 0  #to make sure there is no wrong enter and i dont get a negative value as a number of death number because it is imposible to have death number in minus 
        else:
            return x  
    subset_US_df["deathIncrease"] = subset_US_df["deathIncrease"].apply(delete_negative) #removing negative values from death increase column 
    subset_US_df["positiveIncrease"] = subset_US_df["positiveIncrease"].apply(delete_negative) # removing negative values from positiveIncrease column , infected individual can not be negative so i NEED to remove any possible of wrong entery. 
    subset_US_df.to_csv('US_covid_tracking.csv',index = False) # transform the panda dataframe into csv file
    print ('\n Sample of API data for the whole US Covid-19 tracking \n')
    print(subset_US_df.head())

    
    ######################################################
    # State_covid 
    # requesting the data (COVID-19 tracking for each state in the US, request from the api 
    re = requests.get('https://api.covidtracking.com/v1/states/daily.json')# reponse = reponse.json()
    jason_document = re.json() # put it into a json format 
    State_df = pd.DataFrame(jason_document) # create panda dataframe
    State_df['date'] = pd.to_datetime(State_df['date'], format='%Y%m%d') #change the date formate from string into a date time
    subset_State_df = State_df[["date", "state","deathIncrease"]].copy() # create a subsit of panda dataframe with specific columns 
    subset_State_df["deathIncrease"] = subset_State_df["deathIncrease"].apply(delete_negative) # delete negative values
    subset_State_df.to_csv('State_covid_tracking.csv',index = False) # transform from panda into a csv file 
    print ('\n Sample of API data for Covid-19 tracking of US States \n')
    print(subset_State_df.head(7))
    
## start

    
    State_name = State_names()
    # sum the total death cases for each state in the US
    sum_death_state = dict()
    for state in State_name:
        sum_death_state[state] = State_df.query('state == "%s"' % state)['deathIncrease'].sum()

##end

#Analysis Start:
    # 1 
    # Finding CFR [case fatality rate ] in the USA
    # to calculate the total number of infected individuals with covid-19 in the USA
    sum_infected_cases = subset_US_df["positiveIncrease"].sum()
    # to calculate the total death of covid-19 in the USA
    sum_death_cases = subset_US_df["deathIncrease"].sum()
    # calculate the case fatality rate in the US
    # CFR = total number of deaths from covid-19 / total number of infected individuals 
    CFR = sum_death_cases / sum_infected_cases
    print ('\n The result of calculating the case fatality rate for the COVID-19 disease  in the USA is ', CFR * 100)

    

    #2
    # Compare mortality rate in the US for specific day in 2021 with a specific day in 2020 where vaccine was not invented
    # last day I have on my dataset is 2021-03-07
    deathIn2021 = int (subset_US_df[subset_US_df['date'] == '2021-03-07']['deathIncrease']) # take death increase number of specific date 
    deathIn2020 = int (subset_US_df[subset_US_df['date'] == '2020-12-10']['deathIncrease']) # take death increase number of specific date 
    print ('\n The result of comparing mortality rate in the US for a specific day in 2021 after a mass of covid-19 vaccination processes with a specific day in 2020 where the covid-19 vaccine was not invented \n')
    # create a dataset
    height = [deathIn2020 , deathIn2021]
    bars = ('2020-12-10', '2021-03-07')
    x_pos = np.arange(len(bars))
    # Create bars with different colors
    plt.bar(x_pos, height, color=['red', 'green'])
    # Create names on the x-axis
    plt.xticks(x_pos, bars)
    plt.title('comparing mortality rate in the US for specific day')
    # Show graph
    plt.show()
    
    
    
    #3 
    Square_M = Dic_SquareMile()
    # Calculate the Death cases density of a state 
    Death_Case_Desnsity_State = dict()
    for state in State_name:
        sumD = sum_death_state[state] # calculate the total number of death for each state
        squareM = Square_M[state] #take the squair mile for the specific state
        divi = int (sumD) / int (squareM)
        Death_Case_Desnsity_State[state] = divi #store the result in a dict. 
    death_density_df = pd.DataFrame.from_dict(Death_Case_Desnsity_State, orient='index')
    death_density_df.columns=['DeathDesnsity']
    print ('\n The result of calculating the death cases density of COVID-19 disease for each state in the US \n')
    print (death_density_df)  
    print (' \n Plotting sample of Covid-19 death cases densities of 12 states of US \n')
    # showing only some of Death States densities. 
    first12pairs = {k: Death_Case_Desnsity_State[k] for k in list(Death_Case_Desnsity_State)[3:15]}
    keys = first12pairs.keys()
    values = first12pairs.values()
    plt.bar(keys, values)
    plt.ylabel('Density') # to create a lable for it
    plt.title('Death States densities') #title for the image
    plt.show() # to show the figure



    #4 
    
    #Top 5 States with higest rate of codvid-19 deaths in the US
    # Sort in descending order US states that have a high rate of covid-19 deaths.
    sorted(sum_death_state.items(), key= lambda x: x[1])[-5:]
    print ('\n Result of sorting in descending order US states that have a high rate of covid-19 deaths.\n')
    print ('Top 5 States with higest rate of codvid-19 deaths in the US \n')
    labels= ['PA', 'FL', 'NY', 'TX','CA']
    colors=['blue', 'yellow', 'green', 'orange','red']
    sizes= [24349,32266, 39029, 44451, 54124]
    plt.pie(sizes,labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Top 5 States with higest rate of codvid-19 deaths in the US')
    plt.show()
    
def sum_death_state():
    State_name = State_names() #call function 
    sum_death_state = dict() 
    subset_State_df = pd.read_csv('State_covid_tracking.csv')   # read a csv file from the directory
    for state in State_name:
        sum_death_state[state] = subset_State_df.query('state == "%s"' % state)['deathIncrease'].sum() #find the total death number for each state 
    return sum_death_state
def Dic_SquareMile():
    abbrev_us_state = abbrev_to_us_state()
    global all_body
    Square_M = dict ()
    # Create a dictionary for state name as key and square mile as value
    for i in all_body [1:]:     
        state_name = i.find_all('td')[1].text # taking out only the text from the tag td and it is going to be in the first index 
        square_miles = i.find_all('td')[2].text.replace(',','') # removing the , from the squre mile value becasue I will apply calcuation and I can not do it if it is a string.
        Square_M[state_name]  =  square_miles
    #Changing the state name into its abbreviation ! 
    for key, value in abbrev_us_state.items():
        Square_M[key] = Square_M.pop(value) # deleting the old key and replace it with new one
    return Square_M


def static_function():
# State_Size 
    Sates_size_df = pd.read_csv("Sates_size.csv")  # open csv file 
    print ('\n Sample of web scraping data for the name of the US states and its area size in square mile \n')
    print (Sates_size_df.head()) # print the first 5 elements 
    
 
    
# US_covid
    subset_US_df = pd.read_csv('US_covid_tracking.csv') # open csv file 
    print ('\n Sample of API data for the whole US Covid-19 tracking \n')
    print(subset_US_df.head()) # print the first 5 elements 


# State_covid 
    subset_State_df = pd.read_csv('State_covid_tracking.csv')  # open csv file     
    print ('\n Sample of API data for Covid-19 tracking of US States \n')
    print(subset_State_df.head(7))  # print the first 7 elements 
 
    
 
#Analysis Start:
    # 1 
    # Finding CFR [case fatality rate ] in the USA
    # to calculate the total number of infected individuals with covid-19 in the USA
    sum_infected_cases = subset_US_df["positiveIncrease"].sum()
    # to calculate the total death of covid-19 in the USA
    sum_death_cases = subset_US_df["deathIncrease"].sum()
    # calculate the case fatality rate in the US
    # CFR = total number of deaths from covid-19 / total number of infected individuals 
    CFR = sum_death_cases / sum_infected_cases
    print ('\n The result of calculating the case fatality rate for the COVID-19 disease  in the USA is ', CFR * 100)

    

    #2
    # Compare mortality rate in the US for specific day in 2021 with a specific day in 2020 where vaccine was not invented
    # last day I have on my dataset is 2021-03-07
    deathIn2021 = int (subset_US_df[subset_US_df['date'] == '2021-03-07']['deathIncrease'])
    deathIn2020 = int (subset_US_df[subset_US_df['date'] == '2020-12-10']['deathIncrease'])
    print ('\n The result of comparing mortality rate in the US for a specific day in 2021 after a mass of covid-19 vaccination processes with a specific day in 2020 where the covid-19 vaccine was not invented \n')
    # create a dataset
    height = [deathIn2020 , deathIn2021]
    bars = ('2020-12-10', '2021-03-07')
    x_pos = np.arange(len(bars))
    # Create bars with different colors
    plt.bar(x_pos, height, color=['red', 'green'])
    # Create names on the x-axis
    plt.xticks(x_pos, bars)
    plt.title('comparing mortality rate in the US for specific day')
    # Show graph
    plt.show()
    
    
    
    #3 
    Square_M = Dic_SquareMile()
    # Calculate the Death cases density of a state 
    Death_Case_Desnsity_State = dict()
    State_name = State_names()
    sum_death_s = sum_death_state()
    for state in State_name:
        sumD = sum_death_s[state]
        squareM = Square_M[state]
        divi = int (sumD) / int (squareM)
        Death_Case_Desnsity_State[state] = divi
    death_density_df = pd.DataFrame.from_dict(Death_Case_Desnsity_State, orient='index')
    death_density_df.columns=['DeathDesnsity']
    print ('\n The result of calculating the death cases density of COVID-19 disease for each state in the US \n')
    print (death_density_df)  
    print (' \n Plotting sample of Covid-19 death cases densities of 12 states of US \n')
    # showing only some of Death States densities. 
    first12pairs = {k: Death_Case_Desnsity_State[k] for k in list(Death_Case_Desnsity_State)[3:15]}
    keys = first12pairs.keys()
    values = first12pairs.values()
    plt.bar(keys, values)
    plt.ylabel('Density')
    plt.title('Death States densities')
    plt.show()



    #4 
    
    #Top 5 States with higest rate of codvid-19 deaths in the US
    # Sort in descending order US states that have a high rate of covid-19 deaths.
    sorted(sum_death_s.items(), key= lambda x: x[1])[-5:]
    print ('\n Result of sorting in descending order US states that have a high rate of covid-19 deaths.\n')
    print ('Top 5 States with higest rate of codvid-19 deaths in the US \n')
    labels= ['PA', 'FL', 'NY', 'TX','CA']
    colors=['blue', 'yellow', 'green', 'orange','red']
    sizes= [24349,32266, 39029, 44451, 54124]
    plt.pie(sizes,labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Top 5 States with higest rate of codvid-19 deaths in the US')
    plt.show()    
 
    
 
    
 
    
# to make it posible to run from the command line 

if __name__ == '__main__':
    if len(sys.argv)== 1:  #default mode
        default_function()  
    elif sys.argv[1]== '--static':  #static mode
       # path_to_static_data = sys.argv[2]
        static_function()
    
        


