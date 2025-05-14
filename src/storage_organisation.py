"""
Book Manager · Storage & Organisation  (single-user CSV edition, fixed)
-----------------------------------------------------------------------
• Catalogue: books_mock_dataset.csv                 (read-only)
• Personal data: books_user_data.csv                (Title | Personal_Rating | Startingdate | Finishingdate | Review)
"""

import os
from helpers import reading_goals
from datetime import date, datetime
import csv
import pandas as pd
import streamlit as st
import time
from streamlit_star_rating import st_star_rating


# Initialize session state to store the current goal
if 'current_goal' not in st.session_state:
    st.session_state.current_goal = None
if 'filtered_books' not in st.session_state:
    st.session_state.filtered_books = None
if 'is_filtered' not in st.session_state:
    st.session_state.is_filtered = False
if 'reset' not in st.session_state:
    st.session_state.reset = False

# title
st.header("Book Storage and Organisation 📚")

# Sidebar for reading goal management
with st.sidebar:
    st.subheader("📖 Reading Goal")

    # Get current year
    current_year = datetime.now().year
    reading_goals.manage_reading_goal(current_year)


# Load your CSV database
USER_DATA_PATH = "data/book.csv"
books = pd.read_csv("data/book.csv")
book_categories = books['Genre']





# --- Search Form ---
with st.expander("Search your Library", expanded=False):
    reset = st.button("Clear Filters")
    if reset:
        st.session_state.filtered_books = books
        st.session_state.is_filtered = False
        st.session_state.author_input = ""
        st.session_state.genre_input = "All"
        st.session_state.keyword_input = ""
    with st.form("search_form"):
        st.subheader("📋 Search your Library ")

        # Genre selector with unique genres from the data
        author_input = st.text_input("Author name", key='author_input')
        genre_options = ["All"] + book_categories.unique().tolist()
        selected_genre = st.selectbox("Genre", genre_options, key='genre_input')
        keyword = st.text_input("Keyword in the title", key='keyword_input')

        # Page number filters
        #min_pages = int(books["Pages"].min())
        #max_pages = int(books["Pages"].max())
        #pages_range = st.slider("Number of Pages", min_pages, max_pages, (min_pages, max_pages))

        # Date range filter
        #min_date = df["Finishing Date"].min()
        #max_date = df["Finishing Date"].max()
        #date_range = st.date_input("Finishing Date Range", (min_date, max_date))

        submitted = st.form_submit_button("Search")


if submitted:
    filtered_books = books.copy()

     # Search by keyword in Title or Description
    if keyword:
        filtered_books = filtered_books[
            filtered_books["Title"].str.contains(keyword, case=False, na=False) |
            filtered_books.get("Synopsis", pd.Series([""] * len(filtered_books))).str.contains(keyword, case=False, na=False)
        ]

    # Filter by author
    if author_input:
        filtered_books = filtered_books[
            filtered_books["Authors"].str.contains(author_input, case=False, na=False)
        ]

    # Filter by genre
    if selected_genre != "All":
        filtered_books = filtered_books[filtered_books["Genre"] == selected_genre]

    # Filter by page count
    #filtered_books = filtered_books[
    #    (filtered_books["Pages"] >= pages_range[0]) & (filtered_books["Pages"] <= pages_range[1])
    #]

    # Filter by finishing date range
    #filtered_books = filtered_books[
    #    (filtered_books["Finishing Date"] >= pd.to_datetime(date_range[0])) &
    #    (filtered_books["Finishing Date"] <= pd.to_datetime(date_range[1]))
    #]
    st.session_state.filtered_books = filtered_books
    st.session_state.is_filtered = True

if st.session_state.is_filtered == False:
    st.session_state.filtered_books = books

