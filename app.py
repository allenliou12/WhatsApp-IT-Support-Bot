from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
from datetime import datetime
import sys
import random
import logging
import os

# Change the working directory to the script's folder
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)  # Set script directory as the working directory

# Define the log file path correctly
log_file_path = os.path.join(script_dir, 'support_bot_test.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',  # Specify the desired time format
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

def initialize_driver():
    """
    Setup the driver
    """
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize driver: {str(e)}")
        return None
    
def wait_for_user_reply(driver, timeout=30):
    """
    Waits for a new user message for a given timeout by checking if the
    number of incoming messages has increased. Avoids issues where
    a new reply has the same text as a previous message.
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Max time to wait for a response (default: 30 seconds)
        
    Returns:
        str: The text content of the latest message, or None if no new message appears.
    """
    start_time = time.time()
    # Get the count of incoming messages before waiting.
    messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]//span[contains(@class, 'selectable-text')]")
    initial_count = len(messages)
    
    while time.time() - start_time < timeout:
        logging.info("Waiting for user reply...")
        time.sleep(1)  # check more frequently
        messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]//span[contains(@class, 'selectable-text')]")
        if len(messages) > initial_count:
            new_msg = messages[-1].text.strip()
            logging.info(f"New message detected: '{new_msg}'")
            return new_msg

    return None  # No new message received

def close_chat(driver):
    """
    Close the current conversation
    """
    try:
        logging.info("Opening chat menu...")
        triple_dot_button = driver.find_element(By.XPATH, "//*[@id='main']/header/div[3]/div/div[3]/div/button")
        triple_dot_button.click()
        logging.info("Chat menu open!")

        close_chat_button = driver.find_element(By.XPATH, "//*[@aria-label='Close chat']")
        logging.info("Closing chat....")
        close_chat_button.click()
        logging.info("Exited chat")
        return True
    except Exception as e:
        logging.error({str(e)})
        return False

