import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorrites')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale Spinach & Rocket Smoothy')
streamlit.text('Hard Boiled Free Range Egg')
streamlit.text('Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#New Section to display fruitvice api response
#import requests
streamlit.header('Fruityvise Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
  else:
#streamlit.write('The user entered', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
    
#import snowflake.connector
streamlit.header("View Our Fruit List - Add Your Favorites!:")
#Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
#Add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#Allow the end user to add fruits to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
def insert_row_snowflake(add_my_fruit):
  with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('" + add_my_fruit +"')")
      return "Thanks for adding " + add_my_fruit
  

if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    my_cnx.close()
  
streamlit.write('Thanks for adding a fruit to our list ' + add_my_fruit)
