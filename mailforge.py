#!/usr/bin/env python3

import sys
import argparse
import re

# =========================================
#             M A I L F O R G E
#       Email Generator & Filter Tool
#             Made by MrDedSec
# =========================================

def print_banner():
    print(r"""
 ___  ___  ___  _____ _      ______ ___________ _____  _____ 
 |  \/  | / _ \|_   _| |     |  ___|  _  | ___ \  __ \|  ___|
 | .  . |/ /_\ \ | | | |     | |_  | | | | |_/ / |  \/| |__  
 | |\/| ||  _  | | | | |     |  _| | | | |    /| | __ |  __| 
 | |  | || | | |_| |_| |____ | |   \ \_/ / |\ \| |_\ \| |___ 
 \_|  |_/\_| |_/\___/\_____/ \_|    \___/\_| \_|\____/\____/ 

                Made by MrDedSec
""")

def generate_emails_from_file(input_filename, output_filename, domain, verbose=False):
    emails = []
    rejected = []

    # Regex Pattern: Looks for two capitalized words (First Last) 
    # and ensures they are followed by common delimiters or end of line.
    name_pattern = re.compile(r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b')

    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            for line in file:
                original_line = line.strip()
                
                if not original_line:
                    continue

                # 1. Filter out known "trash" strings immediately
                clean_check = original_line.lower()
                trash_keywords = ["linkedin member", "anonymous user", "view profile", "connection"]
                if any(k in clean_check for k in trash_keywords):
                    if verbose:
                        rejected.append((original_line, "Trash keyword detected"))
                    continue

                # 2. Smart Extraction: Find the name within the line
                # This works even if the line is "John Doe - Software Engineer"
                match = name_pattern.search(original_line)

                if match:
                    first_name = match.group(1).lower()
                    last_name = match.group(2).lower()
                    
                    # Optional: Add check for length
                    if len(last_name) <= 1:
                        if verbose:
                            rejected.append((original_line, "Last name too short"))
                        continue

                    email = f"{first_name}.{last_name}@{domain}"
                    
                    # Prevent duplicates
                    if email not in emails:
                        emails.append(email)
                else:
                    if verbose:
                        rejected.append((original_line, "No name pattern found"))

        # Write the valid emails
        with open(output_filename, "w", encoding="utf-8") as out_file:
            for email in emails:
                out_file.write(email + "\n")

        # Write rejected log if verbose
        if verbose and rejected:
            with open("rejected_log.txt", "w", encoding="utf-8") as reject_file:
                for name, reason in rejected:
                    reject_file.write(f"{name} --> {reason}\n")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    return emails, rejected

if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="MailForge - Email Generator Tool")
    parser.add_argument("--input", required=True, help="Input file containing raw names")
    parser.add_argument("--output", default="full_list.txt", help="Output file for generated emails")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable rejection logging")

    args = parser.parse_args()

    domain_input = input("Enter email domain (example: outlook.com): ").strip().lower()
    if not domain_input:
        print("Error: Domain cannot be empty.")
        sys.exit(1)

    emails, rejected = generate_emails_from_file(
        args.input,
        args.output,
        domain_input,
        verbose=args.verbose
    )

    print(f"\n✔ {len(emails)} unique email addresses forged.")
    print(f"✔ Results saved to '{args.output}'")

    if args.verbose:
        print(f"⚠ {len(rejected)} entries filtered out (see 'rejected_log.txt')")

    print("🔥 MailForge execution complete.")
