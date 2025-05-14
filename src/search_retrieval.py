"""Streamlit app for book searching and adding books to the personal library."""

import time
import streamlit as st
import pandas as pd

from helpers import get_books, save_book_form

st.header("Book Search and retrieval 🔍")


if 'df_books' not in st.session_state:
    st.session_state.df_books = pd.DataFrame()
    st.session_state.selected_row = int()

#get book categories from csv
book_categories = pd.read_csv("data/categories.csv")
book_categories = book_categories.sort_values(by='Category')
st.subheader("Search Book and Add to Library")
with st.expander("Search Book and Add to Library"):
    with st.form("Search book by title"):
        col1, col2 = st.columns(2)
        col3,col4 = st.columns([0.9,0.1])

        search_title = col1.text_input('Search By Book Title', key='book_title')
        search_author = col2.text_input('Search By Author', key='author_search')
        button_search = col4.form_submit_button('Search')

    if button_search:
        st.session_state.df_books = pd.DataFrame()
        st.session_state.selected_row = int()

        st.session_state.df_books = get_books.search_api_by_title(search_title, search_author)

    if not st.session_state.df_books.empty:

        #show search results and let user select which book to add to library
        st.subheader("Search Results")
        st.write("Select a book to add to your library")

        df_books_selected = st.dataframe(
            st.session_state.df_books[["title", "author", "synopsis","pageNumbers", "categories"]],
                                        column_config={"title": "Title", "author": "Author",
                                                       "pageNumbers": "Pages",
                                                       "categories": "Categories",
                                                       "synopsis": "Synopsis"},
                                        column_order=("title", "author", "pageNumbers",
                                                      "categories", "synopsis"),
                                        on_select="rerun",
                                        selection_mode="single-row",
                                        hide_index=True,
                                        use_container_width=True)

        if df_books_selected.selection.rows != []:
            selected_index = df_books_selected.selection.rows[0]
            selected_book = st.session_state.df_books.iloc[selected_index]

            #check if category in book_categories
            if not selected_book['categories'] == []:
                if not selected_book['categories'] in book_categories['Category'].values:
                    #if not in book_categories write it to csv and reload book_categories
                    new_category = pd.DataFrame({'Category': selected_book['categories']})
                    new_category.to_csv("data/categories.csv", mode='a', header=False, index=False)
                    book_categories = pd.read_csv("data/categories.csv")
                    book_categories = book_categories.sort_values(by='Category')

            with st.form("Add book to library"):
                title = st.text_input("Title", value=selected_book['title'])
                author = st.text_input("Author", value=selected_book['author'])
                pages = st.number_input("Page Numbers", value=selected_book['pageNumbers'])
                categories = st.multiselect("Categories", options=book_categories,
                                            default=selected_book['categories'])
                synopsis = st.text_area("Synopsis", value=selected_book['synopsis'],disabled=True)
                button_save = st.form_submit_button('Add Book to the Library')

                if button_save:
                    save_book_form.save_book_form(title, author, pages, categories, synopsis)
    else:
        st.write('No books found.')

st.subheader("Create Book and Add to Library")
with st.expander("Create new book to add to your library"):
    with st.form("Create and Add book to library"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        page_number = st.number_input("Page Numbers")
        genre = st.multiselect("Categories", options=book_categories)
        synopsis = st.text_area("Synopsis")
        button_save = st.form_submit_button('Add Book to the Library')

        if button_save:
            save_book_form.save_book_form(title, author, page_number, genre, synopsis)
