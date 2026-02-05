#!/usr/bin/env python3

import sys
import argparse
import re
import csv
from datetime import datetime

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

def generate_emails_from_file(input_filename, output_filename, domain, verbose=False, export_csv=False):
    results = [] 
    emails_only = [] 
    rejected = []

    # Junk list to catch headers and LinkedIn artifacts
    junk_keywords = [
        "valid", "trash", "edge", "duplicate", "test", "data", "cases", "names",
        "connection", "degree", "first", "second", "third", "st", "nd", "rd", "th"
    ]

    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            for line in file:
                original_line = line.strip()
                if not original_line or "---" in original_line:
                    continue

                # 1. Filter known junk phrases
                clean_check = original_line.lower()
                trash_phrases = ["linkedin member", "anonymous user", "view profile", "click here"]
                if any(p in clean_check for p in trash_phrases):
                    if verbose: rejected.append((original_line, "Trash phrase"))
                    continue

                # 2. Comma Flip Logic
                working_line = original_line
                if ',' in working_line:
                    parts = working_line.split(',')
                    if len(parts) >= 2:
                        working_line = f"{parts[1].strip()} {parts[0].strip()}"

                # 3. Cleaning
                working_line = re.sub(r'\(.*?\)', ' ', working_line)
                working_line = re.sub(r'\b(Dr|Mr|Mrs|Ms|Prof|CEO|Founder|Manager|Engineer|Specialist)\.?\b', '', working_line, flags=re.IGNORECASE)
                
                # 4. Extraction
                words = working_line.split()
                clean_words = []
                for w in words:
                    cleaned_w = re.sub(r"[^a-zA-Z'-]", "", w)
                    low_w = cleaned_w.lower()
                    if len(cleaned_w) > 1 and low_w not in junk_keywords:
                        clean_words.append(cleaned_w)

                # 5. Build Final Email & Metadata
                if len(clean_words) >= 2:
                    f_name = clean_words[0].lower().replace("'", "")
                    l_name = clean_words[1].lower().replace("'", "")
                    full_email = f"{f_name}.{l_name}@{domain}"
                    
                    if full_email not in emails_only:
                        emails_only.append(full_email)
                        
                        # Added Time of Discovery
                        discovery_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        results.append({
                            'First Name': f_name.capitalize(),
                            'Last Name': l_name.capitalize(),
                            'Email': full_email,
                            'Time of Discovery': discovery_time
                        })
                else:
                    if verbose: rejected.append((original_line, "No valid name-pair found"))

        # Save TXT
        with open(output_filename, "w", encoding="utf-8") as out_file:
            for email in emails_only:
                out_file.write(email + "\n")

        # Save CSV
        csv_path = None
        if export_csv and results:
            csv_path = output_filename.rsplit('.', 1)[0] + ".csv"
            keys = results[0].keys()
            with open(csv_path, "w", newline='', encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(results)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return emails_only, rejected, csv_path

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser(description="MailForge Tool")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="full_list.txt")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    print("Example domains: google.com, outlook.com, tesla.com")
    domain_input = input("Enter email domain: ").strip().lower()
    if not domain_input:
        sys.exit("Error: Domain required.")
    
    csv_choice = input("Export results to CSV with timestamps? (y/n): ").strip().lower()
    do_csv = csv_choice == 'y'

    emails, rejected, csv_path = generate_emails_from_file(
        args.input, args.output, domain_input, verbose=args.verbose, export_csv=do_csv
    )

    print("-" * 40)
    print(f"✔ {len(emails)} unique email addresses forged.")
    if csv_path:
        print(f"✔ CSV with Discovery Times saved to: {csv_path}")
    
    print("🔥 MailForge execution complete.")
