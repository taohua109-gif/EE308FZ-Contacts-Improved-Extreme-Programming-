

# Code Style Guide

This document outlines the coding standards and conventions used in the Contact Management System project.

## Python Code Style

### General Guidelines
- Follow **PEP 8** standards
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **79 characters**
- Use meaningful, descriptive variable names
- Write docstrings for all functions, classes, and modules

### Naming Conventions
```python
# Classes: PascalCase
class ContactManager:
    pass

# Functions and variables: snake_case
def add_contact():
    contact_data = {}

# Constants: UPPER_CASE
MAX_CONTACTS = 1000
```

### Imports Order
```python
# Standard library imports
import json
import sqlite3

# Third-party imports
from flask import Flask, request, jsonify
import pandas as pd

# Local application imports
from database import Database
```

### Function Documentation
```python
def add_contact(contact_data):
    """
    Add a new contact to the database.
    
    Args:
        contact_data (dict): Dictionary containing contact information
            - first_name (str): Contact's first name
            - last_name (str): Contact's last name
            - phone_number (str): Contact's phone number
            - email (str): Contact's email address
            - address (str): Contact's physical address
    
    Returns:
        bool: True if contact was added successfully, False otherwise
    """
    # Function implementation
    pass
```

### Error Handling
```python
try:
    # Database operation
    cursor.execute(sql_query, parameters)
    conn.commit()
except sqlite3.Error as e:
    print(f"Database error: {e}")
    return False
finally:
    if conn:
        conn.close()
```

## HTML/CSS/JavaScript Style

### HTML Structure
- Use semantic HTML5 elements
- Proper indentation (2 spaces)
- Include appropriate ARIA labels
- Use Bootstrap classes for styling

```html
<div class="container">
    <header class="header">
        <h1>Contact Management System</h1>
    </header>
    
    <main class="main-content">
        <!-- Content here -->
    </main>
</div>
```

### CSS Guidelines
- Use meaningful class names
- Follow BEM methodology for complex components
- Organize styles logically
- Use CSS variables for theming

```css
.contact-item {
    border: 1px solid #e9ecef;
    padding: 1rem;
    margin-bottom: 1rem;
}

.contact-item--starred {
    background-color: #fff3cd;
    border-color: #ffeaa7;
}

.contact-item__name {
    font-weight: bold;
    font-size: 1.2rem;
}
```

### JavaScript Conventions
- Use modern ES6+ features
- Prefer `const` and `let` over `var`
- Use arrow functions for callbacks
- Handle errors properly

```javascript
// Async/await for API calls
async function loadContacts() {
    try {
        const response = await fetch('/contacts');
        const contacts = await response.json();
        displayContacts(contacts);
    } catch (error) {
        console.error('Failed to load contacts:', error);
        showError('Failed to load contacts');
    }
}

// Event handling
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});
```

## Database Design Standards

### Table Naming
- Use plural nouns for table names: `contacts`
- Use snake_case for column names: `first_name`, `phone_number`

### SQL Formatting
```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(first_name, last_name)
);
```

## File Organization

### Project Structure
```
project/
├── App.py              # Main application entry point
├── database.py         # Database operations
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html
└── static/            # Static assets (CSS, JS, images)
    ├── css/
    ├── js/
    └── images/
```

### Code Organization within Files
1. Imports section
2. Constants and configuration
3. Class definitions
4. Function definitions
5. Main application logic
6. If __name__ == "__main__" block

## Testing Standards

### Test Structure
```python
import unittest
from App import app

class TestContactAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_add_contact(self):
        response = self.app.post('/contacts', json={
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, 201)
```

## Documentation Standards

### Inline Comments
- Use comments to explain "why" not "what"
- Keep comments up to date with code changes
- Remove commented-out code before committing

### README Documentation
- Include setup instructions
- Document API endpoints
- Provide usage examples
- Include troubleshooting section

## Git Commit Messages

Follow conventional commit format:
```
feat: add contact search functionality
fix: resolve duplicate contact validation
docs: update API documentation
style: format Python code according to PEP8
```

## Code Review Checklist

- [ ] Code follows established style guidelines
- [ ] Functions are properly documented
- [ ] Error handling is implemented
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Tests pass successfully
- [ ] Documentation updated if needed

## Performance Best Practices

### Database Optimization
- Use parameterized queries to prevent SQL injection
- Create indexes for frequently searched columns
- Close database connections properly

### Frontend Optimization
- Minimize DOM manipulations
- Use event delegation for dynamic content
- Implement lazy loading for large datasets

### API Design
- Use appropriate HTTP status codes
- Implement pagination for large datasets
- Cache frequently accessed data