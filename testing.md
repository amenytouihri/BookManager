This test suite checks if the save_book_form() function correctly writes book data to a CSV file.

- test_typical() verifies saving with standard input.
- test_edge_case() tests handling of string input for numeric fields.
- test_raises() ensures an error (in our case TypeError) is raised when a required argument is missing.

