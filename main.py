# This script will automatically open chrome, create a new tab,
# then go to HoyoLab's daily forum rewards page
# It will then collect your daily reward for you
# And close the created tab
# NOTE: If your chosen browser is already open, ensure this script runs on the same monitor
#       The active browser window is on, otherwise it won't provide the desired result
from calendar import monthrange
import pyautogui as pag
from math import floor
import datetime as dt
import subprocess
import config
import shlex
import time

# TODO: Run on it's own and sleep while waiting


# Complete prepwork needed to collect reward
def setup_page():
    # Move cursor to center of page, this ensures it will scroll properly
    pag.moveTo(pag.size().width / 2, pag.size().height / 2)

    # Scroll down to get the full calendar in view
    pag.scroll(-1 * (floor(pag.size().height / 2)) + config.BOOTSTRAP_HEIGHT)

    time.sleep(config.SHORT_LOAD)

    # Zoom out x steps to get the full calendar in view
    for i in range(config.ZOOM_STEP):
        pag.hotkey('ctrlleft', '-')


# Destroy the open page and reset any changes made
def destroy_page():
    # Zoom back to the user's original zoom level
    for i in range(config.ZOOM_STEP):
        pag.hotkey('ctrlleft', '+')

    # Chrome hotkey to close tab
    pag.hotkey('ctrlleft', 'w')


# Locate and drag the cursor to today's reward
def find_reward():
    searching = True
    i = 0
    try:
        # Search for today's reward, 0.75 confidence required or it breaks (idk)
        rewards = list(pag.locateAllOnScreen('assets/indicator.png', confidence=0.75))
        print(len(rewards))
        now = dt.datetime.utcnow()

        # If we didn't find any rewards, or too many rewards throw an error
        if rewards is None or len(rewards) > monthrange(now.year, now.month)[1]:
            raise pag.ImageNotFoundException

        # We cannot see today's reward on the screen
        if now.day > len(rewards):
            while searching:
                # Scroll down to next row
                pag.scroll(-1 * config.VERTICAL_OFFSET)
                time.sleep(config.SHORT_LOAD)

                # Scan page again for rewards
                rewards = list(pag.locateAllOnScreen('assets/indicator.png', confidence=0.5))

                # If the day is on the screen
                if now.day <= len(rewards):
                    searching = False
                    # x, y = pag.center(rewards[now.day - 1])
                    # pag.moveTo(x, y)
                # If we find more reward icons than days in the month something went wrong, throw error
                # If we have searched three times and can't find it, give up
                if len(rewards) > monthrange(now.year, now.month)[1] or i > config.MAX_SEARCHES:
                    raise pag.ImageNotFoundException
                i += 1

        # We know where today's icon is
        x, y = pag.center(rewards[now.day - 1])

        # Move cursor to location, accounting for specified offsets
        # Tween makes it look more human (kinda not really, but less bot-like)
        pag.moveTo(x + config.CLICK_X_OFFSET, y + config.CLICK_Y_OFFSET, duration=config.MOVEMENT_DURATION,
                   tween=pag.easeOutQuad)

        print('Collected reward')
    except pag.ImageNotFoundException:
        # The indicator was not found
        pag.alert("Today's reward could not be found. Have you already claimed it?")

        # Reset the user's zoom
        for i in range(config.ZOOM_STEP):
            pag.hotkey('ctrlleft', '+')

        print('Collection failed, aborting...')

        # Close the current tab
        pag.hotkey('ctrlleft', 'w')
        # Exit the program
        exit()


# Handle confirming and collecting reward
def collect_reward():
    # Clicking opens confirmation menu
    pag.click()


def main():
    print('Opening website...')

    # Open chrome as a subprocess using the current user accounts
    # Theoretically this works with any browser, only tested with Chrome
    proc = subprocess.Popen(shlex.split(rf'"{config.BROWSER}" "{config.URL}"'))

    # Wait x seconds to make sure the page loads
    time.sleep(config.TIME_LOAD_PAGE)
    # Kill the subprocess, it's no longer needed
    proc.kill()

    # Now that the page is loaded, prepare it
    setup_page()

    # Wait x second(s) after setup for safetyyyyyy
    time.sleep(config.SHORT_LOAD)

    # Go to today's reward location on screen
    find_reward()

    # Click the cursor to claim the daily reward
    pag.click()

    # Wait x seconds after collecting reward
    time.sleep(config.CONFIRM_LOAD)

    print('Closing website')
    destroy_page()

# Run at least once, on start
main()

while config.RUN_DAILY:
    print(f'Going to sleep. Next run in {config.RUN_INTERVAL} hours')
    # Calculate how long to wait until next execution
    now = dt.datetime.utcnow()
    tomorrow = now + dt.timedelta(days=config.RUN_INTERVAL)
    time.sleep((tomorrow - now).total_seconds())

    # Run script
    main()
