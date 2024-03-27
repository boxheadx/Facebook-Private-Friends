from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import sys
import base64 
import json

EMAIL = 'your-email'
PASSWORD = 'your-password'

driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications") 
options.add_argument("--window-size=1366,768")
options.add_argument("--start-maximized")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get('https://facebook.com')

def login(username, password):
	driver.find_element(By.ID, 'email').send_keys(username)
	driver.find_element(By.ID, 'pass').send_keys(password)
	driver.find_element(By.NAME, 'login').click()


login(EMAIL, PASSWORD)

time.sleep(10)

driver.get(str(sys.argv[1]))

time.sleep(10)

driver.find_element(By.XPATH, "//div[@aria-label='See Options']").click()
friendship = driver.find_element(By.XPATH, "//a[contains(@href, 'friendship')]")
TARGET_UID = re.search(r'/(\d+)/$', (friendship.get_attribute('href'))).group(1)

print(f'Fetched target UID: {TARGET_UID}')

payload = '{"friends:0":"{\\"name\\":\\"users_friends_of_people\\",\\"args\\":\\"%s\\"}"}' % TARGET_UID.strip()
encoded_payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')

print(f'Payload generated: {encoded_payload}')


def check_for_new_elements(last_count):
    current_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com')]"))
    return current_count > last_count

remove_substring = lambda str1, str2: str1.replace(str2, "")


friends = []

def getFriends(letter):
	driver.get(f"https://www.facebook.com/search/people/?q={letter}&filters={encoded_payload}")
	last_element_count = 0
	while True:
	    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
	    time.sleep(2) 
	    
	    if not check_for_new_elements(last_element_count):
	        break
	    
	    last_element_count = len(driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com/')]"))

	elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com/')]")

	for element in elements:
	    if('login_alerts' not in str(element.get_attribute('href') or 'notifications' not in str(element.get_attribute('href') or '__tn__=%3C' not in str(element.get_attribute('href'))))):
	    	friends.append(remove_substring(remove_substring(str(element.get_attribute('href')), '?__tn__=%3C'), '&__tn__=%3C'))

try:
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.TAG_NAME, "input"))
    )
    print("Fetching all the friends...")
    print("(This may take a while)")

    count = 1
    for l in range(97,123):
    	getFriends(chr(l))
    	print(f"{count} chunk fetched")
    	count += 1

except Exception as e:
    print("timed out:", e)


friends = list(set(friends))

output_file = open(f'{TARGET_UID}.txt', 'w')

for f in friends:
	output_file.write(f + '\n')

print(f'The list has been saved to {TARGET_UID}.txt file')

driver.quit()