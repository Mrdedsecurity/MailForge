**MailForge** is a Python 3 utility that generates email addresses by parsing and processing name inputs. 
## ✨ Features

- **Smart Name Parsing**: Automatically extracts first, middle, and last names from various input formats
- **CSV & Text Output**: Export results in both CSV and plain text formats
- **Domain Customization**: Easily configure target email domains
- **Batch Processing**: Process hundreds of names from input files
- **Lightweight**: No external dependencies, pure Python 3

## 📋 Prerequisites

- **Python 3.6** or higher
- Basic command-line knowledge

## 🚀 Guide

```bash
# Clone the repository
git clone https://github.com/Mrdedsecurity/MailForge.git

# How to use 
cd MailForge
python3 mailforge.py --input (rawfilehere)  (Will output file as "full_list.txt")
python3 mailforge.py --input (rawfilehere) --output (outputfilehere)
python3 mailforge.py --input (rawfilehere) -v (verbose mode set)

## ⚠️ Warning
This tool can create false postives, check all output for mistakes. 
