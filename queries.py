import psycopg2
import pandas as pd
import streamlit as st


def get_connection():
    return psycopg2.connect(
        host = st.secrets["db_host"],
        port = st.secrets["db_port"],
        database = st.secrets["db_database"],
        user = st.secrets["db_user"],
        password = st.secrets["db_password"],
        sslmode = st.secrets["db_sslmode"]
    )

@st.cache_data()
def make_query(query):
    conn = get_connection()
    return pd.read_sql(query, conn)
    

def get_all_data():
    return make_query(""" 
        SELECT * 
        FROM public.unemployment_data 
            NATURAL JOIN public.state_lookup
            NATURAL JOIN public.calendar_lookup
    """)

def get_unemployment_data():
    return make_query("SELECT * FROM unemployment_data")

def get_state_data():
    return make_query("SELECT * FROM state_lookup")

def get_national_totals():
    return make_query( """
        SELECT "Date", SUM("Non-Institutional Population") as "Non-Institutional Population", 
            SUM("Labor Force") as "Labor Force", 
            SUM("Employment") as "Employment", 
            SUM("Unemployment") as "Unemployment"
        FROM unemployment_data
            GROUP BY "Date"
            ORDER BY "Date"
        
    """)

def get_precovid_totals():
    return make_query( """
        SELECT "Date", SUM("Non-Institutional Population") as "Non-Institutional Population", 
            SUM("Labor Force") as "Labor Force", 
            SUM("Employment") as "Employment", 
            SUM("Unemployment") as "Unemployment"
        FROM unemployment_data
            NATURAL JOIN public.calendar_lookup cl
            WHERE cl."Year" < 2020
            GROUP BY "Date"
            ORDER BY "Date"
        
    """)

def get_latest_data():
    return make_query("""
        "SELECT * 
        FROM PUBLIC.unemployment_data 
        WHERE "Date" IN ( 
            SELECT DISTINCT "Date" 
            FROM PUBLIC.unemployment_data 
            ORDER BY "Date" DESC 
            LIMIT 1 
        );"
    """)

def get_latest_national_data():
    return make_query("""
    SELECT  
       SUM("Non-Institutional Population") as "Non-Institutional Population", 
       SUM("Labor Force") as "Labor Force", 
       SUM("Employment") as "Employment",
       SUM("Unemployment") as "Unemployment"
    FROM unemployment_data
       WHERE "Date" IN ( 
           SELECT DISTINCT "Date" 
           FROM PUBLIC.unemployment_data 
               ORDER BY "Date" DESC 
               LIMIT 1 ); 
    """)

def get_national_average():
    return make_query("""
        WITH national_data AS (
            SELECT
                SUM("Non-Institutional Population") AS nipc,
                SUM("Labor Force") AS lbc,
                SUM("Employment") AS ec,
                SUM("Unemployment") AS uc
            FROM
                unemployment_data ud
            GROUP BY
                "Date"
        )
        SELECT
            AVG(nipc) AS "Non-Institutional Population",
            AVG(lbc) AS "Labor Force",
            AVG(ec) AS "Employment",
            AVG(uc) AS "Unemployment"
        FROM national_data;
    """)

def get_state_average():
    return make_query("""
        SELECT "FIPS Code", st."State/Area", AVG("Non-Institutional Population") as "Non-Institutional Population", 
            AVG("Labor Force") as "Labor Force", 
            AVG("Employment") as "Employment", 
            AVG("Unemployment") as "Unemployment"
        FROM unemployment_data
        NATURAL JOIN public.state_lookup st 
            GROUP BY "FIPS Code", st."State/Area" 
            ORDER BY "FIPS Code"
    """)
def get_average_year():
    return make_query("""
        WITH change AS ( 
            SELECT 
                cl."Year", 
                cl."Month", 
                SUM("Non-Institutional Population") AS nipc, 
                SUM("Labor Force") AS lbc, 
                SUM("Employment") AS ec, 
                SUM("Unemployment") AS uc, 
                SUM("Unemployment Rate") AS urc 
            FROM  
                unemployment_data ud 
            JOIN  
                calendar_lookup cl ON ud."Date" = cl."Date" 
            WHERE  
                cl."Year" < 2020 
            GROUP BY  
                cl."Year", cl."Month" 
        ) 
        SELECT  
            "Month", 
            AVG(nipc) AS "Non-Institutional Population", 
            AVG(lbc) AS "Labor Force", 
            AVG(ec) AS "Employment", 
            AVG(uc) AS "Unemployment", 
            AVG(urc) AS "Unemployment Rate" 
        FROM change 
        GROUP BY "Month" 
    """)
def get_average_change_year():
    return make_query("""
        WITH change AS ( 
            SELECT 
                cl."Year", 
                cl."Month", 
                SUM("Non-Institutional Population")  
                    - LAG(SUM("Non-Institutional Population")) OVER (ORDER BY cl."Year", cl."Month") AS nipc, 
                SUM("Labor Force")  
                    - LAG(SUM("Labor Force")) OVER (ORDER BY cl."Year", cl."Month") AS lbc, 
                SUM("Employment")  
                    - LAG(SUM("Employment")) OVER (ORDER BY cl."Year", cl."Month") AS ec, 
                SUM("Unemployment")  
                    - LAG(SUM("Unemployment")) OVER (ORDER BY cl."Year", cl."Month") AS uc, 
                SUM("Unemployment Rate")  
                    - LAG(SUM("Unemployment Rate")) OVER (ORDER BY cl."Year", cl."Month") AS urc 
            FROM  
                unemployment_data ud 
            JOIN  
                calendar_lookup cl ON ud."Date" = cl."Date" 
            WHERE  
                cl."Year" < 2020 
            GROUP BY  
                cl."Year", cl."Month" 
        ) 
        SELECT  
            "Month", 
            AVG(nipc) AS "Non-Institutional Population Change", 
            AVG(lbc) AS "Labor Force Change", 
            AVG(ec) AS "Employment Change", 
            AVG(uc) AS "Unemployment Change", 
            AVG(urc) AS "Unemployment Rate Change" 
        FROM change 
        GROUP BY "Month" 
    """)

def get_user_password(user):
    return make_query("""
        SELECT user_password
        FROM users
            WHERE user_name = '""" + user + "'"
    )
     

def get_roles(user):
    return make_query("""
        SELECT role_name 
        FROM users u 
            NATURAL JOIN group_participants gp 
            NATURAL JOIN group_roles gr 
            NATURAL JOIN roles r  
            WHERE user_name = '""" + user + "'" 
    )
     

def get_all_data_tables():
    state_df = make_query("SELECT * FROM state_lookup")
    date_df = make_query("SELECT * FROM calendar_lookup")
    data_df = make_query("SELECT * FROM unemployment_data")
    return state_df, date_df, data_df

def get_all_users_tables():
    user_df = make_query("SELECT * FROM users")
    group_df = make_query("SELECT * FROM groups")
    role_df = make_query("SELECT * FROM roles")
    gp_df = make_query("SELECT * FROM group_participants")
    gr_df = make_query("SELECT * FROM group_roles")
    return user_df, group_df, role_df, gp_df, gr_df


    

