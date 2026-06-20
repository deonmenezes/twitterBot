# twitterBot

A Python automation bot that uses Selenium to interact with Twitter/X — checking internet speeds via Speedtest.net and tweeting the results, as well as reposting top tweets from specified accounts.

## Tech Stack

- **Language:** Python 3
- **Automation:** Selenium WebDriver (Chrome)
- **Browser Driver:** ChromeDriver (must be installed separately)

## Setup

1. Install Python 3.
2. Install Selenium:
   ```bash
   pip install selenium
   ```
3. Ensure ChromeDriver is installed and on your PATH (must match your Chrome browser version).
4. Set your Twitter credentials in the script (see `main.py` for the entry point).

## Build / Run / Test

```bash
# Run the bot
python twitterBot/main.py
```

## Project Structure

```
twitterBot/
  main.py       # Entry point — configures and runs the bot
  twitBot.py    # Core bot class (InternetSpeedTwitterBot) with Selenium logic
  error.png     # Screenshot captured on error (auto-generated)
```

## Architecture & Key Files

- `twitBot.py` defines the `InternetSpeedTwitterBot` class with methods for:
  - `get_internet_speed()` — opens Speedtest.net, waits for results, scrapes download/upload speeds.
  - Tweeting results at the ISP's Twitter handle if speeds are below promised thresholds.
  - `repost_top_4(account)` — reposts the top 4 tweets from a given account.
- `main.py` instantiates the bot and orchestrates the workflow.
- `PROMISED_DOWN = 100` and `PROMISED_UP = 35` (Mbps) are the thresholds hardcoded in `twitBot.py`.

## Conventions & Notes for Agents

- No `requirements.txt` is present; the only external dependency is `selenium`.
- The bot uses `webdriver.ChromeOptions` with `detach=True` so the browser stays open after the script exits.
- Twitter's DOM structure changes frequently; CSS selectors and `data-testid` attributes in `twitBot.py` may break on Twitter UI updates.
- No test suite is present.
- Twitter/X automation may violate platform terms of service — use responsibly.
