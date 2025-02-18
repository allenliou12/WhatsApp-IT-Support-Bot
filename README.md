# WhatsApp IT Support Bot

An automated WhatsApp Web bot that handles IT support requests and ticket management using Selenium WebDriver.

## Features

- Automated response to incoming WhatsApp messages
- Ticket creation and management system
- Support for multiple issue categories:
  - Hardware Issues
  - Network Issues
  - Account/Password Issues
  - Software Issues
  - Other Issues
- Excel-based ticket tracking
- Automated notification system for IT support team
- Handling of both new issues and existing ticket inquiries

## Prerequisites

- Python 3.x
- Chrome Browser
- ChromeDriver (automatically managed by webdriver_manager)

## Installation

1. Clone the repository
```bash
git clone https://github.com/allenliou12/WhatsApp-Bot
cd WhatsApp-Bot
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Create an Excel file named "Examply.xlsx" in the project directory with the following columns:
   - Ticket No
   - Contact Details
   - Issue
   - Description
   - Status
   - Date created

## Usage

1. Run the script:
```bash
python app.py
```

2. Scan the WhatsApp QR code when prompted to log in to WhatsApp Web

3. The bot will automatically:
   - Monitor for new messages
   - Respond to support requests
   - Create tickets
   - Notify support team

## Configuration

- Modify `GROUP_TO_NOTIFY` in the code to set the WhatsApp contact/group for IT support notifications
- Adjust `MAX_RETRIES` to change the maximum number of retry attempts for user inputs
- Customize response messages in the `handle_conversation()` and `handle_new_issue()` functions

## Logging

The application logs all activities to:
- Console output
- `support_bot_test.log` file

## Dependencies

- selenium
- webdriver_manager
- pandas
- openpyxl
- logging

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

- Selenium WebDriver for web automation
- WhatsApp Web for the messaging platform
- Pandas for Excel file handling

## Disclaimer

This bot is for educational purposes only. Please ensure you comply with WhatsApp's terms of service when using automated systems.