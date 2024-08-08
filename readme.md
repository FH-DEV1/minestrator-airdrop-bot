# Minestrator Airdrop Bot

This Python script automates the process of fetching and redeeming codes from the Minestrator airdrop events. The bot continuously monitors the next airdrop time, retrieves codes from a specified Discord channel, and attempts to redeem them on the Minestrator website.

## Features
- Fetches the latest airdrop time from the Minestrator website.
- Retrieves the latest codes from a Discord channel.
- Redeems the codes automatically at the scheduled airdrop time.
- Logs activities and errors for easy debugging.

## Requirements
- Python 3.x
- Required Python packages (listed in `requirements.txt`):
  - `requests`
  - `beautifulsoup4`

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/FHDEV1/minestrator-airdrop-bot.git
   cd minestrator-airdrop-bot
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `config.json` file with the following content:
   ```
   {
       "discord_token": "YOUR_DISCORD_TOKEN",
       "session_id": "YOUR_SESSION_ID",
       "redeem_token": "YOUR_REDEEM_TOKEN"
   }
   ```

5. Update the script with the path to the `config.json` file if needed.

## Usage
1. Ensure all required environment variables and headers are set in the `config.json` file.
2. Run the bot using the provided Python3 file (for Windows users):
   ```
   Python3 main.py
   ```

## Configuration
The script reads configuration values from `config.json`:
- `discord_token`: The authorization token for accessing the Discord API.
- `session_id`: The session ID cookie for the Minestrator website.
- `redeem_token`: The token used in the payload for redeeming codes on the Minestrator website.

## Notes
- Ensure your Discord authorization token is kept secure and not shared publicly.
- This script is for educational purposes. Use it responsibly and adhere to the terms and conditions of the respective services.

## License
This project is licensed under the MIT License.

---

Feel free to customize and improve the bot according to your needs. Contributions are welcome! If you encounter any issues, please open an issue on the GitHub repository.