import altair as alt
import streamlit as st

def good_line_chart(df, x, y, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_point(size=100, color="#0A3161", filled=True, opacity=1).encode(
        x=alt.X(x+":N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format=y_format), 
                scale=alt.Scale())
    ) + alt.Chart(df).mark_line(color="#0A3161", strokeDash=[5,5], opacity=0.6).encode(
        x=x,
        y=y
    ) 

    st.altair_chart(chart, use_container_width=True)

def good_bar_chart(df, x, y, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x+":N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format=y_format)),
        color=alt.condition(
            alt.datum[y] > 0,
            alt.value("#0A3161"),  
            alt.value("#B31942"))  
    )

    st.altair_chart(chart, use_container_width=True)