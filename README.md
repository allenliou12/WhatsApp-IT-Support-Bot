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
- MySQL database integration for ticket tracking
- Automated notification system for IT support team
- Handling of both new issues and existing ticket inquiries
- Configurable group chat filtering
- Detailed logging system

## Prerequisites

- Python 3.x
- Chrome Browser
- ChromeDriver (automatically managed by webdriver_manager)
- MySQL Server
- WhatsApp Web account

## Installation

1. Clone the repository

```bash
git clone https://github.com/allenliou12/WhatsApp-Bot
cd WhatsApp-Bot
```

2. Install required packages

```bash
pip install pipenv
pipenv install
```

3. Set up environment variables by creating a `.env` file with:

```
HOST=your_mysql_host
USER=your_mysql_user
PASSWORD=your_mysql_password
DATABASE=your_database_name
```

4. Set up MySQL database with the required table:

```sql
CREATE TABLE tickets (
    ticket_no INT AUTO_INCREMENT PRIMARY KEY,
    contact_details VARCHAR(255),
    issue_category VARCHAR(50),
    description TEXT,
    status VARCHAR(20),
    date_created DATETIME
);
```

## Configuration

- Modify `GROUPTOBEIGNORED` list to specify which group chats to ignore
- Adjust `MAX_RETRIES` (default: 3) to change the maximum number of retry attempts
- Customize response messages in the message templates
- Configure logging settings in the logging.basicConfig section

## Usage

1. Run the script:

```bash
python app.py
```

2. Scan the WhatsApp QR code when prompted to log in to WhatsApp Web

3. The bot will automatically:
   - Monitor for new messages
   - Respond to support requests
   - Create tickets in MySQL database
   - Notify support team
   - Handle existing ticket inquiries

## Logging

The application logs all activities to:

- Console output
- `support_bot_test.log` file in the script directory
- Includes timestamps, log levels, and detailed error messages

## Dependencies

- selenium
- webdriver_manager
- mysql-connector-python
- python-dotenv
- logging

## Error Handling

The bot includes comprehensive error handling for:

- Database connection issues
- WebDriver initialization failures
- Message sending failures
- User input validation
- Connection timeouts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Troubleshooting

Common issues and solutions:

- If the bot fails to initialize, check your Chrome/ChromeDriver versions
- For database connection issues, verify your .env configuration
- If messages aren't being sent, ensure your WhatsApp Web session is active
- For logging issues, check file permissions in the script directory

## Acknowledgments

- Selenium WebDriver for web automation
- WhatsApp Web for the messaging platform
- MySQL for database management

## Disclaimer

This bot is for educational purposes only. Please ensure you comply with WhatsApp's terms of service when using automated systems. The developer (Liou Jun Yi) not responsible for any misuse or violation of WhatsApp's terms of service.
