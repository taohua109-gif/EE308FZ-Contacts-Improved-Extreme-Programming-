# Contact Management System

A modern, web-based contact management application built with Python Flask backend and responsive HTML/CSS/JavaScript frontend.

## Features

- **Contact Management**: Add, edit, delete, and view contacts
- **Search Functionality**: Real-time search across all contact fields
- **Sorting Options**: Sort by name or category with ascending/descending order
- **Starred Contacts**: Mark important contacts with star indicators
- **Export to Excel**: Export contact list to Excel format
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Instant feedback with toast notifications

## Technology Stack

### Backend
- **Framework**: Python Flask
- **Database**: SQLite
- **Libraries**: pandas, openpyxl (for Excel export)

### Frontend
- **Framework**: Bootstrap 5
- **Styling**: Custom CSS with Inter font
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JS for API interactions

## Project Structure

```
Assignment 1 - Contacts Improved/
├── App.py                 # Main Flask application
├── database.py            # Database operations and SQLite management
├── contacts.db            # SQLite database file
├── templates/
│   └── index.html         # Main frontend interface
├── Blog.md               # Project documentation
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Steps

1. **Clone or download the project**
   ```bash
   # Navigate to the project directory
   cd "Assignment 1 - Contacts Improved"
   ```

2. **Create and activate virtual environment** (recommended)
   For Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ``` 
   For macOS/Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors pandas openpyxl
   ```

4. **Initialize the database**
   - The database will be automatically created on first run
   - Existing `contacts.db` file will be used if present

5. **Run the application**
   ```bash
   python App.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/contacts` | Get all contacts |
| POST | `/contacts` | Add a new contact |
| PUT | `/contacts/<first_name>/<last_name>` | Update a contact |
| DELETE | `/contacts/<first_name>/<last_name>` | Delete a contact |
| PUT | `/contacts/<first_name>/<last_name>/star` | Toggle starred status |
| GET | `/contacts/export` | Export contacts to Excel |

## Usage

### Adding a Contact
1. Click the "Add Contact" button
2. Fill in the contact details (first and last name are required)
3. Click "Save" to add the contact

### Editing a Contact
1. Click the "Edit" button on any contact
2. Modify the contact information
3. Click "Save" to update

### Searching Contacts
- Use the search box to filter contacts by any field
- Search is case-insensitive and works in real-time

### Sorting Contacts
- Use "Sort by Name" or "Sort by Category" buttons
- Click again to toggle between ascending/descending order

### Exporting Contacts
- Click "Export to Excel" to download all contacts as an Excel file
- The exported file includes all contact fields with formatted columns

## Database Schema

The application uses a SQLite database with the following table structure:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    category TEXT,
    phone_number TEXT,
    email TEXT,
    address TEXT,
    institution TEXT,
    is_starred INTEGER DEFAULT 0,
    UNIQUE(first_name, last_name)
);
```

## Development

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Include docstrings for classes and functions
- Maintain consistent indentation (4 spaces)

### File Organization
- Backend logic in `App.py` and `database.py`
- Frontend templates in `templates/` directory
- Static assets loaded via CDN

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes as part of a software engineering assignment.

## Author

Created by Jiayao Hu