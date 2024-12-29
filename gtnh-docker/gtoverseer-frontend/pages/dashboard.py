import streamlit as st
import pandas as pd
import  requests
from streamlit import session_state as ss
from plotly import graph_objects as go

### Session state inicializations ####
if "power_status" not in ss:
    ss.power_status = pd.DataFrame()

if "last_worked_status" not in ss:
    ss.last_worked_status = pd.DataFrame()

if "metric_status" not in ss:
    ss.metric_status = []

#### Functions ####
def updPowerStatus():
    response = requests.get("http://10.21.31.5:40649/api/dashboard/power-status")
    ss["power_status"] = pd.concat([ss["power_status"], pd.DataFrame(response.json()["power_status"])], ignore_index=True)

# @st.cache_data
# def updLastWorkedStatus():
#     response = requests.get("http://10.21.31.5:40649/api/dashboard/last-worked-status")
#     ss["last_worked_status"] = pd.concat([ss["last_worked_status"], pd.DataFrame(response.json())], ignore_index=True)

# @st.cache_data
# def updMetricStatus():
#     response = requests.get("http://10.21.31.5:40649/api/dashboard/metric-status")
#     ss["metric_status"].append(response.json())


### Body functions ###
@st.fragment(run_every=1)
def powerStatus():
    updPowerStatus()
    X = tuple(range(0,len(ss["power_status"])))
    chart = go.Figure() # Graph class
    # Power usage line
    chart.add_trace(
        go.Scatter(
            x=X,
            y=ss["power_status"][0],
            mode="lines",
            name="Power Usage",
            yaxis="y1",
            line={"color":"blue"}
        )
    )
    # Current power storage line
    chart.add_trace(
        go.Scatter(
            x=X,
            y=ss["power_status"][1],
            mode="lines",
            name="Current Power Storage",
            yaxis="y2",
            line={"color":"red"}
        )
    )
    # 
    chart.update_layout(
        title="Power Status",
        yaxis={
            "title":"Power Usage [EU]",
            "titlefont":{"color":"blue"},
            "tickfont":{"color":"blue"}
        },
        yaxis2={
            "title":"Power Storage [EU]",
            "titlefont":{"color":"red"},
            "tickfont":{"color":"red"},
            "anchor":"x",
            "overlaying":"y1",
            "side":"right"
        },
        legend={"orientation":"h"}
    )
    st.plotly_chart(chart)
    #st.write(ss["power_status"])

# @st.fragment(run_every=5)
# def lastWorkedStatus():
#     updLastWorkedStatus()
#     st.write(ss["last_worked_status"])

# @st.fragment(run_every=5)
# def metricsStatus():
#     updMetricStatus()
#     st.write(ss["last_worked_status"])

#### Body ####
## Backlog info message print ##
if ss.backlog_message != "":
    st.toast(ss.backlog_message)
    ss.backlog_message = ""

## Header ##
st.write("# Dashboard")
col1, col2, col3 = st.columns(3)

# Power status
with col1:
    powerStatus()

# Last Worked Status
# lastWorkedStatus()

# Metrics Status
# metricsStatus()