if st.session_state.filtered_books is not None:
    if st.session_state.is_filtered == True:
        st.subheader("📖 Search Results")
    else:
        st.subheader("📖 Your Books")

    selected_books = st.dataframe(st.session_state.filtered_books,
                                        column_config={"PageNumbers": "Pages", "Personal_Rating": "Rating", "Startingdate": "Start Date", "Finishingdate": "Finish Date"},
                                        column_order=("Title", "Authors", "PageNumbers", "Genre", "Personal_Rating","Startingdate","Finishingdate","Synopsis"),
                                        on_select="rerun",
                                        selection_mode="single-row",
                                        hide_index=True,
                                        use_container_width=True)
    st.caption(f"{len(st.session_state.filtered_books)} book(s) found.")


    if selected_books.selection.rows != []:
        selected_index = selected_books.selection.rows[0]
        st.session_state.selected_index = selected_index  # Save it in session
        selected_book = st.session_state.filtered_books.iloc[selected_index]



    if selected_books.selection.rows != []:
        # ---------- 6 · Book selector ----------
        title = selected_book['Title']
        # auto‑clear rating widget when the title changes
        if "active_title" not in st.session_state:
            st.session_state.active_title = title
        elif st.session_state.active_title != title:
            st.session_state.pop(f"rating_{st.session_state.active_title}", None)
            st.session_state.active_title = title

        if title:
            row = books.loc[books["Title"] == title].iloc[0]

            # catalogue details (read‑only)
            st.subheader("Book details")
            st.markdown(f"**Title:** {row.get('Title')}")
            st.markdown(f"**Author:** {row.get('Authors')}")
            st.markdown(f"**Pages:** {int(row.get('PageNumbers')) if pd.notna(row.get('PageNumbers')) else '-'}")
            st.markdown(f"**Synopsis:** {row.get('Synopsis')}" or "_No synopsis available._")


            # personal rating with right‑aligned clear link
            custom_css = """
            [data-baseweb="rating"]{display:flex;align-items:center;}
            [data-baseweb="rating"] [data-baseweb="button"]{margin-left:0.75rem;}
            """
            personal_rating = st_star_rating(
                label="Personal rating",
                maxValue=5,
                defaultValue=int(row["Personal_Rating"]) if pd.notna(row["Personal_Rating"]) else 0,
                key=f"rating_{title}",
                size=40,
                # resetButton=True,
                # resetLabel="clear",
                customCSS=custom_css,
            )


            # dates
            c1, c2 = st.columns(2)
            start_date = c1.date_input(
                "📅 Starting date",
                value=pd.to_datetime(row["Startingdate"]).date()
                if pd.notna(row["Startingdate"]) else date.today(),
                format="DD.MM.YYYY",
                key=f"start_{title}",
            )
            finish_date = c2.date_input(
                "🏁 Finishing date",
                value=pd.to_datetime(row["Finishingdate"]).date()
                if pd.notna(row["Finishingdate"]) else date.today(),
                format="DD.MM.YYYY",
                key=f"finish_{title}",
            )

            # review
            review = st.text_area(
                "✏️ Your review",
                value=str(row["Review"]) if pd.notna(row["Review"]) else "",
                height=150,
                key=f"review_{title}",
            )

            st.divider()

            button_col1, button_col2 = st.columns([0.8,0.2])
            # save button
            if button_col1.button("💾 Save all details", type="secondary"):
                entry = {
                    "Title": title,
                    "Personal_Rating": personal_rating,
                    "Startingdate": start_date.isoformat(),
                    "Finishingdate": finish_date.isoformat(),
                    "Review": review,
                }

                if title in books["Title"].values:
                    books.loc[books["Title"] == title, entry.keys()] = entry.values()
                else:
                    books = pd.concat([books, pd.DataFrame([entry])], ignore_index=True)

                # -------- write / update book.csv --------
                books.to_csv(
                    USER_DATA_PATH,
                    index=False,
                    quoting=csv.QUOTE_MINIMAL,
                    lineterminator="\n",
                    encoding="utf-8",
                )
                st.session_state.filtered_books = books
                st.success("Personal details saved.")
                time.sleep(2)
                st.rerun()

            #delete button
            if button_col2.button("Delete Book from Library", type="primary"):
                if title in books["Title"].values:
                    books = books.loc[books["Title"] != title]
                    # -------- write / update book.csv --------
                    books.to_csv(
                        USER_DATA_PATH,
                        index=False,
                        quoting=csv.QUOTE_MINIMAL,
                        lineterminator="\n",
                        encoding="utf-8",
                    )
                    st.session_state.filtered_books = books
                    st.success("Book successfully deleted.")
                    time.sleep(2)
                    st.rerun()

                else:
                    st.warning("Something went wrong when trying to delete the book.")







