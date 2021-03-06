# This script will automatically open chrome, create a new tab,
# then go to HoyoLab's daily forum rewards page
# It will then collect your daily reward for you
# And close the created tab
# NOTE: If your chosen browser is already open, ensure this script runs on the same monitor
#       The active browser window is on, otherwise it won't provide the desired result
from calendar import monthrange
from math import floor, ceil
import pyautogui as pag
import datetime as dt
import subprocess
import config
import shlex
import time


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
    i, x, y = 0, 0, 0
    searching = True
    try:
        # Search for today's reward
        rewards = list(pag.locateAllOnScreen('assets/indicator.png', grayscale=True, confidence=config.CONFIDENCE))

        # Account for UTC +8 Offset
        now = dt.datetime.utcnow() + dt.timedelta(hours=8)
        month_length = monthrange(now.year, now.month)[1]

        # If we didn't find any rewards, throw an error
        if rewards is None:
            raise pag.ImageNotFoundException('Could not locate rewards')
        # We found more rewards than actually exist, throw an error
        elif len(rewards) > month_length:
            raise pag.ImageNotFoundException('Too many rewards found')

        # We have not found today's reward on screen
        if now.day > len(rewards):
            while searching:
                # Scroll down to next row
                pag.scroll(-1 * config.VERTICAL_OFFSET)
                time.sleep(config.SHORT_LOAD)

                # Scan page again for rewards
                rewards = list(pag.locateAllOnScreen('assets/indicator.png', grayscale=True, confidence=config.CONFIDENCE))

                # If the day is on the screen
                # After scrolling, account for week lost in the view
                if now.day - (i * 7) <= len(rewards):
                    # Decrement index by one to account for list starting at 0 but days starting at 1
                    x, y = pag.center(rewards[(now.day % 7) - 1])
                    # Get number of rows on screen
                    rows_visible = ceil(len(rewards) / 7)

                    # Calculate the correct y to click at
                    # The y we get from center will go to shit
                    y = config.VERTICAL_OFFSET * rows_visible
                    searching = False

                # If we find more reward icons than days in the month something went wrong, throw error
                if len(rewards) > month_length or i > config.MAX_SEARCHES:
                    raise pag.ImageNotFoundException('Too many rewards found')
                # If we have searched x times and can't find it, throw error
                elif i > config.MAX_SEARCHES:
                    raise pag.ImageNotFoundException('Reward not found within search period')
                i += 1
        # Today's reward was within view at start
        else:
            # We know where today's icon is
            x, y = pag.center(rewards[now.day - 1])

        # Move cursor to location, accounting for specified offsets
        # Tween makes it look more human (kinda not really, but less bot-like)
        pag.moveTo(x + config.CLICK_X_OFFSET, y + config.CLICK_Y_OFFSET, duration=config.MOVEMENT_DURATION,
                   tween=pag.easeInOutExpo)

        print('Collected reward')
    except pag.ImageNotFoundException as infe:
        # The indicator was not found
        pag.alert("Today's reward could not be found. Have you already claimed it?")

        # Save error to console
        print(infe)

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

    # Perform any necessary actions to collect reward
    collect_reward()

    # Wait x seconds after collecting reward
    time.sleep(config.CONFIRM_LOAD)

    print('Closing website')
    destroy_page()


# Run at least once, on start
main()

while config.RUN_DAILY:
    print(f'Going to sleep. Next run in {config.RUN_INTERVAL} hours')
    # Calculate how long to wait until next execution
    # Account for UTC + 8 Offset
    now = dt.datetime.utcnow() + dt.timedelta(hours=8)
    tomorrow = now + dt.timedelta(days=config.RUN_INTERVAL)
    time.sleep((tomorrow - now).total_seconds())

    # Run script
    main()
