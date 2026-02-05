#!/usr/bin/env python3

import sys
import argparse

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

    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            for line in file:
                original_name = line.strip()
                
                if not original_name:
                    if verbose:
                        rejected.append((original_name, "Empty line"))
                    continue

                # Clean name for processing
                clean_name = original_name.lower()

                if clean_name == "linkedin member":
                    if verbose:
                        rejected.append((original_name, "LinkedIn Member"))
                    continue

                if clean_name == "anonymous user":
                    if verbose:
                        rejected.append((original_name, "Anonymous user"))
                    continue

                parts = original_name.split()

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

                # isalpha() will fail on names like "O'Connor" or "Smith-Jones"
                # If you want to allow those, you'd need a different check.
                if not (first_name.isalpha() and last_name.isalpha()):
                    if verbose:
                        rejected.append((original_name, "Non-alphabetic characters in name"))
                    continue

                email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
                emails.append(email)

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

    # -------- ARGUMENT PARSING --------
    parser = argparse.ArgumentParser(description="MailForge - Email Generator Tool")
    parser.add_argument("--input", required=True, help="Input file containing raw names")
    parser.add_argument("--output", default="full_list.txt", help="Output file for generated emails")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable rejection logging")

    args = parser.parse_args()

    # ---- USER INPUT FOR DOMAIN ----
    domain_input = input("Enter email domain (example: outlook.com): ").strip().lower()
    if not domain_input:
        print("Error: Domain cannot be empty.")
        sys.exit(1)

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
