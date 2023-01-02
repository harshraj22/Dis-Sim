import streamlit as st
import sqlite3

DB_NAME = './db/monitor.db'
TABLE_NAME = 'monitor'

def get_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT avg_pixel FROM {TABLE_NAME}")
    data = c.fetchall()
    conn.close()
    return data

st.set_page_config(page_title = "Analytics")
st.markdown("Analytics About the Average Pixel Value of Images")
# st.sidebar.markdown("Analytics")

# st.altair_chart(get_data())

st.line_chart(get_data())


st.markdown(f"Grafana Dashboard (Localhost): [Here](http://localhost:3000/)")
