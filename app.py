# This is a sample Python script for Assignment 1 - Contacts
# This script can only be executed by command line
# Created by Jiayao Hu on 10/18/2025

"""
Basic contacts functions
Function 1: add
Basic operations for adding contacts, including name, phone number, etc. and store contacts information in a back-end database
Function 2: modify
Modify the contacts information. must be read from the back-end database, can not use the cache.
Function 3: delete
Requirement as above
"""

# Import the json module to read and write JSON files
import json
import pandas as pd
from io import BytesIO
from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
from database import Database
from werkzeug.utils import secure_filename


# Initialize the Flask app.
app = Flask(__name__)
CORS(app)


# Define a class Contacts to store contacts information,
# with name, phone number, email, address, institution and is_starred
class Contacts:
    def __init__(self, first_name, last_name, category="", phone_number="", email="", address="", institution="", is_starred=False):
        self.first_name = first_name
        self.last_name = last_name
        self.category = category
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.institution = institution
        self.is_starred = is_starred

    # Overload the __str__ method to print the
    # contact information in a readable format
    def __str__(self):
        starred = "★" if self.is_starred else "☆"
        return f"{starred} Name: {self.first_name} {self.last_name}, Category: {self.category}, Institution: {self.institution}, Phone Number: {self.phone_number}, Email: {self.email}, Address: {self.address}"

    # Convert the contact information to a dictionary
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "category": self.category,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            "institution": self.institution,
            "is_starred": self.is_starred
        }

# Define a class AddressBook to store contacts information,
class AddressBook:
    # Initialize the AddressBook with database connection
    def __init__(self):
        self.db = Database()

    # Add contact to the AddressBook
    def add_contact(self, contact: Contacts):
        if self.db.add_contact(contact.to_dict()):
            print(f"Contact {contact.first_name} {contact.last_name} is added successfully.")
            return True
        else:
            print(f"Error: Contact with name '{contact.first_name} {contact.last_name}' already exists.")
            return False

    # find contact in the AddressBook by name
    def find_contact_in_list(self, contacts, first_name: str, last_name: str):
        for i, contact in enumerate(contacts):
            if Acontact['first_name'] == first_name and contact['last_name'] == last_name:
                return i
        return -1

    # Modify contact in the AddressBook
    def modify_contact(self, old_first_name: str, old_last_name: str, contact: Contacts):
        if self.db.update_contact(old_first_name, old_last_name, contact.to_dict()):
            if contact.first_name != old_first_name or contact.last_name != old_last_name:
                print(f"Contact '{old_first_name} {old_last_name}' has been renamed to '{contact.first_name} {contact.last_name}' successfully.")
            else:
                print(f"Contact '{old_first_name} {old_last_name}' is modified successfully.")
            return True
        else:
            print(f"Contact {old_first_name} {old_last_name} is not found.")
            return False

    # Delete contact in the AddressBook
    def delete_contact(self, first_name: str, last_name: str):
        if self.db.delete_contact(first_name, last_name):
            print(f"Contact {first_name} {last_name} is deleted successfully.")
            return True
        else:
            print(f"Contact {first_name} {last_name} is not found.")
            return False

    # Load all contacts from the AddressBook
    def load_contacts(self):
        contacts = self.db.get_all_contacts()
        print(f"{len(contacts)} contacts loaded successfully.")
        return contacts
    
    # Toggle starred status of a contact
    def toggle_starred(self, first_name: str, last_name: str):
        if self.db.toggle_starred(first_name, last_name):
            print(f"Contact {first_name} {last_name} starred status toggled successfully.")
            return True
        else:
            print(f"Contact {first_name} {last_name} not found.")
            return False

# Create a global AddressBook instance
address_book = AddressBook()

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = address_book.load_contacts()
    return jsonify(contacts)

@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contact = Contacts(data['first_name'], data['last_name'], data.get('category', ''),
                      data.get('phone_number', ''), data.get('email', ''), data.get('address', ''),
                      data.get('institution', ''), data.get('is_starred', False))
    if address_book.add_contact(contact):
        return jsonify({'message': f'Contact {contact.first_name} {contact.last_name} added successfully'}), 201
    else:
        return jsonify({'error': f'Contact with name {contact.first_name} {contact.last_name} already exists'}), 400

@app.route('/contacts/<first_name>/<last_name>', methods=['PUT'])
def update_contact(first_name, last_name):
    data = request.json
    contact = Contacts(data['first_name'], data['last_name'], data.get('category', ''),
                      data.get('phone_number', ''), data.get('email', ''), data.get('address', ''),
                      data.get('institution', ''), data.get('is_starred', False))
    if address_book.modify_contact(first_name, last_name, contact):
        return jsonify({'message': f'Contact {first_name} {last_name} updated successfully'})
    else:
        return jsonify({'error': f'Contact {first_name} {last_name} not found'}), 404

