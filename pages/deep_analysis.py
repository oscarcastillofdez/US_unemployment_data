import streamlit as st
import pandas as pd
import altair as alt
from Utils import queries
from Utils import config_page

config_page.config()

all_data = queries.get_all_data()

all_data