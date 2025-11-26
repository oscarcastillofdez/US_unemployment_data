import streamlit as st
import snowflake.connector
import pandas as pd
from Utils import config_page

config_page.config()
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"],
)

cur = conn.cursor()
cur.execute("SELECT CURRENT_TIMESTAMP;")
result = cur.fetchone()

st.write("Hora actual en Snowflake:", result[0])

cur.execute("SELECT * FROM states LIMIT 10;")
df = cur.fetch_pandas_all()
st.dataframe(df)
