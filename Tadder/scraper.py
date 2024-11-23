from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import time
import random
from colorama import init, Fore
import traceback

init()

# Read config
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
time_wait = int(config['Settings']['time_wait'])
members_to_add = int(config['Settings']['members_to_add'])
time_between_adds = int(config['Settings']['time_between_adds'])

class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    RESET = Fore.RESET
    BLUE = Fore.BLUE

def print_colored(text, color):
    print(f"{color}{text}{Colors.RESET}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
    ╔════════════════════════════════════════╗
    ║        Telegram Member Manager         ║
    ╚════════════════════════════════════════╝
    """
    print_colored(banner, Colors.BLUE)

def get_input(prompt):
    return input(f"{Colors.BLUE}{prompt}{Colors.RESET}")

def scrape_members():
    clear_screen()
    print_banner()
    
    print_colored("\n[1] Scraping members...", Colors.GREEN)
    
    client = TelegramClient("session/scraper", api_id, api_hash)
    client.connect()
    
    if not client.is_user_authorized():
        phone = get_input("\nEnter your phone number with country code: ")
        client.send_code_request(phone)
        client.sign_in(phone, get_input('\nEnter the verification code: '))
    
    result = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    
    groups = []
    for chat in result.chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue
    
    print_colored("\nChoose a group to scrape members from:", Colors.GREEN)
    for i, g in enumerate(groups):
        print(f'{i}. {g.title}')
    
    g_index = int(get_input("\nEnter group number: "))
    target_group = groups[g_index]
    
    print_colored(f"\nFetching members from {target_group.title}...", Colors.GREEN)
    all_participants = client.get_participants(target_group)
    
    print_colored("\nSaving members to data.csv...", Colors.GREEN)
    with open("data.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user_id', 'access_hash', 'group'])
        
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            writer.writerow([username, user.id, user.access_hash, target_group.title])
    
    print_colored("\nMembers scraped successfully!", Colors.GREEN)
    client.disconnect()

def add_members():
    clear_screen()
    print_banner()
    
    print_colored("\n[2] Adding members...", Colors.GREEN)
    
    client = TelegramClient("session/adder", api_id, api_hash)
    client.connect()
    
    if not client.is_user_authorized():
        phone = get_input("\nEnter your phone number with country code: ")
        client.send_code_request(phone)
        client.sign_in(phone, get_input('\nEnter the verification code: '))
    
    # Load members from data.csv
    users = []
    with open('data.csv', encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)  # skip the headers
        for row in rows:
            user = {
                'username': row[0],
                'user_id': int(row[1]),
                'access_hash': int(row[2])
            }
            users.append(user)
    
    # Load target group
    print_colored("\nChoose a group to add members to:", Colors.GREEN)
    groups = []
    chats = client.get_dialogs()
    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue
    
    for i, group in enumerate(groups):
        print(f'{i}. {group.title}')
    
    g_index = int(get_input("\nEnter group number: "))
    target_group = groups[g_index]
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
    
    print_colored("\nAdding members...", Colors.GREEN)
    n = 0
    for user in users:
        n += 1
        if n > members_to_add:
            print_colored("\nMember adding limit reached!", Colors.RED)
            break
        
        try:
            user_to_add = InputPeerUser(user['user_id'], user['access_hash'])
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print_colored(f"Successfully added {user['username']}", Colors.GREEN)
            time.sleep(random.randrange(time_between_adds))
        
        except PeerFloodError:
            print_colored("\nGetting Flood Error from Telegram. Waiting...", Colors.RED)
            time.sleep(time_wait)
        except UserPrivacyRestrictedError:
            print_colored(f"User {user['username']} has privacy restriction", Colors.RED)
            continue
        except PhoneNumberBannedError:
            print_colored("\nYour phone number is banned!", Colors.RED)
            break
        except Exception as e:
            print_colored(f"Error: {str(e)}", Colors.RED)
            continue
    
    client.disconnect()

def main():
    while True:
        clear_screen()
        print_banner()
        
        print("\nOptions:")
        print("1. Scrape members")
        print("2. Add members")
        print("3. Exit")
        
        choice = get_input("\nEnter your choice: ")
        
        if choice == "1":
            scrape_members()
        elif choice == "2":
            add_members()
        elif choice == "3":
            print_colored("\nGoodbye!", Colors.BLUE)
            sys.exit()
        else:
            print_colored("\nInvalid choice!", Colors.RED)
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    # Create session directory if it doesn't exist
    if not os.path.exists("session"):
        os.makedirs("session")
    main()
