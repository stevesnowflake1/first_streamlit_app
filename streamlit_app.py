import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 

streamlit.title('My parents New Healthy Dinner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smothie')
streamlit.text('🐔Hard-Boiled & Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New Section to display fruitivice response
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)

# create the repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Normalie Json
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
#New Section to display fruitivice api response

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    # Display nornalized result as a table
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
# my_data_row = my_cur.fetchone()
# my_data_rows = my_cur.fetchall() # get all data rows
# streamlit.text("Hello from Snowflake:")
streamlit.text("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
# Add a button to load the fruit
if streamlit.button('Get Fruit Load First'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list() # get all data rows
    streamlit.dataframe(my_data_rows) 
#streamlit.text(my_data_row)
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_rows)
# don't run anything past here while we troubleshoot
streamlit.stop()
streamlit.write('This should not run')

# Allow end user to add fruit to the list
add_my_fuit = streamlit.text_input('What fruit would you like to add?','')
streamlit.write('Thank you for adding ', add_my_fuit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")


