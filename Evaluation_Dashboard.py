import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np


def read_csv():
    try:
        data = pd.read_csv("evaluation.csv", header=0)
    except OSError:
        data = pd.DataFrame()
    return data


df = read_csv()

st.set_page_config(
    page_title="Evaluation Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title("Persona Chat Evaluation Dashboard")

# top-level filters
model_filter = st.selectbox("Select the model", pd.unique(df["model"]))

# single-element container
placeholder = st.empty()

mean_df = df[["model", "temperature", "top_p", "top_k", "repetition", "max_length", "informativeness",
              "coherency", "fluency"]].groupby("model").mean()

avg_coherency = mean_df.loc[model_filter]["coherency"]
avg_fluency = mean_df.loc[model_filter]["fluency"]
avg_informativeness = mean_df.loc[model_filter]["informativeness"]

whole_coherency = np.mean(mean_df["coherency"])
whole_fluency = np.mean(mean_df["fluency"])
whole_informativeness = np.mean(mean_df["informativeness"])

with placeholder.container():
    # create three columns
    coherency, fluency, informativeness = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    coherency.metric(
        label="Coherency",
        value=avg_coherency,
        delta=avg_coherency - whole_coherency,
        help="out of 10.0"
    )

    fluency.metric(
        label="Fluency",
        value=avg_fluency,
        delta=avg_fluency - whole_fluency,
        help="out of 10.0"
    )

    informativeness.metric(
        label="Informativeness",
        value=avg_informativeness,
        delta=avg_informativeness - whole_informativeness,
        help="out of 10.0"
    )
    st.markdown(f"### Detailed {model_filter} View")
    st.dataframe(df, use_container_width=True)

    hyperparameter = st.selectbox("Select a hyperparameter", df.columns[1:6])

    hyperparameter_df = df[["model", hyperparameter, "fluency", "coherency", "informativeness"]].groupby(
        ["model", hyperparameter]).mean().reset_index().sort_values(by=hyperparameter)
    df = df[(df["model"] == model_filter)]
    # create two columns for charts
    fig_fluency, fig_coherency, fig_inform = st.columns(3)
    with fig_fluency:
        st.markdown(f"### How {hyperparameter} impacts fluency")

        fig = px.line(
            data_frame=hyperparameter_df, x=hyperparameter, y="fluency", markers=True, color="model"
        )
        st.write(fig)

    with fig_coherency:
        st.markdown(f"### How {hyperparameter} impacts coherency")

        fig = px.line(
            data_frame=hyperparameter_df, x=hyperparameter, y="coherency", markers=True, color="model"
        )
        st.write(fig)

    with fig_inform:
        st.markdown(f"### How {hyperparameter} impacts informativeness")

        fig = px.line(
            data_frame=hyperparameter_df, x=hyperparameter, y="informativeness", markers=True, color="model"
        )
        st.write(fig)
