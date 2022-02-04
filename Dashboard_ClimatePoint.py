# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 15:12:49 2021

@author: felix
"""

import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


#global variables
plot_bg = "#ebf3f1"
c1 = "#4ABF9F"
c2 = "#01664B"



#%% functions
def boxplot(df, column_list, by_list):
    
    """
    Creates a boxplot from the given input.
    
    Args:
        df (DataFrame): The dataframe from which data is taken.
        column_list (list): List of columns to be used for calculation.
        by_list (str): Name of column by which data should be sorted.
    
    Returns:
        fig (figure): The boxplot from the input
    
    """
    

#Calculate height of boxplot

    #trying a diffferent measure t o calculate height. Number of groups in plot. not working currently, Trying to calculate number of names in y axis.
    # for i in enumerate(by_list):
    #     x = df[i[1]].nunique()
    # number= np.prod(x)
    number = len(df.index) #use number of datapoints as proxy for boxplot height
    height = (number/3) + 7 #Height of boxplot depending on number of datapoints
    if height > 100:
        height = 100
    else:
        height = height
    
#Plotting    
    fig, ax = plt.subplots(figsize=(20,height))

    df.boxplot(column = column_list,by = by_list, 
                rot = 0, grid = False, patch_artist=True, 
                boxprops=dict(color=c2, facecolor=c1),
                capprops=dict(color=c2),
                whiskerprops=dict(color=c2),
                flierprops=dict(color=c2, markeredgecolor=c2),
                medianprops=dict(color=c2),
                ax=ax,
                vert = False)
#Formatting   
    label = df['ISIC 4'].iloc[0]

    ax.grid(axis="y", color="w", linewidth=1.5)
    ax.set_facecolor(plot_bg)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    #ax.legend(loc = 0, frameon = False,) #not needed

    title_boxplot = 'ISIC: ' +str(label) 
    plt.title( title_boxplot, fontsize = 25 )
    plt.xticks(fontsize =20)
    plt.yticks(fontsize =20)
    plt.tight_layout()	
    plt.suptitle('') 
    # col2.pyplot(plt) 
    return fig


# Read data

#Import Data Ecoinvent. Currently set at reading the file with RANDOM Values. License is needed.
@st.cache #this allows for the app to only read the csv once and cache it, instead of reading it everytime.
def get_data_ecoinvent():
    """
    Imports Ecoinvent data from the already formatted csv in the main directory  
    
    Args:
        None
    
    Returns:
        eco_df: Dataframe of Ecoinvent Data
    """
    eco_df = pd.read_csv('./Ecoinvent38_Random.csv', index_col=(0))
    eco_df.dropna(subset = ["ISIC 1"], inplace = True)
    eco_df.sort_values(by =['ISIC code'], inplace = True)
    return eco_df

#Import Data Exiobase
@st.cache() #this allows for the app to only read the csv once and cache it, instead of reading it everytime
def get_data_exio():
    """
    Imports EXIOBASE data from the already formatted csv in the main directory "EXIOBASE_RESULTS_MERGED.csv"  
    
    Args:
        None
    
    Returns:
        eco_df: Dataframe of Ecoinvent Data
    """
    exio_df = pd.read_csv ('./EXIOBASE_RESULTS_MERGED.csv', usecols = range(1,12))
    #Data filtering
    #Dropping NaN
    exio_df.dropna(axis=0, inplace = True)
    #Dropping infinity values
    exio_df = exio_df[exio_df['Value'] != np.inf]
    return exio_df


#%%### DASHBOARD SETUP
#General setup
st.set_page_config(layout ='wide')#Set layout and title
image = Image.open('./ClimatePoint_logo.png')#Climate Point Logo
st.image(image, width =150 ) #Set image in dashboard
st.title ('ClimatePoint Dashboard Demo') #Title

#About
about = st.expander('About')
about.markdown("""This Dashboard showcases the Global Warming Potential of multiple products and services according to ISIC Classification. \n
It allows for the easy interaction with two databases: Ecoinvent (v3.8) and EXIOBASE (v3.4, year 2011). 
The query results can be used to easily look up recorded emission values of given ISIC codes. 
This Dashboard was created as part of a MSc Industrial Ecology project in conjunction with ClimatePoint \n

