import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from sklearn import linear_model

if "graph_mode" not in st.session_state:
    st.session_state["graph_mode"] = "Mean"


def mode_change():
    if st.session_state["graph_mode"] == "Mean":
        st.session_state["graph_mode"] = "Median"
    else:
        st.session_state["graph_mode"] = "Mean"


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

st.title("LLM Prototype Evaluation Dashboard")

# top-level filters
model_filter = st.selectbox("Select the model", pd.unique(df["model"]))
model_df = df[df["model"] == model_filter]

# single-element container
placeholder = st.empty()

mean_df = df[["model", "temperature", "top_p", "top_k", "repetition", "max_length",
              "coherency", "fluency"]].groupby("model").mean()

avg_coherency = mean_df.loc[model_filter]["coherency"]
avg_fluency = mean_df.loc[model_filter]["fluency"]

whole_coherency = np.mean(mean_df["coherency"])
whole_fluency = np.mean(mean_df["fluency"])

with placeholder.container():
    # create three columns
    coherency, fluency = st.columns(2)

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

    st.markdown(f"### Detailed {model_filter} View")
    st.dataframe(model_df, use_container_width=True)

    hyperparameter = st.selectbox("Select a hyperparameter", df.columns[2:7])

    if st.session_state["graph_mode"] == "Mean":
        hyperparameter_df = df[["model", hyperparameter, "fluency", "coherency"]].groupby(
            ["model", hyperparameter]).mean().reset_index().sort_values(by=hyperparameter)
    else:
        hyperparameter_df = df[["model", hyperparameter, "fluency", "coherency"]].groupby(
            ["model", hyperparameter]).median().reset_index().sort_values(by=hyperparameter)
    # create two columns for charts
    fig_fluency, fig_coherency = st.columns(2)

    with fig_fluency:
        st.markdown(f"### How {hyperparameter} impacts fluency ({st.session_state['graph_mode']})")
        fig = px.line(
            data_frame=hyperparameter_df, x=hyperparameter, y="fluency", markers=True, color="model"
        )

        st.write(fig)

    with fig_coherency:
        st.markdown(f"### How {hyperparameter} impacts coherency ({st.session_state['graph_mode']})")

        fig = px.line(
            data_frame=hyperparameter_df, x=hyperparameter, y="coherency", markers=True, color="model"
        )
        st.write(fig)
    st.button('Toggle Average', on_click=mode_change, use_container_width=True)

    fig_corr1, fig_corr2, df_perfect = st.columns(3)
    with fig_corr1:
        st.markdown(f"### Model correlation matrix")
        corr = model_df[["fluency", "coherency"]].corr()
        fig = px.imshow(corr, text_auto=True)
        st.write(fig)

    with fig_corr2:
        st.markdown(f"### Overall correlation matrix")
        corr = df[["fluency", "coherency"]].corr()
        fig = px.imshow(corr, text_auto=True)
        st.write(fig)

    with df_perfect:
        st.markdown(f"### Perfect Outputs")
        perfect_df = df[df["fluency"] == 10]
        perfect_df = perfect_df[perfect_df["coherency"] == 10]
        st.dataframe(perfect_df, use_container_width=True)

    fluency_reg, coherency_reg = st.columns(2)

    models = dict()
    for model in df["model"].unique():
        models[model] = dict()
        model_normalised_df = df[df["model"] == model]
        models[model]["x"] = model_normalised_df[["temperature", "top_p", "top_k", "repetition", "max_length"]].values
        models[model]["fluency"] = model_normalised_df["fluency"].values
        models[model]["coherency"] = model_normalised_df["coherency"].values

    reg = linear_model.LinearRegression()
    with fluency_reg:
        st.markdown(f"### Fluency Regression")
        for i in models:
            st.write(f"{i} Regression Results")
            reg.fit(models[i]["x"], models[i]["fluency"])
            st.write(pd.DataFrame(
                {"Coefficient": reg.coef_,
                 "Intercept": reg.intercept_
                 }, index=["temperature", "top_p", "top_k", "repetition", "max_length"]))

    with coherency_reg:
        st.markdown(f"### Coherency Regression")
        for i in models:
            st.write(f"{i} Regression Results")
            reg.fit(models[i]["x"], models[i]["coherency"])
            st.write(pd.DataFrame(
                {"Coefficient": reg.coef_,
                 "Intercept": reg.intercept_
                 }, index=["temperature", "top_p", "top_k", "repetition", "max_length"]))
