import requests
import re
import json
from pystyle import Colorate, Colors, Center, Anime

class EmailVerifier:
    def __init__(self, api_key, domains):
        self.headers = {"apikey": api_key}
        self.payload = {}
        self.char_combinations = [".", "-", "_", ""]
        self.domain_combinations = domains
        self.emails = []
    def is_valid_email(self, email):
        pattern = r"^\S+@\S+\.\S+$"
        if re.match(pattern, email):
            return email
        else:
            return None
    def verify_email(self, email):
        if email:
            url = f"https://api.apilayer.com/email_verification/check?email={email}"
            try:
                response = requests.get(url, headers=self.headers, data=self.payload, timeout=2)
                status_code = response.status_code
                if status_code == 402:
                    print(Colors.red + "Invalid API key" + Colors.reset)
                elif status_code == 429:
                    print(Colors.red + "Request limit reached" + Colors.reset)
                elif status_code != 200:
                    quit()
                print(Colorate.Horizontal(Colors.yellow_to_red, f"Verifying email: {email}", 1) + Colors.reset)
                data = json.loads(response.text)
                return data.get("smtp_check", False)
            except requests.Timeout:
                return False
    
    def validate_name(self, first_name, last_name):
        for char in self.char_combinations:
            for domain in self.domain_combinations:
                email_combination1 = f"{first_name}{char}{last_name}@{domain}"
                email_combination2 = f"{last_name}{char}{first_name}@{domain}"
                if self.verify_email(email_combination1):
                    self.emails.append(email_combination1)
                    print(Colorate.Horizontal(Colors.blue_to_green, f"[+] {email_combination1}", 1) + Colors.reset)
                if self.verify_email(email_combination2):
                    self.emails.append(email_combination2)
                    print(Colorate.Horizontal(Colors.blue_to_green, f"[+] {email_combination2}", 1) + Colors.reset)
        return self.emails if self.emails else None
    
    def validate_pseudonym(self, pseudonym):
        for domain in self.domain_combinations:
            email = f"{pseudonym}@{domain}"
            if self.verify_email(email):
                self.emails.append(email)
                print(Colorate.Horizontal(Colors.blue_to_green, f"[+] {email}", 1) + Colors.reset)
        return self.emails if self.emails else None
    
def get_api_key():
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
            return data.get("api_key", None)
    except FileNotFoundError:
        return None

def get_domains():
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
            return data.get("domains", None)
    except FileNotFoundError:
        return None

def main():
    api_key = get_api_key()
    if not api_key or api_key=="":
        print("Please provide a valid API key in a file named config.json.")
        return
    domains = get_domains()
    if not domains or domains==[]:
        print("Please provide a valid list of domains in a file named config.json.")
        return
    email_verifier = EmailVerifier(api_key, domains)
    banner = """
  ██████ ▄▄▄█████▓ ▒▄██████▄   ██▓     ██ ▄█▀
▒██    ▒ ▓  ██▒ ▓▒▒██▒ ▄▄▄░ █▒▓██▒     ██▄█▒ 
░ ▓██▄   ▒ ▓██░ ▒░▒██░█  █▄▀ ▒▒██░    ▓███▄░ 
  ▒   ██▒░ ▓██▓ ░ ▒██ ▒▀▀ ▒▄█░▒██░    ▓██ █▄ 
▒██████▒▒  ▒██▒ ░ ░  ██████▓▒░░██████▒▒██▒ █▄
▒ ▒▓▒ ▒ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▒ ▓▒
░ ░▒  ░ ░    ░      ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒ ▒░
░  ░  ░    ░      ░ ░ ░ ▒    ░ ░   ░ ░░ ░ 
      ░               ░ ░      ░  ░░  ░   
                                          """
    Anime.Fade(Center.Center(banner), Colors.red_to_yellow, Colorate.Diagonal, enter=True)
    name = input(Colors.dark_green + "Enter (\"First-Name Last-Name\") or (Pseudonym) or ([Email]) >> " + Colors.gray)
    print(Colors.blue + "\nVerifying...\n" + Colors.reset)
    if name.startswith("\"") and name.endswith("\""):
        first_name, last_name = name[1:-1].split(" ")
        email = email_verifier.validate_name(first_name, last_name)
    elif name.startswith("[") and name.endswith("]"):
        email = email_verifier.verify_email(name)
    else:
        email = email_verifier.validate_pseudonym(name)
    if email:
        print(Colors.green + "\nValid email(s) found:" + Colors.reset)
        for mails in email:
            print(Colorate.Horizontal(Colors.blue_to_green, f"- {mails}", 1) + Colors.reset)
        input("\n")
    else:
        print("No valid email was found")

if __name__ == "__main__":
    main()
