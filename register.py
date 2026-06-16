import sys
import os
import subprocess

def add_player():
    # 1. Ensure correct inputs are passed via CMD
    if len(sys.argv) < 3:
        print("\n❌ Error: Missing arguments!")
        print("Usage: python register.py \"Player_Name\" [league / knockout / bet]")
        print("Example: python register.py \"Anil_eFoot\" league\n")
        return

    player_input = sys.argv[1]
    category = sys.argv[2].lower()

    # 2. Determine target formatting and hooks
    if category == "league":
        hook = ""
        new_line = f"                <li>{player_input}</li>"
    elif category == "knockout":
        hook = ""
        new_line = f"                <li>{player_input}</li>"
    elif category == "bet":
        hook = ""
        # Expects input format like "Kiran_PES for Rs 100" for bet categories
        if " for " in player_input:
            name, amt = player_input.split(" for ", 1)
            new_line = f"                <li><strong>{name}</strong> is challenging for <strong>{amt}</strong></li>"
        else:
            new_line = f"                <li><strong>{player_input}</strong> is actively challenging</li>"
    else:
        print("❌ Invalid category! Choose 'league', 'knockout', or 'bet'.")
        return

    # 3. Read index.html and insert the data
    html_file = "index.html"
    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found in this folder.")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    if hook not in content:
        print(f"❌ Error: Code hook {hook} is missing inside index.html!")
        return

    # Insert the new player right under the matching hook marker
    updated_content = content.replace(hook, f"{hook}\n{new_line}")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"✅ Successfully added {player_input} to {category} slots locally!")

    # 4. AUTOMATIC GIT PUSH: Execute system commands automatically
    print("🚀 Pushing updates directly to GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Automated registration: {player_input} ({category})"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("💯 100/100! Your live page is officially updated.")
    except subprocess.CalledProcessError as e:
        print("⚠️ HTML updated locally, but Git push ran into an issue. Check your connection or Git settings.")

if __name__ == "__main__":
    add_player()