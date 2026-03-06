#!/usr/bin/env python3
"""
Smart SQLite Password Manager with AI Categorization
A secure CLI password manager with AI-powered features
"""

import argparse
import sqlite3
import os
import sys
from database import PasswordDatabase
from ai_agent import AIPasswordAgent

def main():
    parser = argparse.ArgumentParser(description='Smart Password Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add password command
    add_parser = subparsers.add_parser('add', help='Add a new password')
    add_parser.add_argument('service', help='Service name (e.g., Gmail, Facebook)')
    add_parser.add_argument('username', help='Username or email')
    add_parser.add_argument('password', help='Password to store')
    
    # Get password command
    get_parser = subparsers.add_parser('get', help='Retrieve a password')
    get_parser.add_argument('service', help='Service name to retrieve')
    
    # List passwords command
    list_parser = subparsers.add_parser('list', help='List all stored services')
    
    # Analyze password command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze password strength')
    analyze_parser.add_argument('service', help='Service name to analyze')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize database and AI agent
    db = PasswordDatabase('passwords.db')
    ai_agent = AIPasswordAgent()
    
    try:
        if args.command == 'add':
            # Get AI categorization
            category = ai_agent.categorize_service(args.service)
            print(f"AI detected category: {category}")
            
            # Store password
            db.add_password(args.service, args.username, args.password, category)
            print(f"✓ Password for {args.service} added successfully!")
            
        elif args.command == 'get':
            result = db.get_password(args.service)
            if result:
                service, username, password, category = result
                print(f"Service: {service}")
                print(f"Username: {username}")
                print(f"Password: {password}")
                print(f"Category: {category}")
            else:
                print(f"No password found for {args.service}")
                
        elif args.command == 'list':
            passwords = db.list_passwords()
            if passwords:
                print("\nStored passwords:")
                print("-" * 50)
                for service, username, category in passwords:
                    print(f"{service:<20} {username:<25} [{category}]")
            else:
                print("No passwords stored yet.")
                
        elif args.command == 'analyze':
            result = db.get_password(args.service)
            if result:
                service, username, password, category = result
                analysis = ai_agent.analyze_password_strength(password, service)
                print(f"\nPassword Analysis for {service}:")
                print("-" * 40)
                print(analysis)
            else:
                print(f"No password found for {args.service}")
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()