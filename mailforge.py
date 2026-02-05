#!/usr/bin/env python3

import sys
import argparse
import re

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

    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            for line in file:
                original_line = line.strip()
                if not original_line:
                    continue

                # 1. Filter hard junk keywords
                clean_check = original_line.lower()
                trash_keywords = ["linkedin member", "anonymous user", "view profile"]
                if any(k in clean_check for k in trash_keywords):
                    if verbose: rejected.append((original_line, "Trash keyword"))
                    continue

                # 2. Comma Flip 
                working_line = original_line
                if ',' in working_line:
                    parts = working_line.split(',')
                    if len(parts) >= 2:
                        working_line = f"{parts[1].strip()} {parts[0].strip()}"

                # 3. Aggressive Cleaning
                # Remove content inside parentheses (like degree connections)
                working_line = re.sub(r'\(.*?\)', ' ', working_line)
                # Remove common titles
                working_line = re.sub(r'\b(Dr|Mr|Mrs|Ms|Prof|Project|Manager|Engineer)\.?\b', '', working_line, flags=re.IGNORECASE)
                # Replace non-alphabetic separators with spaces
                working_line = re.sub(r"[^a-zA-Z\s'-]", " ", working_line)

                # 4. Extract first two valid "Name" words
                words = working_line.split()
                clean_words = []
                ignore_list = ["at", "the", "and", "connection", "degree", "of"]

                for w in words:
                    cleaned_w = re.sub(r"[^a-zA-Z'-]", "", w)
                    if len(cleaned_w) > 1 and cleaned_w.lower() not in ignore_list:
                        clean_words.append(cleaned_w)

                # 5. Build Final Email
                if len(clean_words) >= 2:
                    first_name = clean_words[0].lower().replace("'", "")
                    last_name = clean_words[1].lower().replace("'", "")
                    
                    email = f"{first_name}.{last_name}@{domain}"
                    if email not in emails:
                        emails.append(email)
                else:
                    if verbose: rejected.append((original_line, "Insufficient name parts"))

        # Save to file
        with open(output_filename, "w", encoding="utf-8") as out_file:
            for email in emails:
                out_file.write(email + "\n")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return emails, rejected

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser(description="MailForge Tool")
    parser.add_argument("--input", required=True, help="Input file containing raw names")
    parser.add_argument("--output", default="full_list.txt", help="Output file for generated emails")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable rejection logging")

    args = parser.parse_args()

    domain_input = input("Enter email domain (example: outlook.com): ").strip().lower()
    if not domain_input:
        print("Error: Domain cannot be empty.")
        sys.exit(1)

    # RUN TOOL
    emails, rejected = generate_emails_from_file(
        args.input, 
        args.output, 
        domain_input, 
        verbose=args.verbose
    )

    # FINAL SUMMARY OUTPUT
    print("-" * 40)
    print(f"✔ {len(emails)} unique email addresses forged.")
    print(f"✔ Results saved to '{args.output}'")
    
    if args.verbose:
        if rejected:
            with open("rejected_log.txt", "w", encoding="utf-8") as rj:
                for item, reason in rejected:
                    rj.write(f"{item} --> {reason}\n")
            print(f"⚠ {len(rejected)} entries rejected (see 'rejected_log.txt')")
        else:
            print("⚠ 0 entries rejected.")

    print("🔥 MailForge execution complete.")