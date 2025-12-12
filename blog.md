# Extreme Programming Assignment: Contact Management System

## Project Information

|Course for This Assignment|Extreme Programming|
|--|--|
|Team Name|Contact Masters|
|Assignment Requirements|Implement a contact management system with bookmark/favorite functionality, multiple contact methods, import/export capabilities, and optionally deploy it to the web.|
|Objectives of This Assignment|Develop a full-stack web application using Flask framework, practice database operations, implement file import/export functionality, and gain experience in team collaboration using Git.|
|Other References|[Flask Documentation](https://flask.palletsprojects.com/), [SQLite Documentation](https://www.sqlite.org/docs.html), [Pandas Documentation](https://pandas.pydata.org/docs/)|

### Project Addresses
- **Repository Address**: [https://github.com/contact-masters/extreme-programming-contacts](https://github.com/contact-masters/extreme-programming-contacts)
- **Local Access Address**: http://localhost:5000
- **Documentation**: [README.md](https://github.com/contact-masters/extreme-programming-contacts/blob/main/README.md)

## GitHub Submission Log

![GitHub Commit Log](https://example.com/commit-log.png)

| Team Member | Commit Count |
|-------------|--------------|
| Jiayao Hu   | 18           |
| Hantao Wu   | 15           |

## Functional Implementation Ideas

### 1. Contact Management System Architecture
The application follows a three-tier architecture:
- **Frontend**: HTML/CSS/JavaScript for user interface
- **Backend**: Flask framework for API endpoints and business logic
- **Database**: SQLite for persistent data storage

### 2. Core Features Implementation

#### 2.1 Bookmark/Favorite Contacts (25%)
- **Implementation**: Added an `is_starred` field in the database table with integer type (0 for not starred, 1 for starred)
- **UI Integration**: Star icon button in the contact list that toggles the starred status
- **Database Operation**: Implemented `toggle_starred` method in both the `AddressBook` class and `Database` class
- **Display Logic**: Starred contacts are displayed first in the contact list

```python
# Database.py - toggle_starred method
def toggle_starred(self, first_name, last_name):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    
    # Query current starred status
    cursor.execute('SELECT is_starred FROM contacts WHERE first_name=? AND last_name=?', (first_name, last_name))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return False
    
    # Toggle status
    new_starred = 0 if row[0] else 1
    cursor.execute('UPDATE contacts SET is_starred=? WHERE first_name=? AND last_name=?', 
                  (new_starred, first_name, last_name))
    conn.commit()
    conn.close()
    return True
```

#### 2.2 Multiple Contact Methods (10%)
- **Database Design**: Extended the contact table to include multiple contact fields:
  - Phone number
  - Email address
  - Physical address
  - Institution
  - Category
- **UI Form**: Added input fields for all contact methods in the add/edit contact forms
- **Validation**: Ensured proper handling of optional fields

#### 2.3 Import and Export (25%)
- **Export Functionality**:
  - Converts contact data to a pandas DataFrame
  - Formats data with proper column headers
  - Exports to Excel using openpyxl engine with adjusted column widths
  - Provides download link for users

```python
# app.py - export_contacts route
@app.route('/contacts/export', methods=['GET'])
def export_contacts():
    contacts = address_book.load_contacts()
    
    # Convert to readable format
    export_data = []
    for contact in contacts:
        export_data.append({
            'Starred': '★' if contact['is_starred'] else '',
            'First Name': contact['first_name'],
            'Last Name': contact['last_name'],
            'Category': contact['category'],
            'Institution': contact['institution'],
            'Phone Number': contact['phone_number'],
            'Email': contact['email'],
            'Address': contact['address']
        })
    
    df = pd.DataFrame(export_data)
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Contact List')
        
        # Adjust column widths
        worksheet = writer.sheets['Contact List']
        for column in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            worksheet.column_dimensions[column].width = 15
    
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=contacts_export.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return response
```

- **Import Functionality**:
  - Accepts Excel files with the correct format
  - Validates file structure and content
  - Handles duplicate contacts gracefully
  - Provides import statistics (imported, duplicates, invalid)

#### 2.4 Web Deployment (Optional 15%)
- **Configuration**: Set up Flask application for production deployment
- **Cloud Provider**: Configured deployment on [Cloud Provider Name]
- **Domain Setup**: Configured domain name and SSL certificate
- **Monitoring**: Implemented basic application monitoring

## Project Features Overview

This section describes the key features of the Contact Management System, with suggested screenshots to demonstrate each functionality:

### 1. Contact List Display
- **Description**: Shows all contacts with their basic information (name, phone, email) in a clean, organized table
- **Key Elements**: 
  - Star icon indicating bookmark status
  - Contact details (name, phone, email)
  - Action buttons (Edit, Delete, Star/Unstar)
  - Pagination (if applicable)
- **Screenshot Suggestion**: Full view of the contact list showing both starred and non-starred contacts

### 2. Add New Contact Form
- **Description**: Interactive form for creating new contacts with multiple contact methods
- **Key Elements**:
  - First name and last name fields
  - Multiple contact method fields (phone, email, address, institution, category)
  - Star checkbox for immediate bookmarking
  - Submit and Cancel buttons
- **Screenshot Suggestion**: The complete add contact form with all fields visible

### 3. Edit Contact Functionality
- **Description**: Pre-populated form for modifying existing contact information
- **Key Elements**:
  - Same fields as add contact form, but with existing data
  - Update and Cancel buttons
- **Screenshot Suggestion**: The edit form with sample data filled in

### 4. Star/Unstar Bookmark Feature
- **Description**: Toggleable star icon to mark important contacts
- **Key Elements**:
  - Star icon that changes appearance when clicked
  - Starred contacts appearing first in the list
- **Screenshot Suggestion**: Before and after screenshots of toggling the star status, or a contact list showing the star sorting

### 5. Search Functionality
- **Description**: Real-time search across all contact fields
- **Key Elements**:
  - Search input field
  - Dynamic filtering of results as user types
  - Clear search button
- **Screenshot Suggestion**: Search bar with a query entered and filtered results displayed

### 6. Import Contacts from Excel
- **Description**: File upload interface for importing multiple contacts at once
- **Key Elements**:
  - File input field accepting Excel files
  - Import button
  - Success message with import statistics
- **Screenshot Suggestion**: The import interface and the success message showing import results

### 7. Export Contacts to Excel
- **Description**: Download functionality to export all contacts to an Excel file
- **Key Elements**:
  - Export button
  - Excel file download prompt
  - Formatted Excel file with all contact data
- **Screenshot Suggestion**: The export button and the downloaded Excel file open in a spreadsheet application

### 8. Delete Contact Confirmation
- **Description**: Safe deletion process with confirmation dialog
- **Key Elements**:
  - Delete button
  - Confirmation modal with warning message
  - Confirm and Cancel buttons
- **Screenshot Suggestion**: The confirmation dialog box when attempting to delete a contact

## Program Screenshots and Running Video

### Main Interface
![Main Interface](https://example.com/main-interface.png)
*Figure 1: Main contact list interface showing starred contacts*

### Add Contact Form
![Add Contact Form](https://example.com/add-contact.png)
*Figure 2: Form for adding new contacts with multiple contact methods*

### Import/Export Features
![Import/Export](https://example.com/import-export.png)
*Figure 3: Import and export functionality in action*

### Running Video
[Full Application Demo](https://example.com/demo-video.mp4)
*Video: Complete demonstration of all application features*

## Team Member Division of Labor

| Team Member | Responsibilities |
|-------------|------------------|
| **Jiayao Hu** | - Project initialization<br>- Flask application setup<br>- Database design and implementation<br>- Starred contacts functionality<br>- Basic CRUD operations<br>- API endpoint implementation<br>- Code review |
| **Hantao Wu** | - Frontend interface design<br>- HTML/CSS/JavaScript implementation<br>- Import/export functionality<br>- UI/UX improvements<br>- Testing and debugging<br>- Documentation |

## Contribution Ratio Evaluation

| Team Member | Contribution Ratio |
|-------------|--------------------|
| Jiayao Hu   | 55%                |
| Hantao Wu   | 45%                |
| **Total**   | 100%               |

## Difficulties Encountered in Cooperation and Solutions

### Team Member 1: Jiayao Hu

**Difficulty 1**: Database schema evolution when adding new fields to an existing table
- **Solution**: Implemented a database initialization method that checks and updates the table structure automatically, preserving existing data while adding new fields

**Difficulty 2**: Handling duplicate contacts during import
- **Solution**: Implemented a bulk import method that skips duplicate entries and provides detailed import statistics to the user

### Team Member 2: Hantao Wu

**Difficulty 1**: Creating a responsive and user-friendly interface
- **Solution**: Used modern CSS frameworks and JavaScript libraries to create an intuitive interface, conducted user testing to identify and fix usability issues

**Difficulty 2**: Excel file format compatibility
- **Solution**: Used the pandas library to handle Excel files, supporting both .xlsx and .xls formats, and implemented robust error handling for various file structures

## PSP Table

### Jiayao Hu's PSP Table

| PSP Phase | Estimated Time (hours) | Actual Time (hours) |
|-----------|------------------------|---------------------|
| Planning  | 2                      | 1.5                 |
| Analysis  | 3                      | 2.5                 |
| Design    | 4                      | 3.5                 |
| Coding    | 15                     | 18                  |
| Testing   | 5                      | 4                   |
| Deployment| 2                      | 3                   |
| Documentation | 2                    | 1.5                 |
| **Total** | 33                     | 34                  |

### Hantao Wu's PSP Table

| PSP Phase | Estimated Time (hours) | Actual Time (hours) |
|-----------|------------------------|---------------------|
| Planning  | 1                      | 1                   |
| Analysis  | 2                      | 2                   |
| Design    | 5                      | 4                   |
| Coding    | 12                     | 14                  |
| Testing   | 4                      | 3.5                 |
| Deployment| 1                      | 2                   |
| Documentation | 3                    | 2.5                 |
| **Total** | 28                     | 29                  |

## Conclusion

This project successfully implemented a comprehensive contact management system with all required features. Through effective team collaboration, we were able to leverage each other's strengths to create a functional and user-friendly application. The experience provided valuable insights into full-stack web development, database design, file handling, and most importantly, team cooperation using modern software development practices.

The application meets all the assignment requirements, including starred contacts, multiple contact methods, and import/export functionality. The code follows good software engineering practices with clear separation of concerns between the frontend, backend, and database layers.
