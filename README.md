# Telegram Member Manager

A tool for managing Telegram group members, allowing you to scrape members from one group and add them to another.

## Setup Instructions

1. Install Termux from F-Droid or Google Play Store
2. Open Termux and run the following commands:
```bash
pkg install git
git clone [your-repository-url]
cd [repository-name]
chmod +x setup.sh
./setup.sh
```

3. Get your Telegram API credentials:
   - Go to https://my.telegram.org
   - Log in with your phone number
   - Click on 'API Development Tools'
   - Create a new application
   - Copy your API ID and API Hash

4. Edit config.ini:
   - Replace YOUR_API_ID with your actual API ID
   - Replace YOUR_API_HASH with your actual API Hash

## Usage

Run the script:
```bash
python scraper.py
```

The script provides two main functions:
1. Scrape members from a group
2. Add scraped members to another group

## Features

- Scrape members from any accessible Telegram group
- Save member data to CSV files
- Add members to target groups with customizable delays
- Handle Telegram's flood and privacy restrictions
- Colorful terminal interface

## Configuration

Edit config.ini to customize:
- API credentials
- Wait time between actions
- Number of members to add
- Time between member additions

## Files Description

- scraper.py: Main script
- config.ini: Configuration file
- setup.sh: Setup script for Termux
- requirements.txt: Python package dependencies
- data.csv: Stores scraped member data
- clone.csv: Backup of scraped data
- username.csv: Username list
- phone.csv: Phone number list
- BanNumbers.csv: List of banned phone numbers

## Warning

Use this tool responsibly and in accordance with Telegram's terms of service. Excessive use may result in account limitations or bans.