@app.route('/contacts/<first_name>/<last_name>', methods=['DELETE'])
def delete_contact(first_name, last_name):
    if address_book.delete_contact(first_name, last_name):
        return jsonify({'message': f'Contact {first_name} {last_name} deleted successfully'})
    else:
        return jsonify({'error': f'Contact {first_name} {last_name} not found'}), 404

# Toggle contact starred status
@app.route('/contacts/<first_name>/<last_name>/star', methods=['PUT'])
def toggle_star(first_name, last_name):
    if address_book.toggle_starred(first_name, last_name):
        return jsonify({'message': f'Contact {first_name} {last_name} starred status toggled successfully'})
    else:
        return jsonify({'error': f'Contact {first_name} {last_name} not found'}), 404

# Export contacts to Excel
@app.route('/contacts/export', methods=['GET'])
def export_contacts():
    contacts = address_book.load_contacts()
    
    # Convert contacts to a more readable format for Excel
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
    
    # Create a DataFrame and Excel writer
    df = pd.DataFrame(export_data)
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Contact List')
        
        # Get the xlsxwriter worksheet object
        worksheet = writer.sheets['Contact List']
        
        # Adjust column widths
        worksheet.column_dimensions['A'].width = 10
        worksheet.column_dimensions['B'].width = 15  # First Name
        worksheet.column_dimensions['C'].width = 15  # Last Name
        worksheet.column_dimensions['D'].width = 15  # Category
        worksheet.column_dimensions['E'].width = 30  # Institution
        worksheet.column_dimensions['F'].width = 20  # Phone Number
        worksheet.column_dimensions['G'].width = 30  # Email
        worksheet.column_dimensions['H'].width = 40  # Address
    
    output.seek(0)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=contacts_export.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return response

@app.route('/')
def index():
    return render_template('index.html')

# Main function to run the Flask app
@app.route('/contacts/import', methods=['POST'])
def import_contacts():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # 检查文件是否为空
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected for uploading'}), 400
    
    # 检查文件类型（同时支持 .xlsx 和 .xls 格式）
    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        return jsonify({'success': False, 'error': 'Only Excel files (.xlsx or .xls) are allowed'}), 400
    
    try:
        # 读取Excel文件，不将第一行作为标题行
        df = pd.read_excel(file, header=None)
        
        # 验证表格列数是否正确
        if df.shape[1] != 8:
            return jsonify({'success': False, 'error': f'Excel file must have exactly 8 columns, but found {df.shape[1]} columns'}), 400
        
        contacts_data = []
        invalid_count = 0
        
        # 遍历每一行数据
        for index, row in df.iterrows():
            try:
                # 解析星标状态（第一列）
                is_starred = 1 if row[0] == '★' else 0
                
                # 构建联系人数据
                contact_data = {
                    'first_name': str(row[1]) if pd.notna(row[1]) else '',
                    'last_name': str(row[2]) if pd.notna(row[2]) else '',
                    'category': str(row[3]) if pd.notna(row[3]) else '',
                    'institution': str(row[4]) if pd.notna(row[4]) else '',
                    'phone_number': str(row[5]) if pd.notna(row[5]) else '',
                    'email': str(row[6]) if pd.notna(row[6]) else '',
                    'address': str(row[7]) if pd.notna(row[7]) else '',
                    'is_starred': is_starred
                }
                
                # 验证联系人数据的基本完整性
                if not (contact_data['first_name'] or contact_data['last_name']):
                    invalid_count += 1
                    continue
                
                contacts_data.append(contact_data)
            except Exception as e:
                invalid_count += 1
                continue
        
        # 使用批量添加方法导入联系人
        if contacts_data:
            # 检查bulk_add_contacts方法是否存在
            if hasattr(address_book.db, 'bulk_add_contacts'):
                added_count, duplicate_contacts = address_book.db.bulk_add_contacts(contacts_data)
            else:
                # 如果bulk_add_contacts方法不存在，使用逐个添加的方式
                added_count = 0
                duplicate_contacts = []
                
                for contact_data in contacts_data:
                    contact = Contacts(
                        contact_data['first_name'], 
                        contact_data['last_name'], 
                        contact_data['category'],
                        contact_data['phone_number'],
                        contact_data['email'],
                        contact_data['address'],
                        contact_data['institution'],
                        contact_data['is_starred']
                    )
                    
                    if address_book.add_contact(contact):
                        added_count += 1
                    else:
                        duplicate_contacts.append(f"{contact_data['first_name']} {contact_data['last_name']}")
            
            # 返回与前端期望匹配的响应格式
            return jsonify({
                'success': True,
                'imported': added_count,
                'duplicates': len(duplicate_contacts),
                'invalid': invalid_count
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No valid contacts found in the Excel file'
            }), 400
            
    except Exception as e:
        # 记录详细错误信息以便调试
        print(f"Import error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error processing Excel file: {str(e)}'
        }), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
    # app.run(debug=True)