"""
Module defining the Book class.

This module provides a class to represent a book with attributes such as 
ID, title, author, synopsis, page count, and categories. It is used to 
create book objects for easier handling and organization of book data.
"""

class Book:
    """
    A class to represent a book.

    Attributes:
        id (str): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author(s) of the book.
        synopsis (str): A brief description or synopsis of the book.
        pageCount (int): The number of pages in the book.
        categories (list): A list of categories or genres associated with the book.
    """
    def __init__(self, id, title, author, synopsis, page_count, categories):
        self.id = id
        self.title = title
        self.author = author
        self.synopsis = synopsis
        self.page_count = page_count
        self.categories = categories