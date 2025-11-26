import altair as alt
import streamlit as st

def good_point_chart(df, x, y, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_point(size=100, color="#0A3161", filled=True, opacity=1).encode(
        x=alt.X(x+":N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format=y_format), 
                scale=alt.Scale())
    ) + alt.Chart(df).mark_line(color="#0A3161", strokeDash=[5,5], opacity=0.6).encode(
        x=x,
        y=y
    ) 

    st.altair_chart(chart, use_container_width=True)

def blue_line_chart(df, x, y, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_line(color="#0A3161", opacity=1).encode(
        x=alt.X(x+":T", axis=alt.Axis(labelColor="#0A3161",  title=None), sort=sort_order),
        y=alt.Y(y, axis=alt.Axis(labelColor="#0A3161",  title=None, format=y_format), 
                scale=alt.Scale())
    )

    st.altair_chart(chart, use_container_width=True)

def red_line_chart(df, x, y, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_line(color="#B31942", opacity=1).encode(
        x=alt.X(x+":T", axis=alt.Axis(labelColor="#B31942", title=None), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#B31942",  title=None, format=y_format), 
                scale=alt.Scale())
    )

    st.altair_chart(chart, use_container_width=True)

def red_area_chart(df, x, y, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_area(color="#B31942", opacity=1).encode(
        x=alt.X(x+":T", axis=alt.Axis(labelColor="#B31942", title=None), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#B31942",  title=None, format=y_format), 
                scale=alt.Scale())
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


def bar_multi_chart(df, x, y, multi_color, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x+":N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format=y_format)),
        color = multi_color 
    )

    st.altair_chart(chart, use_container_width=True)

def point_multi_chart(df, x, y, multi_color, sort_order = None, y_format = ".0f"):

    chart = alt.Chart(df).mark_point(size=100, color="#0A3161", filled=True, opacity=1).encode(
        x=alt.X(x+":N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format=y_format), 
                scale=alt.Scale()),
        color = multi_color
    ) + alt.Chart(df).mark_line(color="#0A3161", strokeDash=[5,5], opacity=0.6).encode(
        x=alt.X(x+":N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=sort_order),
        y=alt.Y(y+":Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format=y_format), 
                scale=alt.Scale()),
        color = multi_color
    ) 
    st.altair_chart(chart, use_container_width=True)

def prediction_chart(df, x, y_real, y_predict, sort_order = None, y_format = "%", color_A = "#0A3161", color_B = "#B31942"):

    chart = alt.Chart(df).mark_line(color=color_A, opacity=1).encode(
        x=alt.X(x+":T", axis=alt.Axis(labelColor=color_A, title=None), sort=sort_order),
        y=alt.Y(y_real+":Q", axis=alt.Axis(labelColor=color_A,  title=None, format=y_format), 
                scale=alt.Scale())
    ) + alt.Chart(df).mark_line(color=color_B, opacity=1).encode(
        x=alt.X(x+":T", axis=alt.Axis(labelColor=color_B, title=None), sort=sort_order),
        y=alt.Y(y_predict+":Q", axis=alt.Axis(labelColor=color_B,  title=None, format=y_format), 
                scale=alt.Scale()))

    st.altair_chart(chart, use_container_width=True)