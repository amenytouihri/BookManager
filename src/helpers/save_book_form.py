import streamlit as st
import pandas as pd
import time

def save_book_form(title, author, page_number, genre, synopsis):
    csv_file = "data/book.csv"
    new_book = {
        "Title": title,
        "Authors": author,
        "PageNumbers": page_number,
        "Genre": ", ".join(genre) if isinstance(genre, list) else genre,
        "Synopsis": synopsis
    }
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Title", "Authors", "PageNumbers" "Genre", "Synopsis"])

    df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.success("Book saved successfully!")