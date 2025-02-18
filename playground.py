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

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('support_bot.log'),
#         logging.StreamHandler()
#     ]
# )

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
        print(f"Failed to initialize driver: {str(e)}")
        return None

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
        print("Login successfully")
        return True

    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False

def search(driver, contact_to_search):
    """
    Search for a specific contact and open the conversation

    Args:
    contact_to_search = Contact to search duhhh
    """

    try:
        print("Looking for search input box...")
        # Wait for the message input box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "selectable-text"
            ))
        )

        time.sleep(3)
        search_box.clear()
        print(f"Searching for {contact_to_search}")
        search_box.send_keys(contact_to_search)
        time.sleep(2)
        select_first_search(driver)
        return True
    except Exception as e:
        print("Error" , e)
        return False

def close_search_box(driver):
    print("Closing search box...")
    close_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[aria-label= 'Cancel search']"
            ))
        )
    close_search.click()
    print("Search box closed!")
    
def select_first_search(driver):
    """
    Click on the first searched conversation
    """
    try:
        print("Opening conversation for searched")
        searched_contact = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, 'matched-text'
            ))
        )
        
        searched_contact.click()
        print("Searched conversation opened!")
        time.sleep(5)
        return True
        
    except Exception as e:
        print("Searched contact not clicked", e)
        return False

def send_message(driver, message):
    """
    Sends a message in the current chat

    Args:
    message: The message to be sent out
    """
    try:
        print("Looking for message input box...")
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
        print("Message sent!")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send message: {str(e)}")
        return False

def close_chat(driver):
    """
    Close the current conversation
    """
    try:
        print("Opening chat menu...")
        triple_dot_button = driver.find_element(By.XPATH, "//*[@id='main']/header/div[3]/div/div[3]/div/button")
        triple_dot_button.click()
        print("Chat menu open!")

        close_chat_button = driver.find_element(By.XPATH, "//*[@aria-label='Close chat']")
        print("Closing chat....")
        close_chat_button.click()
        print("Exited chat")
        return True
    except Exception as e:
        print(e)
        return False

def notify_group(driver,message):
    GROUP_TO_NOTIFY = "THM IT Team"
    search(driver,GROUP_TO_NOTIFY)
    select_first_search(driver)
    time.sleep(5)
    send_message(driver,message)
    close_chat(driver)
    close_search_box(driver)


def main():
    d = None
    try:
        print("Initializing Chrome...")
        d = initialize_driver()
        if not d:
            print("Failed to initialize Chrome driver")
            return

        # Open WhatsApp Web
        print("Opening WhatsApp Web...")
        d.get('https://web.whatsapp.com')

        check_login(d)
        print("Waiting for page to load completely...")
        time.sleep(5)

        contact_name = search(d,"TH IT Allen Liou")
        close_search_box(d)
    
    except Exception as e:
        print(f"Critical error occurred: {str(e)}")
    finally:
        if d:
            print("Closing browser in 10 seconds...")
            time.sleep(10)
            d.quit()

if __name__ == "__main__":
    main()