# This script will automatically open chrome, create a new tab,
# then go to HoyoLab's daily forum rewards page
# It will then collect your daily reward for you
# And close the created tab
# NOTE: If your chosen browser is already open, ensure this script runs on the same monitor
#       The active browser window is on, otherwise it won't provide the desired result
import pyautogui as pag
from math import floor
import subprocess
import config
import shlex
import time

# TODO: Screen independent?


# Complete prepwork needed to collect reward
def setup_page():
    # Move cursor to center of page, this ensures it will scroll properly
    pag.moveTo(pag.size().width / 2, pag.size().height / 2)

    # Scroll down to get the full calendar in view
    pag.scroll(-1 * (floor(pag.size().height / 2)) + config.BOOTSTRAP_HEIGHT)


# Locate and drag the cursor to today's reward
def goto_reward():
    try:
        # Search for the top_indicator to find today's reward
        reward = pag.locateCenterOnScreen('assets/top_indicator.png')

        # If we didn't find a reward, throw an error
        if reward is None:
            raise pag.ImageNotFoundException

        # Move cursor to location, accounting for specified offsets
        # Tween makes it look more human (kinda not really, but less bot-like)
        pag.moveTo(reward.x + config.CLICK_X_OFFSET, reward.y + config.CLICK_Y_OFFSET, duration=config.MOVEMENT_DURATION,
                   tween=pag.easeOutQuad)
    except pag.ImageNotFoundException:
        # The indicator was not found
        pag.alert("Today's reward could not be found. Have you already claimed it?")
        # Close the current tab
        pag.hotkey('ctrlleft', 'w')
        # Exit the program
        exit()


# Handle confirming and collecting reward
def collect_reward():
    # Clicking opens confirmation menu
    pag.click()

    # Wait x second(s) for confirmation to load
    time.sleep(config.SHORT_LOAD)

    # TODO: Confirmation?


def main():
    # Open chrome as a subprocess using the current user accounts
    # Theoretically this works with any browser, only tested with Chrome
    proc = subprocess.Popen(shlex.split(rf'"{config.BROWSER}" "{config.URL}"'))

    # TODO: Way to see if page is loaded?
    # Wait x seconds to make sure the page loads
    time.sleep(config.TIME_LOAD_PAGE)
    # Kill the subprocess, it's no longer needed
    proc.kill()

    # Now that the page is loaded, prepare it
    setup_page()

    # Wait x second(s) after setup for safetyyyyyy
    time.sleep(config.SHORT_LOAD)

    # Go to today's reward location on screen
    goto_reward()

    # Click the cursor to claim the daily reward
    pag.click()

    # Wait x seconds after moving to hopefully guarantee collection
    time.sleep(config.SHORT_LOAD)
    # Chrome hotkey to close tab
    pag.hotkey('ctrlleft', 'w')


main()
