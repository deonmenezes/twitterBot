        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        import time
        import concurrent.futures

        class MultiAccountTwitterBot:
            def __init__(self, accounts):
                self.accounts = accounts
                self.drivers = []

            def setup_drivers(self):
                for _ in self.accounts:
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_experimental_option('detach', True)
                    driver = webdriver.Chrome(options=chrome_options)
                    self.drivers.append(driver)

            def login_account(self, driver, account):
                driver.get("https://x.com/login")

                sign_in_element = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Sign in')]"))
                )
                sign_in_element.click()

                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "text"))
                )
                username_field.send_keys(account['email'], Keys.RETURN)

                try:
                    password_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "password"))
                    )
                    password_field.send_keys(account['password'], Keys.RETURN)

                except TimeoutException:
                    username_field_2 = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]'))
                    )
                    username_field_2.send_keys(account['username'], Keys.RETURN)

                    password_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "password"))
                    )
                    password_field.send_keys(account['password'], Keys.RETURN)

                time.sleep(5)

            def login_all_accounts(self):
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.accounts)) as executor:
                    executor.map(self.login_account, self.drivers, self.accounts)

            def tweet_all(self, message):
                def tweet(driver, account_message):
                    tweet_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")))
                    tweet_box.send_keys(account_message)
                    tweet_box.send_keys(Keys.CONTROL, Keys.ENTER)

                with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.accounts)) as executor:
                    executor.map(tweet, self.drivers, [account['tweet_message'] for account in self.accounts])

            def repost_top_4_all(self):
                def repost_top_4(driver, account):
                    driver.get(f"https://twitter.com/{account['repost_account']}")
                    time.sleep(5)

                    posts = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='tweet']"))
                    )[:4]

                    for post in posts:
                        repost_button = post.find_element(By.CSS_SELECTOR, "[data-testid='retweet']")
                        repost_button.click()

                        repost_confirm = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
                        )
                        repost_confirm.click()

                        time.sleep(2)

                with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.accounts)) as executor:
                    executor.map(repost_top_4, self.drivers, self.accounts)

            def like_top_4_comments_all(self):
                def like_top_4_comments(driver, account):
                    driver.get(account['tweet_url'])
                    time.sleep(5)

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)

                    liked_count = 0
                    max_attempts = 10
                    attempts = 0

                    while liked_count < 4 and attempts < max_attempts:
                        try:
                            like_buttons = driver.find_elements(By.XPATH, 
                                "//div[@data-testid='cellInnerDiv']//article//div[@data-testid='like']")

                            for like_button in like_buttons:
                                if liked_count >= 4:
                                    break

                                try:
                                    aria_label = like_button.get_attribute("aria-label")
                                    if "Liked" not in aria_label:
                                        like_button.click()
                                        print(f"Liked comment {liked_count + 1} for {account['username']}")
                                        liked_count += 1
                                        time.sleep(2)
                                    else:
                                        print(f"Comment {liked_count + 1} was already liked for {account['username']}")
                                except Exception as e:
                                    print(f"Error liking a comment for {account['username']}: {e}")

                            if liked_count < 4:
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                time.sleep(2)

                        except NoSuchElementException:
                            print(f"No more like buttons found for {account['username']}.")
                            break

                        attempts += 1

                    if liked_count < 4:
                        print(f"Only managed to like {liked_count} comments for {account['username']}.")

                with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.accounts)) as executor:
                    executor.map(like_top_4_comments, self.drivers, self.accounts)

            def run(self):
                self.setup_drivers()
                self.login_all_accounts()
                
                # Example usage of the new methods
                self.tweet_all("This is a test tweet from all accounts!")
                self.repost_top_4_all()
                self.like_top_4_comments_all()

                # Close all browser windows
                for driver in self.drivers:
                    driver.quit()

        # Example usage
        accounts = [
            {
                'email': 'trevorphilent@gmail.com',
                'password': 'Autobots98',
                'username': '@trevorphilent',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'michaeldsouz345@gmail.com',
                'password': 'Jason345',
                'username': '@michaeldsouz345',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'franklinzu345@gmail.com',
                'password': 'Luciana345',
                'username': '@frankli69051824',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'lestercallcops@gmail.com',
                'password': 'Lossantos21',
                'username': '@lester1289074',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'jasontremor6@gmail.com',
                'password': 'Sora123345',
                'username': '@jasontremor6',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'lucianatremor6@gmail.com',
                'password': 'Chatgpt345',
                'username': '@lucianatremor6',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'wednesdayorteba@gmail.com',
                'password': 'Luciana345',
                'username': '@wednesdayorteba',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'alexanderz94219@gmail.com',
                'password': 'Luciana345',
                'username': '@alexanderz94219',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'caesarstrongtgt@gmail.com',
                'password': 'Luciana345',
                'username': '@caesar857608',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'georgecalister345@gmail.com',
                'password': 'Luciana345',
                'username': '@george877185371',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'lawrencecalister99@gmail.com',
                'password': 'Luciana345',
                'username': '@lawrence01631631',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'melwincalister@gmail.com',
                'password': 'Luciana345',
                'username': '@melwincalister',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'helencanister@gmail.com',
                'password': 'Luciana345',
                'username': '@helencanister',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'ivandragister@gmail.com',
                'password': 'Luciana345',
                'username': '@ivandragister',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'ronaldister@yahoo.com',
                'password': 'Luciana345#$%!',
                'username': '@ronaldister',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'loyalarence@outlook.com',
                'password': 'Luciana345',
                'username': '@loyalarence',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'lonalarence@outlook.com',
                'password': 'Luciana345',
                'username': '@lonalarence',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'joylingerry@outlook.com',
                'password': 'Luciana345',
                'username': '@joylingerry',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'jasmineivanister@outlook.com',
                'password': 'Luciana345',
                'username': '@jasmine44047081',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'jasmineivanister@outlook.com',
                'password': 'Luciana345',
                'username': '@jasonivanister',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'rudolphronaldister@outlook.com',
                'password': 'Luciana345',
                'username': '@rudolph1646991',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'royronaldister@outlook.com',
                'password': 'Luciana345',
                'username': '@royronaldister',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'rajronaldister@outlook.com',
                'password': 'Luciana345',
                'username': '@rajronaldister',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            },
            {
                'email': 'gadrielwarhammer@gmail.com',
                'password': 'Jumbotron98',
                'username': '@gadrielwar',
                'tweet_message': 'I heard you are a great man @DeonMen',
                'repost_account': 'DeonMen',
                'tweet_url': 'https://x.com/DeonMen/status/1729334024026608058'
            }
        ]

        bot = MultiAccountTwitterBot(accounts)
        bot.run()
