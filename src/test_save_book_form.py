import pytest
import pandas as pd

from helpers import save_book_form

# Test function to check if the book is saved correctly
def test_typical():
    title = "Test Book"
    author = "Test Author"
    pages = 100
    categories = ["Fiction", "Adventure"]
    synopsis = "This is a test book."

    # Call the function to save the book
    save_book_form.save_book_form(title, author, pages, categories, synopsis)

    # Read the CSV file to check if the book was saved correctly
    df = pd.read_csv("data/book.csv")

    # Check if the book exists in the DataFrame
    assert any(df["Title"] == title)



# Test function to check if the book is saved correctly with different data types
def test_edge_case():
    title = "Test Book Edge Case"
    author = "Test Author"
    pages = "100"
    categories = ["Fiction", "Adventure"]
    synopsis = "This is a test book."

    # Call the function to save the book
    save_book_form.save_book_form(title, author, pages, categories, synopsis)

    # Read the CSV file to check if the book was saved correctly
    df = pd.read_csv("data/book.csv")

    # Check if the book exists in the DataFrame
    assert any(df["Title"] == title)

# Test function to check if the function raises an error
def test_raises():
    with pytest.raises(TypeError):
        title = "Test Raising error"
        author = "Test Author"
        pages = 100
        categories = ["Fiction", "Adventure"]
        synopsis = "This is a test book."

        # Call the function to save the book
        save_book_form.save_book_form(title, author, pages, categories)