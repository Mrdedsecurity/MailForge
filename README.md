**MailForge - Email Address Generator
✨ Overview
MailForge is a Python 3 utility that intelligently generates email addresses by parsing name inputs. This tool creates professional email formats from personal names, making it useful for research, marketing outreach, and contact list building.

⚠️ Python 3 Requirement
This tool requires Python 3 to run properly. Check your Python version:

bash
python --version
# or
python3 --version
If you see Python 2.x, you need to install Python 3 or use python3 command specifically.

🚀 Quick Start
Installation
bash
git clone https://github.com/Mrdedsecurity/MailForge.git
cd MailForge
Running with Python 3
Use one of these commands depending on your system:

bash
# Most systems with Python 3 installed
python3 mailforge.py

# Some systems where 'python' defaults to Python 3
python mailforge.py

# If you have multiple Python versions, specify Python 3 explicitly
python3.8 mailforge.py  # or python3.9, python3.10, etc.
📁 Project Structure
text
MailForge/
├── mailforge.py     # Main Python 3 script
├── input.txt        # Input file with names to process
├── test_full_list.csv   # Example output in CSV format
├── test_full_list.txt   # Example output in text format
├── README.md        # This documentation
└── LICENSE          # License file
🔧 Features
Name Parsing: Automatically extracts first, last, and middle names from input

Multiple Email Formats: Generates emails in common professional formats:

first.last@domain.com

first_last@domain.com

firstinitiallast@domain.com

etc.

CSV Support: Outputs results in CSV format for easy spreadsheet integration

Python 3 Compatible: Uses modern Python 3 syntax and libraries

Customizable: Easily modify to add custom email formats or domains

📝 Usage Examples
Prepare your input file (input.txt):

text
John Smith
Jane Doe
Robert James Miller
Run the script with Python 3:

bash
python3 mailforge.py
Check output files:

test_full_list.txt - Text format results

test_full_list.csv - CSV format results

🐍 Python 3 Troubleshooting
Common Issues & Solutions:
Issue	Solution
python runs Python 2.x	Use python3 mailforge.py instead
"Command not found: python3"	Install Python 3
Syntax errors with print statements	Ensure you're using Python 3 (Python 2 uses print x, Python 3 uses print(x))
Module import errors	Check Python 3 library installation
Verifying Python 3 Installation:
bash
# Check if Python 3 is available
python3 --version
# Should show: Python 3.x.x

# Alternative check
python --version
# If this shows 2.x, you must use 'python3' command
📊 Technical Details
Language: Python 3 (100%)

Latest Update: February 6, 2026

Version: Initial release

Dependencies: Standard Python 3 libraries (no external packages required)

Commit History: 11 commits with recent improvements to CSV functionality

🤝 Contributing
Contributions are welcome! Feel free to:

Report issues

Suggest new features

Submit pull requests

Note: All contributions must maintain Python 3 compatibility.

📄 License
This project is released under the terms specified in the LICENSE file included in the repository.**
