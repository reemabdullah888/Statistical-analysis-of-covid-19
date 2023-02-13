

Steps to help you run Almijmaj_Reem_HW5.py:

Please before you run the Almijmaj_Reem_HW5.py program, download rquirement.txt 
to make sure that you install the correct versions of the required Python libraries/packages. 
You can do this by typing in the command line: pip install -r requirements.txt
The libraries and packages that I used are:
beautifulsoup4==4.10.0
matplotlib==3.3.4
numpy==1.20.1
pandas==1.2.4
requests==2.25.1

Almijmaj_Reem_HW5.py is a file that has both the scraping code and the analysis code. 
You can run Almijmaj_Reem_HW5.py from the command line in two modes:


1- Default mode:  
python Almijmaj_Reem_HW5.py
It may take some time, for me, it works fine with 2 minutes delay.
The output you should expect:
Sample of web scraping data for the name of the US states and its area size in the square mile, a table with two columns the state name and its square mile. 
Sample of API data for the whole US Covid-19 tracking, a table with 3 columns date, positive increase, death increase.
Sample of API data for Covid-19 tracking of the US States, a table with 3 columns date, state,  death increase.
Some printed analysis will show up with 3 figures will show up one after another, you have to close the figure to see the next one.


2- Static mode:
To run the static mode, first after you zip the folder, make sure you are in the same directory/file path. 
In other words, you need to change the command line path and become in the same folder where the .py file and the static files (csv) exist. 
You can type in the command line: cd <path_to_files>
For example:
cd C:\Users\lenovo\Desktop\510\HW4\Almijmaj_Reem_DSCI510_HW4
Then in the command line type:
python Almijmaj_Reem_HW5.py --static
Please do not include any path to the static mode when you run the code.  
The expected output is the same as the output of the default mode. 

 

API keys:
My APIs are free and there is no key provided, so accessing the API’s URL are super easy. 

Extensibility:
•	Working with real-time data because the data I worked on within this project is static (already stored data) and not up-to-date. 
•	Using sophisticated statistical tools to get a meaningful insight out of the data because I used simple calculations.
        because the more advanced techniques were used, the more accurate the result became. 
•	Improve the graphs, and choose better plotting libraries.
        Also, create a better user interface that could help the user to see the result clearly and accurately. 

Maintainability:
•	Scraping the data could take sometime around 2 minutes to run in default mode, and the time might vary from computer to computer. If this happens, I highly suggest running the code in a static mode. 
•	If you did not download the right packages/libraries, the code might not work, and you might get unexpected results. 
•	There is no issue regarding the API keys, as I can access the data directly without accessing a key 
        also, there is no limitation for daily access. 


A small note: I have double check with the professor Yigal about my data analysis part,
 and he was saying it is fine and suggested me to mention that. Thank you. 