def check_login(driver, timeout=30):
    """
    Checks if the login is successful by waiting for the presence of an element.

    Args:
    driver: Selenium WebDriver instance
    timeout: Maximum time to wait for the element to appear
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.ID, "pane-side")))
        logging.info("Login successfully")
        return True

    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        return False
        
def click_unread_button(driver):
    """
    Click the unread button to go to the unread messages tab
    """
    try:
        logging.info("Looking for unread button...")
        time.sleep(5)
        check_input = driver.find_element(By.XPATH, "//*[@id='unread-filter']")
        logging.info("Unread button found!")
        check_input.click()
        return True
    
    except Exception as e:
        logging.error(f"Failed to click unread_button{str(e)}")
        return False

def select_first_unread(driver):
    """
    Click on the first unread conversation from the unread tab
    """
    try:
        logging.info("Looking for unread messages...")
        unread_msg = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div[1]/div/div")
        unread_msg.click()
        time.sleep(5)
        return True
        
    except Exception:
        logging.warning("No unread messages")
        return False

def send_message(driver, message):
    """
    Sends a message in the current chat

    Args:
    message: The message to be sent out
    """
    try:
        logging.info("Looking for message input box...")
        # Wait for the message input box
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"
            ))
        )
        
        # Type and send message
        message_box.clear()
        message_box.send_keys(message)
        time.sleep(3)
        message_box.send_keys(Keys.ENTER)
        logging.info("Message sent!")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send message: {str(e)}")
        return False

def search(driver, contact_to_search):
    """
    Search for a specific contact and open the conversation

    Args:
    contact_to_search = Contact to search duhhh
    """

    try:
        logging.info("Looking for search input box...")
        # Wait for the search input box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "selectable-text"
            ))
        )

        time.sleep(3)
        search_box.clear()
        logging.info(f"Searching for {contact_to_search}")
        search_box.send_keys(contact_to_search)
        time.sleep(2)
        select_first_search(driver)

    except Exception as e :
        logging.error({str(e)})

def close_search_box(driver):
    """
    Close the search box
    """
    try:
        logging.info("Closing search box...")
        close_search = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, "[aria-label= 'Cancel search']"
                ))
            )
        time.sleep(2)
        close_search.click()
        logging.info("Search box closed!")
    except Exception as e:
        logging.error({str(e)})
    
def select_first_search(driver):
    """
    Click on the first searched conversation
    """
    try:
        logging.info("Opening conversation for searched")
        searched_contact = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, 'matched-text'
            ))
        )
        
        searched_contact.click()
        logging.info("Searched conversation opened!")
        time.sleep(5)
        
    except Exception as e:
        logging.error({str(e)})

def get_contact_details(driver):
    """
    Extracts the contact details of the current chat, gets the name if the contact is saved, or the contact number if the contact is not saved

    Returns:
    The name of the current selected chat
    """

    try:
        logging.info("Extracting contact details...")
        name_element = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div/div/div/span')
        contact_name = name_element.text
        logging.info(f"Contact Number: {contact_name}")
        return contact_name

    except NoSuchElementException as e:
        logging.error("Cannot find element", {str(e)})
        return False

    except Exception:
        logging.error("Couldn't fetch the phone number. It might be hidden or the XPath is outdated.")
        return False

def get_next_ticket_number(excel_file):
    """
    Extract the last ticket number from the excel file and increment it

    Returns:
    A number based on the last created ticket
    """
    try:
        # Read the existing Excel file
        existing_excel = pd.read_excel(excel_file)
        
        # Check if the "Ticket No" column exists
        if "Ticket No" not in existing_excel.columns:
            return 1  # If no tickets exist, start from 1
        
        # Extract the last ticket number and increment it
        last_ticket_number = existing_excel["Ticket No"].iloc[-1]  # Get the last ticket number
        last_ticket_number = int(last_ticket_number.lstrip('#'))  # Remove the '#' and convert to int
        return last_ticket_number + 1
    
    except FileNotFoundError:
        logging.warning(f"Error: The file {excel_file} does not exist.")
        return 1  # Start from 1 if file doesn't exist
    
    except ValueError:
        logging.warning("Error: There is invalid data in the 'Ticket No' column.")
        return 1  # Start from 1 in case of invalid data
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return 1  # Start from 1 in case of any other errors

def create_ticket(contact_number, issue_category, issue_description):
    """
    Creates a ticket and saves it to an Excel file with auto-adjusted column widths.
    """
    EXISTING_FILE = os.path.join(script_dir, "Examply.xlsx")
    current_time = datetime.now()

    try:
        logging.info("Creating ticket....")
        # Get the next ticket number
        n = get_next_ticket_number(EXISTING_FILE)
        ticket_num = f"#{n:05d}"  # Format with leading zeros

        # Create the new ticket
        new_ticket = {
            "Ticket No": ticket_num,
            "Contact Details": contact_number,
            "Issue": issue_category,
            "Description": issue_description,
            "Status": "Ongoing",
            "Date created": current_time.strftime("%d/%m/%Y, %H:%M")
        }

        # Read existing Excel file or create a new DataFrame
        existing_excel = pd.read_excel(EXISTING_FILE)

        # Append the new ticket
        new_row = pd.DataFrame([new_ticket])
        updated_excel = pd.concat([existing_excel, new_row], ignore_index=True)

        # Save the updated DataFrame with auto column width
        with pd.ExcelWriter(EXISTING_FILE, engine="openpyxl") as writer:
            updated_excel.to_excel(writer, index=False, sheet_name="Tickets")
            worksheet = writer.sheets["Tickets"]

            # Auto-adjust column widths
            for col in worksheet.columns:
                max_length = 0
                col_letter = col[0].column_letter  # Get column letter
                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                worksheet.column_dimensions[col_letter].width = max_length + 2  # Add padding

        logging.info(f"Ticket created for {contact_number}, ticket num: {ticket_num}")
        return ticket_num  # Return the generated ticket number

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False

def handle_conversation(driver):
    """
    Handles the initial conversation and directs the user accordingly.
    """
    name = get_contact_details(driver)
    if name == "TH IT Allen Liou":
        close_chat(driver)
    else:
        MESSAGE = ("Thanks for contacting TH IT Support! Could you please let us know what you need help with?\n"
                " Reply 1️⃣ for a **new issue**\n"
                " Reply 2️⃣ for an **update on an existing issue**\n"
                " Type 'exit' to cancel this request.")
        logging.info("Sending template msg to check if new or old issue")
        send_message(driver, MESSAGE)

        # last_seen_msg = wait_for_user_reply(driver)  # Store last seen message
        start_time = time.time()
        retries = 0

        while retries < MAX_RETRIES:
            reply = wait_for_user_reply(driver, timeout=30)  # Wait for a response

            if reply:  
                if reply.lower() == "exit":
                    send_message(driver, "Your request has been canceled. Let us know if you need anything else.")
                    close_chat(driver)
                    logging.info("Conversation exited due to user request")
                    return  # Exit conversation
                    
                elif reply == "1":
                    logging.info("New issue report")
                    handle_new_issue(driver)
                    return  # Exit after handling

                elif reply == "2":
                    logging.info("Assisting to check for existing issue")
                    handle_existing_issue(driver,get_contact_details(driver))
                    return  # Exit after handling

                else:
                    retries += 1
                    if retries < MAX_RETRIES:
                        send_message(driver, f"Invalid response. You have {MAX_RETRIES - retries} attempts left. Please reply '1' for a **new issue**, '2' for an **update**, or 'exit' to cancel.")
                    else:
                        send_message(driver, "We couldn't understand your response. Please restart the conversation if you still need assistance.")
                        close_chat(driver)
                        logging.info("Conversation ended due to user sending messages in wrong format after max retries")
                        return  # Exit after max retries

            elif time.time() - start_time > 60:
                send_message(driver, "We haven't received a response. Please reply '1' for a new issue, '2' for an update, or 'exit' to cancel.")
                start_time = time.time()  # Reset timer to avoid spamming
                retries += 1

            close_chat(driver)  # Close the chat if max retries exceeded
        
MAX_RETRIES = 3
def handle_new_issue(driver):
    """
    Handle new issue flow while ensuring proper wait time for user response.
    """
    MESSAGE = ("We apologize for any inconvenience caused. "
               "Before going further, could you please tell us what kind of problem you are facing? \n"
               "Please reply:\n"
               "1️⃣ for **HARDWARE** Issues\n"
               "2️⃣ for **NETWORK** Issues\n"
               "3️⃣ for **ACCOUNT/PASSWORD** Issues\n"
               "4️⃣ for **SOFTWARE** Issues\n"
               "5️⃣ for **OTHERS**\n"
               "or Type 'exit' to cancel this request.")
    
    logging.info("Sending template msg to get category of issue")
    send_message(driver, MESSAGE)
    
    # Wait for and handle user reply
    retries = 0
    while retries < MAX_RETRIES:
        category_reply = wait_for_user_reply(driver, timeout=30)  # Wait for user reply

        if category_reply:
            category_reply = category_reply.strip().lower()  # Normalize reply

            # Check if user wants to exit
            if category_reply == "exit":
                send_message(driver, "Your request has been canceled. Let us know if you need anything else.")
                logging.info("Exiting conversation due to user request")
                close_chat(driver)
                return  # Exit function

            # If the user responds with a valid category (1-5)
            if category_reply in CATEGORY_MAP:
                issue_category = CATEGORY_MAP[category_reply]

                # Prompt for issue description
                logging.info("Getting brief description of issue faced...")
                send_message(driver, "Thank you! Could you please provide a brief description of the issue in one message?")
                issue_description = wait_for_user_reply(driver, timeout=90)  # Wait for user to describe issue
                if not issue_description:
                    send_message(driver, "It seems we didn't receive a description. Proceeding with ticket creation.")
                    issue_description = "No description provided."

                # Create ticket with category and description
                contact_num = get_contact_details(driver)
                ticket_num = create_ticket(contact_number=contact_num, 
                                           issue_category=issue_category, 
                                           issue_description=issue_description)

                if ticket_num:
                    send_message(driver, "Thank you for providing the details.\n"
                                         f"A ticket has been created for you.\n"
                                         f"Your ticket number is {ticket_num}.")
                    send_message(driver, "Please wait while we arrange for IT support to contact you.")
                else:
                    send_message(driver, "Sorry, we encountered an error while creating your ticket. Please try again later.")
                
                close_chat(driver)
                MESSAGE = (
                f"{contact_num} is in need of help! \n"
                f"Category: {issue_category} \n"
                f"Description of issue: {issue_description} \n"
                f"Ticket No: {ticket_num} \n"
                "Please send assistance"
                )

                click_unread_button(driver)
                notify_group(driver,MESSAGE)
                return  # Exit function after successful handling

            else:
                retries += 1
                if retries < MAX_RETRIES:
                    send_message(driver, f"Invalid response. You have {MAX_RETRIES - retries} attempts left. Please reply with '1' for **Hardware Issues**, '2' for **Network Issues**, '3' for **Account/Password Issues**, '4' for **Software Issues**, '5' for **Others** or 'exit' to cancel.")
                else:
                    send_message(driver, "Sorry, we couldn't understand your response. Please restart the conversation if you need help.")
                    close_chat(driver)
                    logging.info("Conversation exited after max retries")
                    return  # Exit after max retries

    close_chat(driver)  # Close the chat if max retries exceeded

def handle_existing_issue(driver,contact_num):
    """
    Handle existing issue flow
    """
    name = get_contact_details(driver)
    df = pd.read_excel("Examply.xlsx")
    filtered_df = df[(df["Contact Details"] == contact_num) & (df["Status"] == "Ongoing")]
    MESSAGE = (f"You currently have {len(filtered_df)} unresolved ticket \n"
               f"{filtered_df['Ticket No'].to_list()} \n"
               "Can you please tell us which ticket are you referring to?\n"
               "Please reply the ticket no only, Thank you")
    send_message(driver, MESSAGE)
    reply = wait_for_user_reply(driver,40)
    logging.info("Sent msg to update current number of unresolved ticket for the user")
    MESSAGE = ("Thank you for your reply \n"
               "Please hold which we get an IT support to assist you")
    send_message(driver, MESSAGE)
    close_chat(driver)
    click_unread_button(driver)

    MESSAGE = (f"{name} has contacted me to ask about ticket no:{reply} \n"
               "Please send someone to assist")
    notify_group(driver, MESSAGE)
    return

def notify_group(driver,message):
    """
    Send notification to someone 
    """
    GROUP_TO_NOTIFY = "Allen"
    search(driver,GROUP_TO_NOTIFY)
    time.sleep(5)
    send_message(driver,message)
    close_chat(driver)
    time.sleep(1)
    # close_search_box(driver)

CATEGORY_MAP = {
    "1": "Hardware",
    "2": "Network",
    "3": "Account/Password",
    "4": "Software",
    "5": "Others"
}


def main():
    driver = None
    try:
        logging.info("Initializing Chrome...")
        driver = initialize_driver()
        if not driver:
            logging.warning("Failed to initialize Chrome driver")
            return

        # Open WhatsApp Web
        logging.info("Opening WhatsApp Web...")
        driver.get('https://web.whatsapp.com')

        check_login(driver)
        logging.info("Waiting for page to load completely...")
        time.sleep(5)

        while True:
            try:
                # First check for unread messages
                click_unread_button(driver)
                
                # Try to select first unread conversation
                if select_first_unread(driver):
                    # Process the conversation (your existing message handling code)
                    handle_conversation(driver)
                    # click_unread_button(driver)
                    # After handling the conversation, check for unread messages again
                    logging.info("Checking for more unread messages...")
                    
                else:
                    logging.info("No unread conversations found, waiting before next check...")
                    time.sleep(random.randint(2, 30))
                    click_unread_button(driver)
                             
            except NoSuchElementException as e:
                logging.error(f"Element not found: {str(e)}")
                time.sleep(random.randint(2, 30))
            except Exception as e:
                logging.error(f"Unexpected error: {str(e)}")
                time.sleep(random.randint(2, 30))

    except Exception as e:
        logging.error(f"Critical error occurred: {str(e)}")
    finally:
        if driver:
            logging.info("Closing browser in 10 seconds...")
            time.sleep(10)
            driver.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()