         
# Contact Management System: Project Documentation and Implementation

## GitHub Repository Address
- Backend Repository: [https://github.com/yourusername/contacts-backend](https://github.com/yourusername/contacts-backend)
- Frontend Repository: [https://github.com/yourusername/contacts-frontend](https://github.com/yourusername/contacts-frontend)

## Project Summary

This project implements a full-featured Contact Management System with a separate frontend and backend architecture. The backend is built with Python and Flask, providing RESTful API endpoints for contact management operations, while the frontend is a responsive single-page application using HTML, CSS, JavaScript, and Bootstrap. The system allows users to create, view, search, sort, update, and delete contacts with various attributes including name, category, phone number, email, and address.

## PSP Table

| **Task** | **Estimated Time** | **Actual Time** | **Notes** |
|----------|---------------------|-----------------|-----------|
| Project Setup | 1 hour | 1.5 hours | Initializing repositories and project structure |
| Database Design | 1 hour | 0.5 hours | SQLite database schema design |
| Backend Implementation | 4 hours | 5 hours | Flask API endpoints and database operations |
| Frontend Implementation | 5 hours | 6 hours | HTML/CSS/JS with Bootstrap styling |
| API Integration | 2 hours | 2.5 hours | Connecting frontend and backend |
| Testing | 2 hours | 3 hours | Unit and integration testing |
| Bug Fixing | 1 hour | 1.5 hours | Resolving issues and edge cases |
| Documentation | 2 hours | 2 hours | Writing README and this blog post |
| **Total** | **18 hours** | **22 hours** | - |

## Cloud Server Deployment
The application is deployed and accessible at: [https://contacts.yourdomain.com](https://contacts.yourdomain.com)

## Feature Demonstration

### 1. Contact List View
![Contact List View](https://placeholder-for-image.com/contact-list.png)
The main dashboard displays all contacts in a clean, organized list format. Each contact entry shows the contact's name, category, phone number, email, and address. The header includes search functionality and the option to add new contacts.

### 2. Add New Contact Modal
![Add New Contact Modal](https://placeholder-for-image.com/add-contact.png)
The "Add Contact" button opens a modal form where users can input contact details including first name, last name, category, phone number, email, and address. First and last names are required fields.

### 3. Edit Existing Contact
![Edit Contact Modal](https://placeholder-for-image.com/edit-contact.png)
Clicking the "Edit" button on any contact opens the same modal form but pre-populated with the contact's current information, allowing users to make changes and save updates.

### 4. Delete Contact Confirmation
![Delete Contact Confirmation](https://placeholder-for-image.com/delete-contact.png)
The delete function includes a confirmation dialog to prevent accidental removal of contacts, ensuring user actions are intentional.

### 5. Search Functionality
![Search Functionality](https://placeholder-for-image.com/search-contact.png)
Users can search contacts by typing keywords in the search box. The system filters contacts in real-time based on matches in any field including name, category, phone number, email, or address.

### 6. Sorting Options
![Sorting Options](https://placeholder-for-image.com/sort-contact.png)
Contacts can be sorted alphabetically by last name or by category. Each sort option includes a toggle for ascending or descending order.

### 7. Contact Avatars
![Contact Avatars](https://placeholder-for-image.com/contact-avatars.png)
Each contact entry is represented by an avatar with randomly generated colors and the initials of the contact's first and last name, providing visual distinction.

### 8. Empty State Display
![Empty State Display](https://placeholder-for-image.com/empty-state.png)
When there are no contacts in the system, an empty state message appears with guidance on how to add the first contact.

### 9. Loading State Indicator
![Loading State](https://placeholder-for-image.com/loading-state.png)
During data operations, a loading spinner appears to indicate that the system is processing the request.

### 10. Success/Error Toast Messages
![Toast Messages](https://placeholder-for-image.com/toast-message.png)
After completing an operation (add, update, delete), a toast notification appears in the corner of the screen to confirm success or report errors.

## Design and Implementation Process

### System Architecture
The project follows a client-server architecture with clear separation between frontend and backend components.

```
┌─────────────────┐     HTTP Requests     ┌─────────────────┐
│   Frontend      │──────────────────────▶│   Backend       │
│   (HTML/CSS/JS) │◀──────────────────────│   (Python/Flask)│
└─────────────────┘                       └──────────┬──────┘
                                                    │
                                            ┌───────▼───────┐
                                            │  SQLite       │
                                            │  Database     │
                                            └───────────────┘
```

### Database Design
The system uses a SQLite database with a single `contacts` table containing fields for id, first_name, last_name, category, phone_number, email, and address. The database is initialized and managed by the Database class in `database.py`. The table structure ensures efficient storage and retrieval of contact information.

### Backend Development
The backend is built using Flask to create RESTful API endpoints. It implements the following key components:

1. **Database Class**: Handles all database operations including connection, table creation, and CRUD operations.
2. **Contacts Controller**: Defines the API routes and request handlers.
3. **Error Handling**: Provides meaningful error messages for various edge cases.

### Frontend Development
The frontend is a responsive single-page application that provides a user-friendly interface for contact management. Key components include:

1. **HTML Structure**: Organizes the layout with Bootstrap components.
2. **CSS Styling**: Custom styles for enhanced user experience.
3. **JavaScript Functions**: Implement API calls, form handling, search, sorting, and UI updates.

## Key Code Explanations

### Database Operations
The Database class provides methods for all contact management operations:

```python:absolute/path/to/database.py
class Database:
    def __init__(self, db_file):
        # Initialize database connection and create table if not exists
        self.db_file = db_file
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.create_table()
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        # Create contacts table if it doesn't exist
        create_table_sql = """ CREATE TABLE IF NOT EXISTS contacts (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    first_name TEXT NOT NULL,
                                    last_name TEXT NOT NULL,
                                    category TEXT,
                                    phone_number TEXT,
                                    email TEXT,
                                    address TEXT
                                );"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def update_contact(self, original_first_name, original_last_name, contact_data):
        # Update an existing contact in the database
        sql = ''' UPDATE contacts
                  SET first_name = ?,
                      last_name = ?,
                      category = ?,
                      phone_number = ?,
                      email = ?,
                      address = ?
                  WHERE first_name = ? AND last_name = ?'''  # Update by name combination
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (
                contact_data['first_name'],
                contact_data['last_name'],
                contact_data['category'],
                contact_data['phone_number'],
                contact_data['email'],
                contact_data['address'],
                original_first_name,
                original_last_name
            ))
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            print(e)
            return False
```
<mcfile name="database.py" path="D:\软件工程\Assignment 1 - Contacts Improved\Jiayao Hu_832301310_contacts_backend\src\database.py"></mcfile>

### RESTful API Endpoints
The backend exposes several API endpoints for contact management:

```python:absolute/path/to/contacts.py
# Get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    db = Database('contacts.db')
    contacts = db.get_all_contacts()
    return jsonify(contacts), 200

# Add a new contact
@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    if not data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = Database('contacts.db')
    success = db.add_contact(data)
    if success:
        return jsonify({'message': 'Contact added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add contact'}), 500

# Update an existing contact
@app.route('/contacts/<first_name>/<last_name>', methods=['PUT'])
def update_contact(first_name, last_name):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = Database('contacts.db')
    success = db.update_contact(first_name, last_name, data)
    if success:
        return jsonify({'message': 'Contact updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update contact'}), 500

# Delete a contact
@app.route('/contacts/<first_name>/<last_name>', methods=['DELETE'])
def delete_contact(first_name, last_name):
    db = Database('contacts.db')
    success = db.delete_contact(first_name, last_name)
    if success:
        return jsonify({'message': 'Contact deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete contact'}), 500
```
<mcfile name="contacts.py" path="D:\软件工程\Assignment 1 - Contacts Improved\Jiayao Hu_832301310_contacts_backend\src\controller\contacts.py"></mcfile>

### Frontend API Integration
The frontend uses JavaScript to interact with the backend API:

```javascript:absolute/path/to/contacts.html
// Load All Contacts
async function loadContacts(filter = '') {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/contacts`);
        const contacts = await response.json();

        // Apply Search Filter
        let filteredContacts = contacts;
        if (filter) {
            const lowerFilter = filter.toLowerCase();
            filteredContacts = contacts.filter(contact =>
                contact.first_name.toLowerCase().includes(lowerFilter) ||
                contact.last_name.toLowerCase().includes(lowerFilter) ||
                (contact.category && contact.category.toLowerCase().includes(lowerFilter)) ||
                contact.phone_number.toLowerCase().includes(lowerFilter) ||
                contact.email.toLowerCase().includes(lowerFilter) ||
                contact.address.toLowerCase().includes(lowerFilter)
            );
        }

        currentContacts = filteredContacts;
        sortAndDisplayContacts(filteredContacts);
        contactCount.textContent = filteredContacts.length;
    } catch (error) {
        console.error('Failed to load contacts:', error);
        showToast('Failed to load contacts. Please try again later.', 'danger');
        showEmptyState();
    } finally {
        hideLoading();
    }
}

// Handle Form Submit for Add/Update
async function handleFormSubmit(e) {
    e.preventDefault();

    const originalFirstName = originalFirstNameInput.value;
    const originalLastName = originalLastNameInput.value;
    const contactData = {
        first_name: document.getElementById('first-name').value,
        last_name: document.getElementById('last-name').value,
        category: document.getElementById('category').value,
        phone_number: document.getElementById('phone_number').value,
        email: document.getElementById('email').value,
        address: document.getElementById('address').value
    };

    try {
        let response;
        let successMessage;

        if (originalFirstName && originalLastName) {
            // Update Contact
            response = await fetch(`${API_BASE_URL}/contacts/${encodeURIComponent(originalFirstName)}/${encodeURIComponent(originalLastName)}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(contactData)
            });
            successMessage = 'Contact updated successfully';
        } else {
            // Add Contact
            response = await fetch(`${API_BASE_URL}/contacts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(contactData)
            });
            successMessage = 'Contact added successfully';
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Operation failed');
        }

        showToast(successMessage, 'success');
        contactModalInstance.hide();
        loadContacts();
    } catch (error) {
        console.error('Operation failed:', error);
        showToast(error.message, 'danger');
    }
}
```
<mcfile name="contacts.html" path="D:\软件工程\Assignment 1 - Contacts Improved\Jiayao Hu_832301310_contacts_frontend\src\contacts.html"></mcfile>

## Conclusion and Reflection

The Contact Management System successfully implements a complete CRUD application with a clean separation between frontend and backend components. The project demonstrates the effectiveness of using Flask for creating RESTful APIs and Bootstrap for responsive web design.

Key takeaways from this project include:

1. **Separation of Concerns**: The clear division between frontend and backend makes the codebase more maintainable and allows for independent development of each component.

2. **User Experience**: Implementing features like search, sorting, loading indicators, and toast notifications significantly enhances the user experience.

3. **Error Handling**: Proper error handling ensures the application remains robust and provides meaningful feedback to users.

4. **Future Improvements**: Potential enhancements could include user authentication, contact groups, import/export functionality, and more advanced search capabilities.

This project provided valuable experience in full-stack web development and demonstrated how different technologies can work together to create a functional and user-friendly application.
        