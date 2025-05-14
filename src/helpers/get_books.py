"""Module to fetch books from the Google Books API."""
import pandas as pd
import requests
from helpers import book_class



#get data from google books api
#AIP endpoint
URL = "https://www.googleapis.com/books/v1"

#API key
API_KEY = "AIzaSyBe8SW2oq29wsGcorUhryuVFPtX6Pxz8qg"


#make request
#fields needed:
#items (array)
#--id (string)
#--volumeInfo (object)
#----title (string)
#----authors (array)
#----description (string)
#----pageCount (int)
#----categories (array)


def search_api_by_title(title, author):
    """
    Fetch books from the Google Books API based on title and author.

    Args:
        title (str): The title of the book to search for.
        author (str): The author of the book to search for.

    Returns:
        pd.DataFrame: A DataFrame containing the following columns:
            - id (str): The unique ID of the book.
            - title (str): The title of the book.
            - author (str): The author(s) of the book, joined as a single string.
            - synopsis (str): The description or synopsis of the book.
            - pageNumbers (int): The number of pages in the book.
            - categories (list): A list of categories or genres for the book.
        If no books are found, an empty DataFrame is returned.
        If the API request fails, the HTTP status code is returned.
    """
    get_response = requests.get(f"{URL}/volumes?q=intitle:{title}+inauthor:{author}&maxResults=20&key={API_KEY}",
                                timeout=300)
    if get_response.status_code == 200:
        get_response_json = get_response.json()
        books = pd.DataFrame(columns=['id', 'title', 'author', 'synopsis','pageNumbers', 'categories'])
        if 'items' not in get_response_json:
            return pd.DataFrame(columns=['id', 'title', 'author', 'synopsis','pageNumbers', 'categories'])
        else:
            for item in get_response_json['items']:
                if 'authors' in item['volumeInfo']:
                    author = ", ".join(item['volumeInfo']['authors'])
                else:
                    author = ""
                if 'description' in item['volumeInfo']:
                    synopsis = item['volumeInfo']['description']
                    # if type(synopsis) == tuple():
                    #     synopsis = synopsis[0]
                else:
                    synopsis = ""
                if 'categories' in item['volumeInfo']:
                    categories = item['volumeInfo']['categories']
                else:
                    categories = []
                if 'pageCount' in item['volumeInfo']:
                    page_count = item['volumeInfo']['pageCount']
                else:
                    page_count = 0

                if 'title' in item['volumeInfo']:
                    title = item['volumeInfo']['title']
                else:
                    title = ""
                # create book object
                book_object = book_class.Book(item['id'], title, author,
                                             synopsis, page_count, categories=categories)

                # add book object to dataframe
                books.loc[len(books)] = [book_object.id,
                                         book_object.title,
                                         book_object.author,
                                         book_object.synopsis,
                                         book_object.page_count,
                                         book_object.categories]

    else:
        return get_response.status_code
    books = books[books['title'] != ""]
    return books
