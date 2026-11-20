import time

import pyperclip
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = uc.Chrome(version_main=157)


def ask(prompt: str) -> str:
    try:
        driver.get("https://chatgpt.com")
        wait = WebDriverWait(driver, 12)

        textarea = wait.until(EC.element_to_be_clickable((By.ID, "mobile-composer-prompt")))
        textarea.clear()
        textarea.send_keys(prompt)

        send_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Gửi tin nhắn"], button.xgrdywr')
            )
        )
        send_button.click()

        wait = WebDriverWait(driver, 12)
        copy_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '(//button[@aria-label="Copy response"])[last()]')
            )
        )

        time.sleep(0.5)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", copy_btn)
        time.sleep(0.5)
        copy_btn.click()

        time.sleep(1)
        content = pyperclip.paste()
        return content
    finally:
        driver.quit()
