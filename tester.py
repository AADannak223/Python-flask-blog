import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_blog(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("programmers", driver.title)

        try:

            about = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ab"))
            )
            about.click()
            time.sleep(2)

            contact = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ct"))
            )
            contact.click()

            name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
            )
            name.clear()
            name.send_keys("omkar Dannak")
            time.sleep(1)

            email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
            )
            email.clear()
            email.send_keys("aadannak@gmail.com")
            time.sleep(1)

            phone = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "phone"))
            )
            phone.clear()
            phone.send_keys("9112622263")
            time.sleep(1)

            message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "message"))
            )
            message.clear()
            message.send_keys("Hello I am omkar.")
            time.sleep(1)

            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sendMessageButton"))).click()

            admin_dashboard = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ad"))
            )
            admin_dashboard.click()
            time.sleep(3)
            assert "Admin Login" in driver.page_source

            username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "floatingInput"))
            )
            username.clear()
            username.send_keys("omkardannak24@gmail.com")
            

            password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "floatingPassword"))
            )
            password.clear()
            password.send_keys("adiraj123")
            time.sleep(1)
            password.send_keys(Keys.RETURN)
            
            add_new_post = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "anp"))
            )
            add_new_post.click()
            
            title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "title"))
            )
            title.clear()
            title.send_keys("What is WSGI?" )
            
            subtitle = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "subtitle"))
            )
            subtitle.clear()
            subtitle.send_keys("Web Server Gateway Interface")

            slug = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "slug"))
            )
            slug.clear()
            slug.send_keys("new-post")

            content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "content"))
            )
            content.clear()
            content.send_keys("WSGI refers to Web Server Gateway Interface. WSGI plays a vital role at the time when you deploy your Django or Flask application. Here, in this blog, I will be discussing what WSGI is, when should you dive deeper into the concept of WSGI and how does WSGI works.WSGI refers to Web Server Gateway Interface. WSGI plays a vital role at the time when you deploy your Django or Flask application. Here, in this blog, I will be discussing what WSGI is, when should you dive deeper into the concept of WSGI and how does WSGI works.")
           


            # WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.NAME, "file1"))).click
            # time.sleep(5)
            




        finally:
            driver.quit()



    
if __name__ == "__main__":
    unittest.main()