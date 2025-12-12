import sqlite3

class Database:
    def __init__(self, db_file="contacts.db"):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # 检查当前表结构
        cursor.execute("PRAGMA table_info(contacts)")
        columns = [column[1] for column in cursor.fetchall()]

        # 如果表不存在或字段不完整，则创建或修改表
        if not columns:
            # 创建全新的表
            cursor.execute("""
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
                )
            """)
        else:
            # 表已存在，检查并添加缺失的字段
            if 'first_name' not in columns or 'last_name' not in columns:
                # 需要从name字段拆分first_name和last_name
                # 创建临时表
                cursor.execute("""
                    CREATE TABLE contacts_temp (
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
                    )
                """)

                # 从原表复制数据并拆分姓名
                cursor.execute("SELECT name, phone_number, email, address FROM contacts")
                rows = cursor.fetchall()

                for row in rows:
                    full_name = row[0]
                    # 简单拆分姓名，实际应用中可能需要更复杂的逻辑
                    name_parts = full_name.split(' ', 1)
                    if len(name_parts) == 1:
                        first_name = name_parts[0]
                        last_name = ''
                    else:
                        first_name = name_parts[0]
                        last_name = name_parts[1]

                    cursor.execute(
                        "INSERT INTO contacts_temp (first_name, last_name, category, phone_number, email, address, institution, is_starred) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (first_name, last_name, '', row[1], row[2], row[3], '', 0)
                    )

                # 删除原表并重命名临时表
                cursor.execute("DROP TABLE contacts")
                cursor.execute("ALTER TABLE contacts_temp RENAME TO contacts")

            # 添加category字段（如果不存在）
            if 'category' not in columns:
                cursor.execute("ALTER TABLE contacts ADD COLUMN category TEXT")
            
            # 添加institution字段（如果不存在）
            if 'institution' not in columns:
                cursor.execute("ALTER TABLE contacts ADD COLUMN institution TEXT")
            
            # 添加is_starred字段（如果不存在）
            if 'is_starred' not in columns:
                cursor.execute("ALTER TABLE contacts ADD COLUMN is_starred INTEGER DEFAULT 0")

        conn.commit()
        conn.close()

    def get_all_contacts(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        # 按is_starred降序排序，让星标联系人优先显示
        cursor.execute('SELECT first_name, last_name, category, phone_number, email, address, institution, is_starred FROM contacts ORDER BY is_starred DESC')
        rows = cursor.fetchall()
        conn.close()

        return [{"first_name": row[0], "last_name": row[1], "category": row[2], "phone_number": row[3], "email": row[4],
                 "address": row[5], "institution": row[6], "is_starred": bool(row[7])} for row in rows]

    def add_contact(self, contact_data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO contacts (first_name, last_name, category, phone_number, email, address, institution, is_starred)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (contact_data['first_name'], contact_data['last_name'],
                  contact_data.get('category', ''), contact_data['phone_number'],
                  contact_data['email'], contact_data['address'],
                  contact_data.get('institution', ''), contact_data.get('is_starred', 0)))
            conn.commit()
            print(f"Contact {contact_data['first_name']} {contact_data['last_name']} is added successfully.")
            return True
        except sqlite3.IntegrityError:
            print(
                f"Error: Contact with name '{contact_data['first_name']} {contact_data['last_name']}' already exists.")
            return False
        finally:
            conn.close()

    def update_contact(self, old_first_name, old_last_name, contact_data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE contacts
                SET first_name = ?, last_name = ?, category = ?, phone_number = ?, email = ?, address = ?, institution = ?, is_starred = ?
                WHERE first_name = ? AND last_name = ?
            """, (contact_data['first_name'], contact_data['last_name'], contact_data.get('category', ''),
                  contact_data['phone_number'], contact_data['email'], contact_data['address'],
                  contact_data.get('institution', ''), contact_data.get('is_starred', 0),
                  old_first_name, old_last_name))
            conn.commit()
            print(f"Contact {old_first_name} {old_last_name} is updated successfully.")
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_contact(self, first_name, last_name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # 添加调试信息
        print(f"Attempting to delete contact: '{first_name}' '{last_name}'")
        
        # 先检查联系人是否存在
        cursor.execute('SELECT first_name, last_name FROM contacts WHERE first_name=? AND last_name=?', (first_name, last_name))
        existing = cursor.fetchone()
        
        if not existing:
            print(f"Contact not found: '{first_name}' '{last_name}'")
            conn.close()
            return False
        
        # 执行删除操作
        cursor.execute('DELETE FROM contacts WHERE first_name=? AND last_name=?', (first_name, last_name))
        conn.commit()
        affected = cursor.rowcount > 0
        
        print(f"Delete operation affected {cursor.rowcount} rows")
        
        conn.close()
        return affected
        
    # 更新联系人星标状态的方法
    def toggle_starred(self, first_name, last_name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # 先查询当前星标状态
        cursor.execute('SELECT is_starred FROM contacts WHERE first_name=? AND last_name=?', (first_name, last_name))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        # 切换星标状态
        new_starred = 0 if row[0] else 1
        cursor.execute('UPDATE contacts SET is_starred=? WHERE first_name=? AND last_name=?', 
                      (new_starred, first_name, last_name))
        conn.commit()
        conn.close()
        return True

    def bulk_add_contacts(self, contacts_data):
        """
        批量添加联系人以提高性能
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        added_count = 0
        duplicate_contacts = []
        
        try:
            for contact_data in contacts_data:
                try:
                    cursor.execute("""
                        INSERT INTO contacts (first_name, last_name, category, phone_number, email, address, institution, is_starred)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (contact_data['first_name'], contact_data['last_name'],
                          contact_data.get('category', ''), contact_data['phone_number'],
                          contact_data['email'], contact_data['address'],
                          contact_data.get('institution', ''), contact_data.get('is_starred', 0)))
                    added_count += 1
                except sqlite3.IntegrityError:
                    # 联系人已存在
                    duplicate_contacts.append(f"{contact_data['first_name']} {contact_data['last_name']}")
                    continue
                    
            conn.commit()
            return added_count, duplicate_contacts
        finally:
            conn.close()

    def search_contacts(self, search_term):
        """
        搜索联系人，在所有字段中查找匹配的关键词
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # 构建SQL查询，在所有文本字段中搜索
        query = """
            SELECT first_name, last_name, category, phone_number, email, address, institution, is_starred 
            FROM contacts 
            WHERE first_name LIKE ? OR last_name LIKE ? OR category LIKE ? OR phone_number LIKE ? OR email LIKE ? OR address LIKE ? OR institution LIKE ?
            ORDER BY is_starred DESC
        """
        
        # 使用%进行模糊匹配
        search_pattern = f'%{search_term}%'
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        rows = cursor.fetchall()
        conn.close()

        return [{"first_name": row[0], "last_name": row[1], "category": row[2], "phone_number": row[3], "email": row[4],
                 "address": row[5], "institution": row[6], "is_starred": bool(row[7])} for row in rows]