"""
Secure SQLite database handler with encryption
"""

import sqlite3
import os
from cryptography.fernet import Fernet
import base64
import hashlib

class PasswordDatabase:
    def __init__(self, db_path='passwords.db'):
        self.db_path = db_path
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        self._init_database()
    
    def _get_or_create_key(self):
        """Get encryption key from file or create new one"""
        key_file = 'master.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # For starter project, we'll use a simple key generation
            # In production, this should be derived from a master password
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            print("🔑 New encryption key generated and saved to master.key")
            print("⚠️  Keep this file safe! Without it, your passwords cannot be decrypted.")
            return key
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password BLOB NOT NULL,
                    category TEXT DEFAULT 'uncategorized',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def _encrypt_password(self, password):
        """Encrypt password using Fernet symmetric encryption"""
        return self.cipher.encrypt(password.encode())
    
    def _decrypt_password(self, encrypted_password):
        """Decrypt password from database"""
        return self.cipher.decrypt(encrypted_password).decode()
    
    def add_password(self, service, username, password, category='uncategorized'):
        """Add a new password entry to the database"""
        encrypted_password = self._encrypt_password(password)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO passwords 
                (service, username, encrypted_password, category)
                VALUES (?, ?, ?, ?)
            ''', (service, username, encrypted_password, category))
            conn.commit()
    
    def get_password(self, service):
        """Retrieve and decrypt a password by service name"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT service, username, encrypted_password, category
                FROM passwords WHERE service = ?
            ''', (service,))
            
            result = cursor.fetchone()
            if result:
                service, username, encrypted_password, category = result
                decrypted_password = self._decrypt_password(encrypted_password)
                return service, username, decrypted_password, category
            return None
    
    def list_passwords(self):
        """List all stored password entries (without actual passwords)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT service, username, category
                FROM passwords ORDER BY service
            ''')
            return cursor.fetchall()