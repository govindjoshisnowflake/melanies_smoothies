# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smootie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smootie
    """
)


name_on_order=st.text_input("Name on smoothie")
st.write("The name on your smoothie will be ",name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredient_list=st.multiselect('select 5 ingredients',my_dataframe,max_selections=5)

if ingredient_list:
    ingredients_string=''   

    for each_fruit in ingredient_list:
        ingredients_string += each_fruit + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
         
        st.text(ingredients_string)

     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER )
            values ('""" + ingredients_string + "','" + name_on_order + """')"""

     #st.write(my_insert_stmt)
     time_to_insert=st.button("Submit Order!")
     if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + name_on_order +'!', icon="✅")
