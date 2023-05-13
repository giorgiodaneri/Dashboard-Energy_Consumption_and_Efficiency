# Dashboard: Energy Consumption and Efficiency
A dashboard programmed in Python. Topics covered are energy consumption and efficiency all over the world. We selected a few Key Performance Indicators (KPIs) to evaluate carbon footprint and energetic sustainability of the major countries in the world.

The dashboard consists of four interactive graphs.
- The choropleth represents the energy mix of all the major countries in the world. The user can select the energy source of interest and check which countries rely upon it the most. Alternatively, the user can check the growth of a certain energy source between 2020 and 2021. 
- The bar chart shows CO2 emissions for several countries. The values shown are two: global share and emissions per capita. The second one is overall more significant, as the value is normalized by the population number and tells how much that country pollutes for each citizen. 
- The box plot represents LCOE (Levelized Cost of Electricity) values for different energy sources. The user can select a different discount rate and check how the sample distribution changes. The actual distribution of the values is found next to each whisker. 
- The scatter plot renders LCOE values based on the selected country. Each dot corresponds to a specific project, whose characteristics are shown in the hover text. While the previous graph prescinds has a general approach, this one is tailored on the single country and its financial ecosystem, as well as econimic benefits granted for renewable energy projects and availability of a certain energy resource.

# How to make it work on your device
First of all, you will need to change the path to the datasets in the Dashboard.py file with their actual location on your memory. Then you will probably need to adjust values in the css file in order to fit your monitor resolution. 

# How it looks
![WhatsApp Image 2023-05-13 at 5 49 43 PM](https://github.com/giorgiodaneri/Dashboard-Energy_Consumption_and_Efficiency/assets/118806991/9cf230ef-9f5d-4ce5-af3d-41e3306d870e)
Please note that a dashboard is conceived to be examined and interacted with in fullscreen. This screenshot only aimes at giving a glimpse of its aesthetic appearance. 
