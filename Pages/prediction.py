import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from prophet import Prophet
from Utils import queries
from Utils import config_page

def create_prophet_model(df):
    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=48, freq="M")
    pred = model.predict(future)
    
    pred_df = pred[["ds","yhat","yhat_lower","yhat_upper"]].set_index("ds")

    df = df.set_index("ds")
    pred_df["real"] = df["y"]

    return pred_df

def prophet_test(data: pd.DataFrame):

    nip_pred = create_prophet_model(data.drop(columns=["Labor Force", "Employment", "Unemployment"]).rename(columns={"Date":"ds","Non-Institutional Population":"y"}))
    lf_pred = create_prophet_model(data.drop(columns=["Employment", "Non-Institutional Population", "Unemployment"]).rename(columns={"Date":"ds","Labor Force":"y"}))
    employment_pred = create_prophet_model(data.drop(columns=["Labor Force", "Non-Institutional Population", "Unemployment"]).rename(columns={"Date":"ds","Employment":"y"}))
    unemployment2_pred = create_prophet_model(data.drop(columns=["Labor Force", "Non-Institutional Population", "Employment"]).rename(columns={"Date":"ds","Unemployment":"y"}))

    unemployment_pred = pd.DataFrame()
    unemployment_pred["Date"] = nip_pred.reset_index()["ds"]
    unemployment_pred["yhat"] = data["Date"]
    unemployment_pred = unemployment_pred.set_index("Date")
    unemployment_pred["yhat"] = lf_pred["yhat"] - employment_pred["yhat"]
    unemployment_pred["yhat_upper"] = lf_pred["yhat_lower"] - employment_pred["yhat_lower"]
    unemployment_pred["yhat_lower"] = lf_pred["yhat_upper"] - employment_pred["yhat_upper"]
    unemployment_pred["real"] = data.reset_index().rename(columns={"Date":"ds","Unemployment":"y"}).set_index("ds")["y"]

    st.subheader("Predicción de población no institucionalizada")
    st.line_chart(nip_pred)
    st.subheader("Predicción de población activa")
    st.line_chart(lf_pred)
    st.subheader("Predicción de población empleada")
    st.line_chart(employment_pred)
    st.subheader("Predicción de población desempleada (en base a las gráficas anteriores)")
    st.line_chart(unemployment_pred)
    st.subheader("Predicción de población desempleada (predicción directa)")
    st.line_chart(unemployment2_pred)
    
def predict_ahead(data, prediction, model, months):

    historico = list(data["Value"].values)

    for i in range(months):
        lag1 = historico[-1]
        lag2 = historico[-2]
        lag3 = historico[-3]
        lag6 = historico[-6]
        lag9 = historico[-9]
        lag12 = historico[-12]

        entrada = [[lag1, lag2, lag3, lag6, lag9, lag12]]
        pred = model.predict(entrada)[0]

        historico.append(pred)

        prediction.append(pred)
    
    return prediction


def create_linear_regresion_model(data):

    data["lag1"] = data["Value"].shift(1)
    data["lag2"] = data["Value"].shift(2)
    data["lag3"] = data["Value"].shift(3)
    data["lag6"] = data["Value"].shift(6)
    data["lag9"] = data["Value"].shift(9)
    data["lag12"] = data["Value"].shift(12)


    data = data.dropna()

    X = data[["lag1","lag2","lag3","lag6","lag9","lag12"]]
    y = data["Value"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)


    y_pred = model.predict(X)

    months = 480

    predicction = predict_ahead(data, list(y_pred), model, months)
    
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=months+1, freq="M")[1:]  # meses futuros
    full_index = data.index.append(future_dates)

    df_pred = pd.DataFrame({
        "Predicción": predicction, 
        "Real": y
        
    }, index=full_index)

    return df_pred

def linear_regresion_test(data: pd.DataFrame):

    data = data.set_index("Date")

    
    data["Unemployment Rate"] = data["Unemployment"] / data["Labor Force"]
    unemployment_rate_pred = create_linear_regresion_model(data.drop(columns=["Labor Force", "Employment", "Unemployment", "Non-Institutional Population"]).rename(columns={"Unemployment Rate":"Value"}))
    employment_pred = create_linear_regresion_model(data.drop(columns=["Labor Force", "Unemployment", "Non-Institutional Population", "Unemployment Rate"]).rename(columns={"Employment":"Value"}))
    nip_pred = create_linear_regresion_model(data.drop(columns=["Labor Force", "Unemployment", "Employment", "Unemployment Rate"]).rename(columns={"Non-Institutional Population":"Value"}))
    lf_pred = create_linear_regresion_model(data.drop(columns=["Unemployment", "Employment", "Non-Institutional Population", "Unemployment Rate"]).rename(columns={"Labor Force":"Value"}))
    unemployment_pred2 = create_linear_regresion_model(data.drop(columns=["Labor Force", "Employment", "Non-Institutional Population", "Unemployment Rate"]).rename(columns={"Unemployment":"Value"}))

    unemployment_pred = pd.DataFrame()
    unemployment_pred["Date"] = nip_pred.index
    unemployment_pred["Predicción"] = nip_pred.index
    unemployment_pred = unemployment_pred.set_index("Date")
    unemployment_pred["Predicción"] = lf_pred["Predicción"] - employment_pred["Predicción"]
    unemployment_pred["Real"] = lf_pred["Real"] - employment_pred["Real"]


    st.subheader("Predicción de población no institucionalizada")
    st.line_chart(nip_pred)
    st.subheader("Predicción de población activa")
    st.line_chart(lf_pred)
    st.subheader("Predicción de población empleada")
    st.line_chart(employment_pred)
    st.subheader("Predicción de población desempleada")
    st.line_chart(unemployment_pred)
    st.subheader("Predicción de población desempleada directa")
    st.line_chart(unemployment_pred2)
    st.subheader("Predicción de población porcentaje desempleada")
    st.line_chart(unemployment_rate_pred)

####################################################################################################################################

config_page.config()


#data = queries.get_unemployment_data()
#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m")

national_data = queries.get_national_totals()
national_data["Date"] = pd.to_datetime(national_data["Date"], format="%Y-%m")

linear_regresion_test(national_data)
prophet_test(national_data)




# Continua con la regresión lineal, separa por los datos de población, u cosas así

    

