import streamlit as st
import pandas as pd
import  requests
from streamlit import session_state as ss
from plotly import graph_objects as go
from plotly import express as px
from datetime import datetime, timedelta

### Session state inicializations ####
if "power_status" not in ss:
    ss.power_status = pd.DataFrame()

if "last_worked_status" not in ss:
    ss.last_worked_status = pd.DataFrame()

if "metric_status" not in ss:
    ss.metric_status = []

if "last_update_work" not in ss:
    ss.last_update_work = datetime.now()

#### Functions ####
def updPowerStatus():
    response = requests.get("http://10.21.31.5:40649/api/dashboard/power-status")
    ss["power_status"] = pd.concat([ss["power_status"], pd.DataFrame(response.json()["power_status"])], ignore_index=True)

def updLastWorkedStatus():
    response = requests.get("http://10.21.31.5:40649/api/dashboard/last-worked-status")
    df = pd.DataFrame(response.json()["last_worked_status"],columns=["Machine","Time"])
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")  # Convert to datetime
    df["Time"] = df["Time"].dt.tz_localize(None) # remove timezone
    ss["last_worked_status"] = df
    ss["last_update_work"] = datetime.now()

def assignSection(row): # assign machines to sections
    # parse pandas datetime to python datetime
    py_time = row["Time"].to_pydatetime() if not pd.isna(row["Time"]) else None
    # extract start_time and endtime as timedelta
    start_time, end_time = ss["time_range"]
    start_delta = timedelta(minutes=start_time)
    end_delta = timedelta(minutes=end_time)

    # get ranges in datetime
    start_range = ss["last_update_work"] - start_delta
    end_range = ss["last_update_work"] - end_delta

    # machine never worked => end_time
    if py_time is None:
        return f">{end_time}"
    elif py_time > start_range:
        return f"<{start_time}"
    elif py_time < end_range:
        return f">{end_time}"
    else:
        # get section size and the time machine has not worked for
        total_range = abs((start_delta - end_delta).total_seconds())
        section_size = total_range / 4  #Split range into 4 equal sections
        elapsed_time = abs((ss["last_update_work"] - py_time).total_seconds())

        # Drink 2 redbulls and write this variable section size assigner
        if elapsed_time <= section_size:
            return f"[{start_time},{start_time + section_size / 60:.0f}]"
        elif elapsed_time <= 2 * section_size:
            return f"[{start_time + section_size / 60:.0f},{start_time + 2 * section_size / 60:.0f}]"
        elif elapsed_time <= 3 * section_size:
            return f"[{start_time + 2 * section_size / 60:.0f},{start_time + 3 * section_size / 60:.0f}]"
        else:
            return f"[{start_time + 3 * section_size / 60:.0f},{end_time}]"
        # who let me cook


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

@st.fragment(run_every=5)
def logStatus():
    response = requests.get("http://10.21.31.5:40649/log")
    if response.json()["status"]:
        logs = response.json()["log"]
    else:
        logs = []
    for row in logs:
        st.write(f"{row[0][4:-4]}: {row[1]}")

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
col1, col2 = st.columns([2,1])

# Power status
with col1:
    powerStatus()

# Last Worked Status
with col2:
    updLastWorkedStatus() # get fresh data
    # Configuration sliders n such
    st.slider(
        "Select Time Range in minutes",
        min_value=0,
        max_value=59,
        value=(0,59),
        key="time_range"
    )
    c1, c2 = st.columns(2)
    c1.checkbox("Include beyond boundary values", key="include_boundaries")
    c2.button("Update data",on_click=updLastWorkedStatus)

    # Graph data
    df = ss["last_worked_status"] 
    # axis 1 applies to each column (0 to index)
    df["Range"] = df.apply(assignSection, axis=1)
    if not ss["include_boundaries"]:
        # just removes rows where <min_range and >max_range is in column range
        df_filtered = df[~df["Range"].isin([f"<{ss["time_range"][0]}", f">{ss["time_range"][1]}"])]
    else:
        df_filtered = df
    # counts number of machiens, reset_index so pd doesnt cry
    pie_data = df_filtered["Range"].value_counts().reset_index() 
    pie_data.columns = ["Range", "Count"]

    pie_chart = px.pie(
        pie_data,
        names="Range",
        values="Count",
        title="Last Time Machine Worked Distribution",
        color="Range"
    )
    st.plotly_chart(pie_chart) # plot that shit

col1, col2 = st.columns(2)
with col1:
    logStatus()

# Metrics Status
# metricsStatus()
