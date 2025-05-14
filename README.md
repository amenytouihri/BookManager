# 📚 Book Manager Software

The **Book Manager Software** is designed to help users organize their library, track their reading progress, and analyze their habits. This tool offers a clean and efficient way to manage their literary life.

## 📌 Overview

**Goals:**
- Simplify book tracking and organization
- Visualize reading performance and preferences
- Encourage consistent reading habits

**Main Features:**
- Add and manage books with full metadata
- Track reading progress and goals
- Filter and search by genre, author, or keyword
- Visualize stats like books per month or average pages read
- Integrate with book APIs for discovery and recommendations


## 📁 Project Structure

```
Bookmanager2/
│
├── src/                            # Source code
│   ├── bookmanager_app.py          # Streamlit app main entry point
│   ├── storage_organisation.py     # Handles storage and organization of book data
│   ├── search_retrieval.py         # Logic for searching and filtering book entries
│   ├── data_analysis.py            # Functions for data visualization and analysis
│   └── helpers/
│           ├── book_class.py        #
│           ├── get_books.py         # API integration and book data retrieval
│           ├── reading_goals.py     # Readging goals functionality
│           └── save_book_form.py    # 
│
├── data/                           # Local data storage
│   ├── book.csv                    # User database of saved books
│   ├── reading_goals.csv           # Yearly reading goals
│   └── categories.csv              # Book categories
│
│── test/
│   ├── testing.md                  # 
│   └── test_save_book_formpy       #
│
│
├── .gitignore                      # Files and folders to ignore in version control
├── CHANGE.md                       # Descriptions of abstractions/ decomposition
├── FORMATTER.md                    # Descriptions of code improvement with pylint
├── LICENSE                         # Project license
├── README.md                       # Project documentation
├── exceptions.md                   #
├── requirements.txt                # Project dependencies
└── roadmap.md                      # Planned features and development goals
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `pip` (Python package installer)

### Installation & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AdvPythonFS25/Bookmanager2
   cd Bookmanager2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run src/bookmanager_app.py
   ```

4. **Open your browser** to `http://localhost:8501` to start using the Book Manager.


## ⚙️ Usage

1. Open the app in your browser at `http://localhost:8501`
2. Use the form to add new books with details (title, author, rating, etc.)
3. View and filter your collection
4. Set a yearly reading goal and monitor progress
5. Explore visual stats on reading trends and preferences


## 👨‍💻 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push and open a pull request

## 🙋 Support

If you encounter any issues or have questions: Open an issue on GitHub

## 📄 License

This project is licensed under the [MIT License](LICENSE).
