from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

PROMISED_DOWN = 100
PROMISED_UP = 35

class InternetSpeedTwitterBot:
    def __init__(self, twitter_handle):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.down = None
        self.up = None
        self.twitter_handle = twitter_handle
    def repost_top_4(self, account):
        # Navigate to the account's page
        self.driver.get(f"https://twitter.com/{account}")
        time.sleep(5)

        # Find the top 4 posts
        posts = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='tweet']"))
        )[:4]

        for post in posts:
            # Click the repost (retweet) button
            repost_button = post.find_element(By.CSS_SELECTOR, "[data-testid='retweet']")
            repost_button.click()

            # Click the "Repost" option in the popup menu
            repost_confirm = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
            )
            repost_confirm.click()

            time.sleep(2)  # Wait a bit between reposts

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(5)  

        go_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        go_button.click()

        time.sleep(60)

        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text

    def tweet_at_provider(self):
        # if float(self.down) < PROMISED_DOWN or float(self.up) < PROMISED_UP:
            self.driver.get("https://x.com/login")

            sign_in_element = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Sign in')]"))
            )
            sign_in_element.click()

            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_field.send_keys("gadrielwarhammer@gmail.com", Keys.RETURN)

            try:
                password_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                password_field.send_keys("Jumbotron98", Keys.RETURN)

            except TimeoutException:
                username_field_2 = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]'))
                )
                username_field_2.send_keys('gadrielwar345', Keys.RETURN)

                password_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                password_field.send_keys("Jumbotron98", Keys.RETURN)

                time.sleep(5)

            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")))

            tweet_box.send_keys(f"{self.twitter_handle} @DeonMen is one of the most talented coders  "
                                f"your guaranteed money")
            tweet_box.send_keys(Keys.CONTROL, Keys.ENTER)
    def like_top_4_comments(self, tweet_url):
        try:
            self.driver.get(tweet_url)
            time.sleep(5)

            # Scroll down to load comments
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Increased wait time after scrolling

            liked_count = 0
            max_attempts = 10
            attempts = 0

            while liked_count < 4 and attempts < max_attempts:
                try:
                    # XPath for like buttons, modified to select multiple buttons
                    like_buttons = self.driver.find_elements(By.XPATH, 
                        "//div[@data-testid='cellInnerDiv']//article//div[@data-testid='like']")

                    for like_button in like_buttons:
                        if liked_count >= 4:
                            break

                        try:
                            # Check if the tweet is already liked
                            aria_label = like_button.get_attribute("aria-label")
                            if "Liked" not in aria_label:
                                like_button.click()
                                print(f"Liked comment {liked_count + 1}")
                                liked_count += 1
                                time.sleep(2)  # Wait between likes
                            else:
                                print(f"Comment {liked_count + 1} was already liked")
                        except Exception as e:
                            print(f"Error liking a comment: {e}")

                    if liked_count < 4:
                        # Scroll again to load more comments
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)

                except NoSuchElementException:
                    print("No more like buttons found.")
                    break

                attempts += 1

            if liked_count < 4:
                print(f"Only managed to like {liked_count} comments.")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.save_screenshot("error.png")
        # else:
        #     self.driver.get("https://x.com/login")

        #     sign_in_element = WebDriverWait(self.driver, 30).until(
        #         EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Sign in')]"))
        #     )
        #     sign_in_element.click()

        #     username_field = WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.NAME, "text"))
        #     )
        #     username_field.send_keys("gadrielwarhammer@gmail.com", Keys.RETURN)

        #     try:
        #         password_field = WebDriverWait(self.driver, 10).until(
        #             EC.presence_of_element_located((By.NAME, "password"))
        #         )
        #         password_field.send_keys("Jumbotron98", Keys.RETURN)

        #     except TimeoutException:
        #         username_field_2 = WebDriverWait(self.driver, 10).until(
        #             EC.presence_of_element_located((
        #                 By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]'))
        #         )
        #         username_field_2.send_keys('FnaticOdt', Keys.RETURN)

        #         password_field = WebDriverWait(self.driver, 10).until(
        #             EC.presence_of_element_located((By.NAME, "password"))
        #         )
        #         password_field.send_keys("Jumbotron98", Keys.RETURN)

        #         time.sleep(5)

        #     tweet_box = WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")))
      
        #     tweet_box.send_keys(f"@{self.twitter_handle} My internet speed is excellent today! "
        #                         f"Download Speed: {self.down}Mbps, Upload Speed: {self.up}Mbps. Keep up the good work!")
        #     tweet_box.send_keys(Keys.CONTROL, Keys.ENTER)
        

bot = InternetSpeedTwitterBot("@elonmusk")
# bot.get_internet_speed()
print(f"Download Speed: {bot.down}Mbps")
print(f"Upload Speed: {bot.up}Mbps")
bot.tweet_at_provider()
# bot.repost_top_4("DeonMen")
bot.like_top_4_comments("https://x.com/DeonMen/status/1729334024026608058")
