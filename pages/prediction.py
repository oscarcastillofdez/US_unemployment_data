import streamlit as st
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score
from prophet import Prophet

from Utils import queries
from Utils import charts
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

def create_model_variables(data, value):

    data["lag1"] = data[value].shift(1)
    data["lag2"] = data[value].shift(2)
    data["lag3"] = data[value].shift(3)
    data["lag6"] = data[value].shift(6)
    data["lag9"] = data[value].shift(9)
    data["lag12"] = data[value].shift(12)
    data["lag15"] = data[value].shift(15)
    data["lag18"] = data[value].shift(18)
    data["lag21"] = data[value].shift(21)
    data["lag24"] = data[value].shift(24)


    data = data.dropna()

    X = data[["lag1","lag2","lag3","lag6","lag9","lag12","lag15","lag18","lag21","lag24"]]
    Y = data[value]

    return X, Y
    
def predict_ahead(model, history, months):

    history = list(history.values)

    prediction = []

    for i in range(months):
        lag1 = history[-1]
        lag2 = history[-2]
        lag3 = history[-3]
        lag6 = history[-6]
        lag9 = history[-9]
        lag12 = history[-12]
        lag15 = history[-15]
        lag18 = history[-18]
        lag21 = history[-21]
        lag24 = history[-24]

        entrada = [[lag1, lag2, lag3, lag6, lag9, lag12, lag15, lag18, lag21, lag24]]
        pred = model.predict(entrada)[0]

        history.append(pred)

        prediction.append(pred)
    
    return prediction

def predict(model, data, value, months):

    Y = data[value]

    prediction = predict_ahead(model, Y, months)
    
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=months+1, freq="M")[1:]
    full_index = data.index.append(future_dates)

    target_len = len(full_index)

    if len(prediction) < target_len:
        padding = [None] * (target_len - len(prediction))
        prediction = padding + list(prediction)
    else:
        prediction = list(prediction)

    if len(Y) < target_len:
        Y = list(Y) + [None] * (target_len - len(Y))
    else:
        Y = list(Y)

    return pd.DataFrame({
        "Prediction": prediction, 
        "Real": Y
    }, index=full_index)

def create_linear_regresion_model(data, value):

    X, y = create_model_variables(data, value)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = LinearRegression()

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    scores = cross_val_score(model, X, y, cv=kf, scoring='r2')

    #st.write("Scores per fold:", scores)
    #st.write("Average:", scores.mean())

    model.fit(X_train, y_train)
    #st.write("Score on the test set: ",  model.score(X_test, y_test))

    return model

####################################################################################################################################

config_page.config()

all_data = queries.get_all_data()
all_data["Date"] = pd.to_datetime(all_data["Date"], format="%Y-%m")


national_data = all_data.groupby("Date")[["Non-Institutional Population", "Labor Force", "Employment", "Unemployment"]].sum()

national_data["Unemployment Rate"] = national_data["Unemployment"] / national_data["Labor Force"]
national_data["State/Area"] = "Total"
national_data = national_data.reset_index()

state_data  = all_data[["Date", "State/Area","Non-Institutional Population", "Labor Force", "Employment", "Unemployment", "Unemployment Rate"]]

rates_data = pd.concat([state_data, national_data])
rates_data["Employment Rate"] = rates_data["Employment"] / rates_data["Non-Institutional Population"]
rates_data = rates_data[["Date", "State/Area", "Employment Rate", "Unemployment Rate"]]


state = st.selectbox("State", list(rates_data.reset_index()["State/Area"].unique()))

rates_data = rates_data.set_index("State/Area")
data = rates_data.loc[state]
precovid_data = data[data["Date"] < "2020-01-01"]

data = data.set_index("Date")
precovid_data = precovid_data.set_index("Date")

unemployment_rate_model = create_linear_regresion_model(precovid_data, "Unemployment Rate")
employment_rate_model = create_linear_regresion_model(precovid_data, "Employment Rate")

ur_pred = predict(unemployment_rate_model, data, "Unemployment Rate", 24)
er_pred = predict(employment_rate_model, data, "Employment Rate", 24)

ur_pred = ur_pred.reset_index()
er_pred = er_pred.reset_index()


data = data.reset_index()

st.write("## Unemployment Rate")
charts.prediction_chart(ur_pred, "index", "Real", "Prediction", color_A="#B31942", color_B="#0A3161")
st.write("## Employment Rate")
charts.prediction_chart(er_pred, "index", "Real", "Prediction")

#linear_regresion_test(national_data)
#prophet_test(national_data)

# Continua con la regresión lineal, separa por los datos de población, u cosas así

    

