# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)


name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_string = ''
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = (' ').join(ingredients_list)    

    time_to_insert = st.button('Submit Order')

    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients,name_on_order) 
    values ('{ingredients_string}','{name_on_order}')
    """
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
