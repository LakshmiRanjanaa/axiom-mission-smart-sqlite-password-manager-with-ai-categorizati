# Smart SQLite Password Manager with AI Categorization

A secure command-line password manager that uses SQLite for encrypted storage and OpenAI for intelligent categorization and password policy suggestions.

## Features
- Encrypted password storage using SQLite and cryptography
- AI-powered automatic categorization
- Password strength analysis
- Policy suggestions for better security

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set your OpenAI API key: `export OPENAI_API_KEY=your_key_here`
3. Run the app: `python password_manager.py --help`

## Usage Examples
bash
# Add a new password
python password_manager.py add "Gmail" "myemail@gmail.com" "mypassword123"

# List all passwords
python password_manager.py list

# Get a specific password
python password_manager.py get "Gmail"

# Analyze password strength
python password_manager.py analyze "Gmail"


## Security Note
This is a starter project for learning. For production use, consider additional security measures like master password hashing and secure key derivation.