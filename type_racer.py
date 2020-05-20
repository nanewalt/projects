from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time

driver = webdriver.Chrome()

driver.get('https://play.typeracer.com')
wait = WebDriverWait(driver, 15)
play_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a')))
play_button.click()

element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'inputPanel')))
text = element.text

box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'txtInput')))
box.click()

FULL_SPEED = False
wpm = 99

if FULL_SPEED:
	pyautogui.write(text)
else:
	t = 60 / wpm
	for w in text.split():
		t1 = time.time()
		pyautogui.write(w + ' ')
		t2 = time.time()
		time.sleep(max(t-(t2-t1), 0))

time.sleep(5)
driver.quit()