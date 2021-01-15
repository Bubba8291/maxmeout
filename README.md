# maxmeout
Send a Discord webhook request when AirPods Max are in stock at your local Apple Store!

<p align="center">
  <img src="https://github.com/Bubba8291/maxmeout/raw/main/assets/running_screenshot.png" />
</p>

### Instructions
By using this software, you agree to the terms in the `LICENSE` file.
1. Download the repository and modify the `main.py` for the Discord webhook information. You'll need a Discord webhook url and your Discord ID (if you want to get pinged when there's stock).
2. You'll also need to get the page URL of the store you want to monitor (the script will automatically monitor (up to) the 11 nearest stores to that store as well). To do that, go to the page on the Apple website for your store (you can just google "apple \<location\>") and copy the URL. For example, the Apple Park Visitor Center store page is https://www.apple.com/retail/appleparkvisitorcenter/.
3. Install the dependency for the code. There is only one: `requests` for fetching inventory data from Apple's website and sending a Discord webhook request when there's stock.<br>`$ pip3 install requests`
4. Now you're ready to run the script! Once you downloaded this repository, open a terminal window, and `cd` to where you've downloaded the code. This should be the same directory where `main.py` is. Run the script with:<br><br>```$ python3 main.py --store_url STORE_URL --models MODELS_TO_WATCH```<br><br>replacing `STORE_URL` with the store page url you noted down in step 2, and `MODELS_TO_WATCH` with a comma separated of the list of colors you want to monitor: `space_gray`, `silver`, `green`, `sky_blue`, `pink`.<br><br>For example, to monitor for space gray, silver, and sky blue availability at Apple Park Visitor Center:<br>`$ python3 main.py --store_url https://www.apple.com/retail/appleparkvisitorcenter/ --models space_gray,silver,sky_blue`<br>If you want to change the amount of time before it checks the store again, add to the script run command `--sleep_time TIME_IN_SECONDS` to modify it.<br>The script will keep repeatedly checking until you terminate it, so now get back to doing whatever you were doing before! If inventory is found, it'll let you know on the Discord webhook you setup in step 1.

Good luck, and happy hunting!

Special thank to tonypeng for making the original script :)