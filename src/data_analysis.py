
"""Streamlit app to visualise book ratings and genres with ECharts pie charts."""

from datetime import datetime
import os
import math
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
import altair as alt

# --------------------
# Title and Setup
# --------------------
st.header("Insights 📈")


# --------------------------------------
# PART 1 : Reading Goal Progress
# --------------------------------------


# File paths
BOOKFILE = "data/book.csv"
GOALFILE = "data/reading_goals.csv"

# Load books
try:
    books_df = pd.read_csv(BOOKFILE)
except FileNotFoundError:
    st.error(f"📁 `{BOOKFILE}` not found. Please add a book to your library and add the finishing date")
    st.stop()

# Convert Finishdate to datetime
books_df["Finishingdate"] = pd.to_datetime(books_df["Finishingdate"], errors="coerce")

# Current year
current_year = datetime.now().year
books_this_year = books_df[books_df["Finishingdate"].dt.year == current_year]
books_count = len(books_this_year)

# Check if goal file exists
if not os.path.exists(GOALFILE):
    st.warning(f"📁 `{GOALFILE}` not found. Reading goal unavailable. Please add a reading goal.")
    st.title(f"📚 Books Finished in {current_year}")
    st.metric(label="Books Read", value=books_count)
    st.stop()

# Load reading goals
goals_df = pd.read_csv(GOALFILE)

# Check if goal for current year exists
goal_row = goals_df[goals_df["year"] == current_year]

if goal_row.empty:
    st.warning(f"No reading goal found for {current_year} in `{GOALFILE}`. Please set a goal.")
    st.title(f"📚 Books Finished in {current_year}")
    st.metric(label="Books Read", value=books_count)
    st.stop()

# Get goal
goal = int(goal_row.iloc[0]["goal"])
percentage = min(books_count / goal, 1.0)

#Books read per month
books_this_year['month'] = books_this_year['Finishingdate'].dt.month
books_per_month = books_this_year.groupby('month').size().reset_index(name='books_read')
#average number of books read per month
books_average_per_month = math.floor(books_per_month['books_read'].mean())

#average pages read per month
pages_per_month = books_this_year.groupby('month')['PageNumbers'].sum().reset_index()
pages_average_per_month = math.floor(pages_per_month['PageNumbers'].mean())

# Display progress
card1, card2 = st.columns(2)
st.subheader(f"Reading Progress for {current_year}")
card1.metric(label="Books Read", value=books_count)
card1.metric(label="Goal", value=goal)
st.progress(percentage, text=f"{books_count}/{goal} books ({int(percentage*100)}%)")
card2.metric(label='Average Books Read per Month', value=books_average_per_month)
card2.metric(label='Average Pages Read per Month', value=pages_average_per_month)


# --------------------------------------
# PART 2 : Visualisation by categories   
# --------------------------------------

# Load CSV
base_dir = os.path.dirname(os.path.abspath(__file__))  # path to src/
data_path = os.path.join(base_dir, "..", "data", "book.csv")
df = pd.read_csv(data_path)

# --------------------
# Define Colour Palette (soft pastels + grey for 'Not Rated')
# --------------------
pastel_colors = [
    "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
    "#E4C1F9", "#F6D6AD", "#C1E1C1", "#FDE2E4", "#DADFF7",
    "#D3D3D3"  # light grey for 'Not Rated'
]

# --------------------
# Sidebar Controls
# --------------------
st.sidebar.header("Chart Settings")
view_mode = st.sidebar.radio("Breakdown by:", ["Genre", "Rating"], index=0)

include_unrated = True
if view_mode == "Rating":
    include_unrated = st.sidebar.checkbox("Include 'Not Rated' books", value=True)

# --------------------
# Data Preparation
# --------------------
if view_mode == "Genre":
    genre_counts = df["Genre"].value_counts().reset_index()
    genre_counts.columns = ["label", "count"]
    breakdown = genre_counts
    chart_title = "Books by Genre"

else:
    # Fill missing or blank ratings
    df["rating_display"] = df["Personal_Rating"].fillna("Not Rated").replace("", "Not Rated")

    if include_unrated:
        rating_series = df["rating_display"]
        chart_title = "Books by Rating (including Not Rated)"
    else:
        rating_series = df[df["rating_display"] != "Not Rated"]["rating_display"]
        chart_title = "Books by Rating (excluding Not Rated)"

    rating_counts = rating_series.astype(str).value_counts().sort_index().reset_index()
    rating_counts.columns = ["label", "count"]
    breakdown = rating_counts

# --------------------
# Pie Chart Configuration
# --------------------
chart_options = {
    "color": pastel_colors,
    "title": {"text": chart_title, "left": "center"},
    "tooltip": {"trigger": "item"},
    "legend": {"orient": "vertical", "left": "left"},
    "series": [
        {
            "name": view_mode,
            "type": "pie",
            "radius": "60%",
            "data": [
                {"value": int(row["count"]), "name": str(row["label"])}
                for _, row in breakdown.iterrows()
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            },
            "animation": True,
            "animationDurationUpdate": 800,
            "animationEasingUpdate": "cubicOut"
        }
    ]
}


# --------------------
# Display Chart
# --------------------
st.subheader(f"{view_mode} Distribution")
st_echarts(options=chart_options, height="500px", key="pie_chart")

# --------------------------------------
# PART 3 : Rating Trends per Author
# --------------------------------------

st.subheader("📊 Rating Trends per Author")

# Filter out rows with missing ratings or authors
rating_df = df[["Authors", "Personal_Rating"]].dropna()

# Convert rating to string (Altair works better for categorical axes)
rating_df["Personal_Rating"] = rating_df["Personal_Rating"].astype(str)

# Count of ratings per author
rating_counts = (
    rating_df.groupby(["Authors", "Personal_Rating"])
    .size()
    .reset_index(name="count")
)

# Create Altair chart
chart = alt.Chart(rating_counts).mark_bar().encode(
    x=alt.X("Personal_Rating:N", title="Rating"),
    y=alt.Y("count:Q", title="Number of Books"),
    color="Authors:N",
    tooltip=["Authors:N", "Personal_Rating:N", "count:Q"]
).properties(
    
    width=600,
    height=400
)

# Display in Streamlit
st.altair_chart(chart, use_container_width=True)
