import path

import json
import requests
from git import Repo
from apscheduler.schedulers.blocking import BlockingScheduler

def regenerate_easylist():
    
    # Fetch the EasyList file
    def fetch_easylist():
        url = "https://easylist.to/easylist/easylist.txt"
        response = requests.get(url)

        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print("Failed to fetch EasyList.")
            return []

    # Function to remove non-ASCII characters from the URL pattern
    def remove_non_ascii(url):
        return ''.join([ch for ch in url if ord(ch) < 128])

    # Convert EasyList lines to DeclarativeNetRequest format
    def convert_to_declarative_net_request(easylist_lines):
        rules = []
        rule_id = 1  # Start rule IDs from 1

        for line in easylist_lines:
            line = line.strip()
            if line.startswith("!") or not line:  # Skip comments and empty lines
                continue

            # Remove non-ASCII characters from the rule
            sanitized_rule = remove_non_ascii(line)

            # Convert the sanitized rule into DeclarativeNetRequest format
            rule = {
                "id": rule_id,
                "priority": 1,  # Default priority
                "action": {
                    "type": "block"
                },
                "condition": {
                    "urlFilter": sanitized_rule,
                    "resourceTypes": ["main_frame", "sub_frame", "script", "image", "stylesheet", "object", "font"]
                }
            }
            rules.append(rule)
            rule_id += 1  # Increment rule ID for each new rule

        return rules

    # Save the rules to a JSON file
    def save_to_json(rules, filename="rules.json"):
        with open(filename, "w") as f:
            json.dump(rules, f, indent=4)

    # Main process
    easylist_lines = fetch_easylist()
    rules = convert_to_declarative_net_request(easylist_lines)
    save_to_json(rules)

    print("DeclarativeNetRequest rules.json file generated.")
    push_to_github()

# Function to push the updated rules.json to GitHub
def push_to_github():
    repo_path = path.PATH  # Path to your local Git repository. Change this to work on your computer
    repo = Repo(repo_path)
    
    # Add the changes to Git
    repo.git.add('rules.json')
    
    # Commit the changes
    repo.git.commit('-m', 'Update rules.json with the latest Easylist filters')
    
    # Push the changes to GitHub
    origin = repo.remote(name='origin')
    origin.push()
    
    print("Successfully pushed changes to GitHub.")

# Run the script immediately once to fetch and push for the first time
regenerate_easylist()