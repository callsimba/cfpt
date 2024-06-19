# Cryptocurrency Fraud Protection Tool

This tool is designed to help combat cryptocurrency fraud and theft by managing and rotating user agents, proxies, and mnemonic phrases. It features a graphical user interface (GUI) and a command-line interface (CLI) for versatility.

## Features

- **User-Agent Management**: Add, remove, and select user agents. Rotate user agents at a custom interval.
- **Proxy Management**: Add, remove, and activate/deactivate proxies. Rotate proxies along with user agents.
- **Mnemonic Management**: Add, remove, and select mnemonic phrases.
- **Browser Management**: Add and remove browsers. Open browsers with selected user agents and proxies.
- **Logging and Reporting**: Detailed logging and reporting capabilities. Send reports to a designated Telegram bot.
- **Settings Management**: Save and load settings to retain configuration between sessions.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/callsimba/cfpt.git
Navigate to the project directory:

bash
Copy code
cd cfpt
Install the required dependencies:

bash
Copy code
pip install ttkthemes telepot
Usage
GUI Mode
Run the following command to start the graphical user interface:

bash
Copy code
python src/main.py
CLI Mode
Use the following commands to run the tool in command-line interface mode:

User-Agent Management
Add a user agent:

bash
Copy code
python src/cli.py useragent add "Your User Agent String"
Remove a user agent:

bash
Copy code
python src/cli.py useragent remove "Your User Agent String"
List all user agents:

bash
Copy code
python src/cli.py useragent list
Proxy Management
Add a proxy:

bash
Copy code
python src/cli.py proxy add 192.168.1.1 8080 HTTP
Remove a proxy:

bash
Copy code
python src/cli.py proxy remove "192.168.1.1:8080 (HTTP)"
List all proxies:

bash
Copy code
python src/cli.py proxy list
Mnemonic Management
Add a mnemonic:

bash
Copy code
python src/cli.py mnemonic add "your mnemonic phrase"
Remove a mnemonic:

bash
Copy code
python src/cli.py mnemonic remove "your mnemonic phrase"
List all mnemonics:

bash
Copy code
python src/cli.py mnemonic list
Start the Tool
Start the tool:

bash
Copy code
python src/cli.py start
Contributing
Contributions are welcome! Please open an issue or submit a pull request.

License
This project is licensed under the MIT License.
