#!/usr/bin/env python3

import sys
import argparse

# =========================================
#             M A I L F O R G E
#       Email Generator & Filter Tool
#             Made by MrDedSec
# =========================================

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
                original_name = line.strip()
                clean_name = original_name

                if not clean_name:
                    if verbose:
                        rejected.append((original_name, "Empty line"))
                    continue

                if clean_name.lower() == "anonymous user":
                    if verbose:
                        rejected.append((original_name, "Anonymous user"))
                    continue

                parts = clean_name.split()

                if len(parts) < 2:
                    if verbose:
                        rejected.append((original_name, "Not a full name"))
                    continue

                first_name = parts[0]
                last_name = parts[-1]

                if len(last_name) <= 1:
                    if verbose:
                        rejected.append((original_name, "Last name too short"))
                    continue

                if not (first_name.isalpha() and last_name.isalpha()):
                    if verbose:
                        rejected.append((original_name, "Non-alphabetic characters in name"))
                    continue

                email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
                emails.append(email)

        with open(output_filename, "w", encoding="utf-8") as out_file:
            for email in emails:
                out_file.write(email + "\n")

        if verbose:
            with open("rejected_log.txt", "w", encoding="utf-8") as reject_file:
                for name, reason in rejected:
                    reject_file.write(f"{name} --> {reason}\n")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        sys.exit(1)

    return emails, rejected


# -------- ARGUMENT PARSING --------
parser = argparse.ArgumentParser(description="MailForge - Email Generator Tool")
parser.add_argument("--input", required=True, help="Input file containing raw names")
parser.add_argument("--output", default="full_list.txt", help="Output file for generated emails")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable rejection logging")

args = parser.parse_args()

# ---- USER INPUT FOR DOMAIN ----
domain_input = input("Enter email domain (example: outlook.com): ").strip().lower()

# ---- RUN TOOL ----
emails, rejected = generate_emails_from_file(
    args.input,
    args.output,
    domain_input,
    verbose=args.verbose
)

print(f"\n✔ {len(emails)} email addresses forged and saved to '{args.output}'")

if args.verbose:
    print(f"⚠ {len(rejected)} entries rejected (see 'rejected_log.txt')")

print("🔥 MailForge execution complete.")