Ecoinvent Data is not real. A license is necessary to use the desired data for defined purposes. Data shown are randomized values and structure is based on Ecoinvent's Database Overview.
 """)

#instructions
instructions = st.expander('Instructions')
instructions.markdown('''

To use the dashboard, select your desired ISIC code 
from level 1 to level 4. Please allow for some time after selecting a level. Due to the databases sizes calculations may take a few seconds. 
Once a full ISIC code is selected the two databases offer further customization options in the center console.
If you do not know the ISIC code of your desired product or service, search for it at the bottom of the sidebar to identify the ISIC Code and unit.
                      
### Ecoinvent
Click on the box saying, “Select specific products/services, geography, and type of activity”. In the opening dropdown menu, you can specify 
up to a product-specific level what data you are interested in. If names go beyond the box hover over the name to see the full text. Clicking
 on the “x” on the right clears the selection. Clicking on the button opens a dropdown menu to select products, geographies, i.e. geographic 
 locations, and types of activities, i.e. market activities or ordinary transformation activities. For further explanations of the terminology 
 open the “Ecoinvent terminology” box below.


### EXIOBASE
In the EXIOBASE menu you can adjust the perspective, type of GHG intensity and type of average. Furthermore, you 
can adjust the selected regions in the field below. For further explanations of the terminology open the “EXIOBASE terminology” box below.

#### Important Note!
Make sure you read the “Disclaimer” box! Use the results with caution. Both databases are in constant development and undergo changes and updates. 
Emission values should never be taken at face value, but rather as an approximation.
                   
''')

#Disclaimer Paragrpah
disclaimer = st.expander('Disclaimer')
disclaimer.markdown('''
The use of this tool is only for academic purposes. No industrial application is permitted. The data for Ecoinvent is analysed under the Campus Ecoinvent license of Leiden University (retrieved from https://www.ecoinvent.org). The data for Exiobase is open-source and can be used for academic and non-academic purposes (retrieved from https://www.exiobase.eu).
Please cite as follows: Tan, Chia Wu, Delgado Elizundia, Felix, Breekveldt, Laurence, Ilgemann, Pablo, Müller, Amelie (2022). ClimatePoint Rapid Impact Assessment Dashboard. Leiden University                     
''')

st.write('''***''') #line break

#%% ISIC Selector

#Call function to read ecoinvent data
eco_df = get_data_ecoinvent()

#Define Selecting menu
st.markdown("## **ISIC Filter for selection**")

#Filters and selection boxes
ISIC1_List=eco_df['ISIC 1'].unique().tolist() # Create list of unique ISIC 1 values
ISIC1_List.sort()
ISIC1 = st.selectbox('Select ISIC 1 Sector', ISIC1_List) # Selectbox of values in the list above


ISIC2_List = eco_df['ISIC 2'].loc[eco_df['ISIC 1'] == ISIC1].unique() # Create list of unique ISIC 2 values within the selected ISIC 1 
ISIC2 = st.selectbox('Select ISIC 2 Division',ISIC2_List, 0) # Selectbox of values in the list above

# ISIC3_List=eco_df['ISIC 3'].unique()
ISIC3_List = eco_df['ISIC 3'].loc[eco_df['ISIC 2'] == ISIC2].unique() # Create list of unique ISIC 3 values  within the selected ISIC 2 
ISIC3 = st.selectbox('Select ISIC 3 Group', ISIC3_List, 0) # Selectbox of values in the list above

# ISIC4_List =  eco_df['ISIC 4'].unique()
ISIC4_List = eco_df['ISIC 4'].loc[eco_df['ISIC 3'] == ISIC3].unique() # Create list of unique ISIC 4 values  within the selected ISIC 3
ISIC4 = st.selectbox('Select ISIC 4 Class', ISIC4_List, 0) # Selectbox of values in the list above

#%% search bar in the middle
st.write('''***''') #line break

st.markdown(''' ### Don't know the ISIC Classification? \n Search by product and find it's ISIC category:''')

search_bar = st.expander("Search ISIC codes")

#helper
product_list2  = eco_df['Reference Product Name'].unique()  
product_helper = search_bar.selectbox('Product/Service', product_list2) #Creating a multiselect of available products/services
helper = eco_df[eco_df['Reference Product Name']==product_helper] #selects all processes matching the input
helper = helper.loc[:, [ 'ISIC 1', 'ISIC 2','ISIC 3', 'ISIC 4', 'Unit']].iloc[0] # Show the column names you want (loc) and first row (iloc[0])
search_bar.dataframe(helper)

#%% set columns
st.write('''***''') #line break

#Columns of dashboard
col2, col3 = st.columns((1,1)) #Creating columns

st.write('''***''') #line break

#%%#### COLUMN TWO - ECOINVENT
col2.title('ECOINVENT v3.8') #Title
col2.markdown(""" Current Ecoinvent data imported is not real. Random values for the data shown""")

#Terminology of ecoinvent expander
eco_terminology = col2.expander ("Ecoinvent Terminology")
eco_terminology.markdown ('''

**Product/Service**: A reference product. This represents a specific product, for example grapes or cement.
\n
            
**Geography**: Depending on data availability one or several regions or countries are available per product/service. 
For some products/services there is only the global level (GLO), but for others data on many countries may be available. 
Countries are denoted in two-letter standard. RoW is rest of worl nd. RER is Europe (the region, not the EU!). CA-QC is Quebec, Canada.
/n

**Type of activity**: There are two types of activities: 1) ordinary transformation activity and 2) market activity.
* *Ordinary transformation activities* are the actual production processes and its connected emissions. 
* *Market activities* are summaries of all ordinary transformation activities, 
    usually aggregated at a global level. Market activities contain a mix of regional production activities as well as transport and losses between 
    the producer and an average global consumer. Where possible ordinary transformation activities should be selected over market activities.

            ''')



#Ecoinvent only filters in an expander bar
eco_expander = col2.expander ('Select specific products/services, geography, and Unit')  #Creating expander conainer in column 2
product_list  = eco_df['Reference Product Name'].loc[eco_df['ISIC 4'] == ISIC4].unique()  #Getting list of pproducts/services of chosen ISIC 4
product = eco_expander.multiselect('Product/Service', product_list , product_list) #Creating a multiselect of available products/services

geo_list  = eco_df['Geography'].loc[eco_df['Reference Product Name'].isin(product)].unique()  #Getting list of geographies of chosen products/services
geography = eco_expander.multiselect('Geography', geo_list  , geo_list ) #Multiselect box of geographies

#Unit button
unit_List = eco_df['Unit'].loc[eco_df['Reference Product Name'].isin(product)].unique() # Create list of unique ISIC 4 values  within the selected ISIC 3
unit = eco_expander.radio('Select Unit (Only products with the same unit can be displayed)', unit_List) # Selectbox of values in the list above

# Selected data for Econinvent
# Selection of dataframe based need to comply on filters of sidebar and ecoinvent only filters
selected_data_ecoinvent= eco_df[ (eco_df['ISIC 4']== ISIC4) & # == only takes one value
                      (eco_df['Reference Product Name'].isin(product)) &
                      (eco_df.Geography.isin(geography)) &# isin can take a list
                      (eco_df['Unit'] == unit)].copy()



#Data
col2.write ('#### Table of Selected Data ')
col2.write('Data Dimension: ' + str(selected_data_ecoinvent.shape[0]) + 
          ' rows and ' + str(selected_data_ecoinvent.shape[1]) + 
          ' columns')

# col2.dataframe(selected_data_ecoinvent)
col2.dataframe(selected_data_ecoinvent.loc[:,['Reference Product Name', 
                                              'Name',
                                              "Special Activity Type", 
                                              "Geography",
                                              "GWP [kg CO2 eq.]","Unit", 
                                              "Sector"]])



col2.markdown (""" **How to interpret the table** \n
Table results show available data in most detail, but also the least visual. It shows the emissions summarized in kg CO2 eq. per 1 unit 
of reference product and the specific region. The emission data seems very accurate, considering emission values go to the third decimal.
However, this value should be used carefully for two reasons: \n
1. Actual emissions depend on a great number of factors, thus the presented value is only an approximation. 
2. Some processes, and their respective emissions, are simply extrapolations and educated guesses 
from other processes, thus their values may be even more inaccurate. \n
To check how the data was gathered for a process the user must consult 
the [Ecoinvent website](https://ecoinvent.org/) and search for the process’ PDF documentation file.""" )

#%% Boxplot of Product and Services
col2.write ('#### Boxplot of product and services \n Ordinary Transforming Activity')


#Dataframe of only values of processes (ordinary transformation activity)
boxplot_tranf_act_df = selected_data_ecoinvent [selected_data_ecoinvent["Special Activity Type"] == 'ordinary transforming activity']
#Boxplot
boxplot1_ECO = boxplot(boxplot_tranf_act_df, 
                        ["GWP [kg CO2 eq.]"], 
                        ['Reference Product Name'])
plt.xlabel('Global Warming Potential '+'[CO2eq / ' + str(unit)+']', fontsize = 30) #Unit label

col2.pyplot(boxplot1_ECO)

# btn1 = col2.download_button(
#              label="Download plot",
#              data=boxplot1_ECO,
#              file_name="boxplot1.png",
#              mime="image/png"
#            )  
plt.close()

col2.markdown ("""The boxplot summarizes available emissions Global Warming Potential (GWP) data on a reference product level.
              It only inlcudes the Ordinary transforming activity type, aka, the actual production process itself.
            The range of the data stems from regional variabilities in production emissions. 
            Use the boxplot below to visualize the GWP of the Market Activity. 
            Datapoints outside the interquartile range are shown as circles outside the boxplot.""")

#%% descriptive statistics table of selected products and services

#section title
col2.write ('###### Descriptive statistics of boxplot ')

#calculating descriptive statistics
descriptive_statistics = boxplot_tranf_act_df["GWP [kg CO2 eq.]"].describe()

#putting results in pandas dataframe
descriptive_statistics_df = pd.DataFrame(descriptive_statistics.iloc[1:])

#formatting dataframe for better visuals and understanding
descriptive_statistics_df = descriptive_statistics_df.rename(index={"mean": "Mean",
                                                                    "std": "Standard deviation",
                                                                    "min": "Minimum",
                                                                    "25%": "Lower quartile",
                                                                    "50%": "Median",
                                                                    "75%": "Upper quartile",
                                                                    "max": "Maxmimum"})

#displaying results on dashboard
col2.write(descriptive_statistics_df)

#%% Boxplot of Product and Services by type of activity
col2.write ('#### Boxplot of product and services by type of activity ' '\n' 'Ordinary Transforming activity and Market Activity')
boxplot2_ECO = boxplot(selected_data_ecoinvent, ["GWP [kg CO2 eq.]"], ['Reference Product Name','Special Activity Type'])

plt.xlabel('Global Warming Potential '+'[CO2eq / ' + str(unit)+']', fontsize = 30) #Unit label
#plt.savefig('boxplot_eco2.png')
col2.pyplot(boxplot2_ECO) 
 

#Download button
# btn2 = col2.download_button(
#         label="Download plot",
#         data=boxplot2_ECO,
#         file_name="boxplot_eco2.png",
#         mime="image/png"
#       )                  
plt.close()  
   
col2.markdown ("""The boxplot summarizes all available emissions data on a reference product level differentiating 
                between ordinary transformation activities and market activities. 
                The range of the data stems from regional variabilities in production emissions. 
                The separation of ordinary transformation activities and market activities avoids double counting. 
                Therefore, use this boxplot wherever possible. Datapoints outside the interquartile range are shown as circles outside the boxplot. """ )


#%% descriptive statistics table of selected products and services by activity type

#getting unique activity types
unique_activity_types = list(selected_data_ecoinvent["Special Activity Type"].unique())


#sorting by activity
activity_list = []

for activity in unique_activity_types:
    by_activity_list = selected_data_ecoinvent[selected_data_ecoinvent["Special Activity Type"] == activity]
    activity_list.append(by_activity_list)


#calculating descriptive statistics per element in activity list
descriptive_stats_list_ECO_boxplot2 = []

for element in activity_list:
    descriptive_statistics_boxplot2 = element["GWP [kg CO2 eq.]"].describe().iloc[1:]
    descriptive_stats_list_ECO_boxplot2.append(descriptive_statistics_boxplot2)


for element, title in list(zip(descriptive_stats_list_ECO_boxplot2, unique_activity_types)):
    
    descriptive_statistics2_df = pd.DataFrame(element)
    #formatting dataframe for better visuals and understanding
    descriptive_statistics2_df = descriptive_statistics2_df.rename(index={"mean": "Mean",
                                                                    "std": "Standard deviation",
                                                                    "min": "Minimum",
                                                                    "25%": "Lower quartile",
                                                                    "50%": "Median",
                                                                    "75%": "Upper quartile",
                                                                    "max": "Maxmimum"})
    #heading in dashboard
    col2.write ('###### Descriptive statistics for ' + title)
    #displaying results on dashboard
    col2.write(descriptive_statistics2_df)

 
#%% #### COLUMN three -  EXIOBASE
col3.title('EXIOBASE')
exio_terminology = col3.expander ("EXIOBASE Terminology")
exio_terminology.markdown ('''
##### Terminology:

**Perspective**: EXIOBASE comes with two perspectives: 1) consumer and 2) producer.\n
* The *consumer perspective* shows emission values of products as they are consumed in a certain region or country. 
    Thus, the consumer perspective includes domestic production, imports from other regions but excludes exports. 
* On the other hand, the *producer perspective* includes the emission values of products as they are produced in the respective region, 
    irrespective of where they are later consumed.  Depending on the application of the benchmark, either the consumer or producer perspective 
    is more suitable. Note that due to the highly globalized economy, there can be significant differences between the two perspectives. 
    On a global level, consumer and producer perspectives are the same since trade between regions is summed up. 
\n

**Type of GHG intensity**: Due to the richness in data in EXIOBASE, we decided to offer 4 types of GHG intensity: 2 mass-based intensities 
and two monetary intensities. The user is invited to choose the type of GHG intensity that suits her best.\n
1. GHG intensity per physical weight of the product: This GHG intensity shows the emission values in kg CO2 eq. per one kilogram physical mass, such as kg CO2-eq per kg of dairy product.
2. GHG intensity per embodied mass of the product: This GHG intensity shows the emission values in kg CO2 eq. per one kilogram material extracted from the environment in the process of producing a certain product. 
3.	GHG intensity per product costs: This GHG intensity shows the emission values in kg CO2 eq per euro of product costs.
4.	GHG intensity per product profit: This GHG intensity shows the emission values in kg CO2 eq per euro of product profit. The difference between this and the other monetary intensity above is that for this GHG intensity, only the margin of profit, also called value added, of a product is considered as the nominator. This makes more profitable products less carbon-intensive. 
\nNote that among the above mentioned GHG intensities, only GHG intensity per physical weight has a direct match in the Ecoinvent data base, which does not contain embodied mass or monetary data. 

\n
**Type of average**: For the cases, where ISIC products match EXIOBASE products, the average of GHG intensities of these products is calculated. 
Here, we offer a normal mean and a weighted mean. The normal mean assumes an equal weight of all contributing products flowing into an ISIC code. 
The weighted mean is based on the market value of the contributing products and is justified because it accounts for the differences in production 
volume and prices of the contributing products within one ISIC class.
''')


#Get data from exiobase
exio_df = get_data_exio()
#Exiobase only filters in an expander bar
exio_expander = col3.expander ('Select perspective, GHG Intensity type, and mean type') #Creating expander conainer in column 3
perspective_list = exio_df['Perspective'].loc[exio_df['ISIC 4'] == ISIC4].unique()  #Getting list of perspectives (Consumer / Producer)
perspective = exio_expander.selectbox('Perspective', perspective_list, index = 1) #Creating a radio button with the two perrspectives

# ISIC4 = "3510:Electric power generation, transmission and distribution"
# perspective = 'Producer'
type_list = exio_df['Type'].loc[(exio_df['Perspective'] == perspective) & (exio_df['ISIC 4'] == ISIC4)].unique() #Getting list of GHG Emission intensity type (Mass / Monetary)
types = exio_expander.selectbox('Type of GHG Intensity', type_list, index = 0)  #Creating a radio button with the two GHG intensity types

mean_type_list = exio_df['Mean'].loc[(exio_df['Type'] == types) & (exio_df['Perspective'] == perspective) & (exio_df['ISIC 4'] == ISIC4)].unique() #Getting list of calculated means (Weighted mean / Normal Mean)
mean_type = exio_expander.selectbox('What type of average?', mean_type_list, index = 0)  #Creating a radio button with the two means

region_list = exio_df['Region'].loc[exio_df['Mean'] == mean_type].unique() #Getting list of Exiobase Regions
region = exio_expander.multiselect('Select Region(s)', region_list  , region_list)  #Creating a multiselect box for exiobase regions

col3.write ('#### Table of Selected Data ')
# Selected data for EXIOBASE. Done by the ISIC 4 level filter chosen
selected_data_exio= exio_df[ (exio_df['ISIC 4']== ISIC4) & 
                       (exio_df['Perspective']== perspective) &
                       (exio_df['Type']== types) &
                       (exio_df['Mean']== mean_type) &
                       (exio_df.Region.isin(region))].copy()



#Data dimensions of selected data
col3.write('Data Dimension: ' + str(selected_data_exio.shape[0]) + 
          ' rows and ' + str(selected_data_exio.shape[1]) + 
          ' columns')

col3.dataframe(selected_data_exio.loc[:, ['Region', 'ISIC 4',
                                          'Value', 
                                          'Perspective', 
                                          'Type', "World Region"]])

col3.write ('Showcasing ' + str(types) + ' Intensity with ' + str(perspective) + ' Perspective by ' + str(mean_type))
col3.markdown (""" **How to interpret the table** \n
This table shows the given GHG intensity for a ISIC code from the Input-Output-Analysis, using data from Exiobase. 
The perspective “Consumer” shows emission values of products as they are consumed in a certain region or country 
(including import and excluding exports) while the perspective “Producer” shows the regional production. 
The monetary intensity shows the GHG emissions in kg CO2/€ while the physical intensity shows GHG emissions in kg CO2/ kg of product. T
he geographical scope encompasses individual countries as well as political entities, such as the EU27, or geographic regions, such as Africa.""" )
#Barchart
col3.write ('#### GHG Intensity of product and services by region ')

fig, ax = plt.subplots(figsize=(20,7))

#Create df for barchart, exclude values of aggregated regions to be plotted as lines
barchart_df = selected_data_exio[(selected_data_exio['Region'] != 'EU27') &
                                 (selected_data_exio['Region'] != 'AsiaPacific') &
                                 (selected_data_exio['Region'] != 'Americas') &
                                 (selected_data_exio['Region'] != "Europe including EU27") &
                                 (selected_data_exio['Region'] != 'Africa') &
                                 (selected_data_exio['Region'] != 'MiddleEast') &
                                 (selected_data_exio['Region'] != 'GLO') ].copy()                       
                                 
barchart_df.plot.bar('Region', 'Value', width = 1.0, ec = c2, color=c1, ax=ax)

#Plot horizontal lines of GLOBAL and EU Values
if "GLO" in selected_data_exio.Region.values :
    plt.axhline(y=float(selected_data_exio.loc[selected_data_exio['Region'] == 'GLO', 'Value']) , color = 'r', linewidth = '3', label = 'Global' ) #horizontal line for GLO Value
if "Europe including EU27" in selected_data_exio.Region.values :
    plt.axhline(y=float (selected_data_exio.loc[selected_data_exio['Region'] == 'Europe including EU27', 'Value']) , color = 'b', linewidth = '3', label = 'Europe' )#horizontal line for EU Value
label = selected_data_exio ['ISIC 4'].iloc[0]
title_boxplot = 'ISIC: ' +str(label) 
ax.grid(axis="y", color="w", linewidth=1.5)
ax.set_facecolor(plot_bg)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
#ax.legend(loc = 0, frameon = False,) #not needed
plt.suptitle('')

plt.xticks(fontsize =20)
plt.yticks(fontsize =20)

plt.legend ( fontsize = 15)
#Unit label
if types == 'Physical Mass':
    ulabel = 'CO2eq / Kg'
elif types == 'Physical Mass':
    ulabel = 'CO2eq / Kg'
else:
    ulabel = 'CO2eq / Euros'
plt.ylabel(ulabel, fontsize = 20) #Unit label
# plt.xlabel(fontsize = 20)
#plt.savefig('barchart_exio.png')
col3.pyplot(plt)

#Download button

# btn3 = col3.download_button(
#         label="Download plot",
#         data=plt,
#         file_name="barchart_exio.png",
#         mime="image/png"
#       )   
plt.close()
  
col3.markdown ('The barchart showcases the '+ str(mean_type)+ ' Emission ' + str(types) + ' Intensity (' + str(ulabel) + ') data from a ' + str(perspective) + 
               """ Perspective of the selected ISIC code by country. 
               The chart also shows the Global and European value. 
               
               """)
if "GLO" in selected_data_exio.Region.values :
    col3.write('The global value is: ' +  str("{:.2f}".format(float(selected_data_exio.loc[selected_data_exio['Region'] == 'GLO', 'Value']))) +" " + str(ulabel) ) 
if "Europe including EU27" in selected_data_exio.Region.values :
    col3.write('The european value is: ' +  str("{:.2f}".format(float(selected_data_exio.loc[selected_data_exio['Region'] ==  'Europe including EU27', 'Value'])) )+" " +str(ulabel))
#Boxplot by region
col3.write ('#### Boxplot GHG Instensity of product and services by World region ')
region_boxplot_df = barchart_df

#Duplicate EU values to be able to plot EU 27 and EUROPE, including EU27
EU_df =region_boxplot_df [region_boxplot_df ["World Region"].isin(['EU27, Europe including EU27', 'Europe including EU27'])  ] #Create df of all Europe (no distinction)
EU_df.replace(to_replace ='EU27, Europe including EU27', value = 'Europe, including EU27' , inplace = True) #Changing name to Europe
EU_df.replace(to_replace ='Europe including EU27', value = 'Europe, including EU27' , inplace = True) #Changing name to Europe
region_boxplot_df.replace(to_replace ='EU27, Europe including EU27', value = 'EU27' , inplace = True) #Changing name to EU27
region_boxplot_df = region_boxplot_df[region_boxplot_df['World Region'] != 'Europe including EU27'] #keep only EU27 values
region_boxplot_df2=pd.concat([region_boxplot_df , EU_df]) # merge DFs and creat one with duplicated values for countries in both EU27 and Europe

#Plotting
region_boxplot = boxplot (region_boxplot_df2, ["Value"], ["World Region"])
plt.xlabel(ulabel, fontsize = 20) #Unit label
#plt.savefig('boxplot_exio.png')
col3.pyplot(region_boxplot)   

#Download button
# btn = col3.download_button(
#         label="Download plot",
#         data=region_boxplot,
#         file_name="boxplot_exio.png",
#         mime="image/png"
#         )
plt.close() 
#Comment on boxplot
col3.write ('The boxplot summarizes Emission ' + str(types) + ' Intensity (' + str(ulabel) + ') from a ' + str(perspective) + ' Perspective calculated by ' + str(mean_type)+ 
            " data of the selected ISIC code level differentiating between World Regions. The range of the data stems from country level variabilities within the same region. " )

#Descirptive statistics
col3.write ('###### Descriptive statistics of boxplot ')

#calculating descriptive statistics
descriptive_statistics = region_boxplot_df["Value"].describe()

#putting results in pandas dataframe
descriptive_statistics_df = pd.DataFrame(descriptive_statistics.iloc[1:])

#formatting dataframe for better visuals and understanding
descriptive_statistics_df = descriptive_statistics_df.rename(index={"mean": "Mean",
                                                                    "std": "Standard deviation",
                                                                    "min": "Minimum",
                                                                    "25%": "Lower quartile",
                                                                    "50%": "Median",
                                                                    "75%": "Upper quartile",
                                                                    "max": "Maxmimum"})

#displaying results on dashboard
col3.write(descriptive_statistics_df)





# col3.write(EU_df)



