import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


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

hyperparameter = st.selectbox("Select the displayed hyperparameter", df.columns[1:6])
evaluation = st.selectbox("Select the displayed evaluation", df.columns[-3:])

# single-element container
placeholder = st.empty()

og_df=df
df=df[(df["model"] == model_filter)]



#  live feed simulation
for seconds in range(100):
    avg_coherency = np.mean(df["coherency"])
    avg_fluency = np.mean(df["fluency"])
    avg_informativeness = float((df.shape[0] / 100) * df[(df["informativeness"] == "True")].shape[0])

    whole_coherency=np.mean(og_df["coherency"])
    whole_fluency = np.mean(og_df["fluency"])
    whole_informativeness = float((df.shape[0] / 100) * og_df[(og_df["informativeness"] == "True")].shape[0])


    with placeholder.container():
        # create three columns
        coherency, fluency, informativeness = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        coherency.metric(
            label="Coherency",
            value=avg_coherency,
            delta=avg_coherency-whole_coherency,
            help="out of 10.0"
        )

        fluency.metric(
            label="Fluency",
            value=avg_fluency,
            delta=avg_fluency - whole_coherency,
            help="out of 10.0"
        )

        informativeness.metric(
            label="Informativeness",
            value=avg_informativeness,
            delta=avg_informativeness - whole_informativeness,
            help="out of 100.0"
        )

        # create two columns for charts
        fig_col1, model_comparison = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")

            fig = px.line(
                data_frame=df, y=hyperparameter, x=evaluation
            )
            st.write(fig)

        with model_comparison:
            st.markdown("### Model Comparison")
            fig2 = px.histogram(
                data_frame=df, y=hyperparameter, x=evaluation
            )
            st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
