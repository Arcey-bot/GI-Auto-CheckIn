# GI-Auto-CheckIn
GI Auto Checkin is a program is a script meant to automatically collect daily rewards for Genshin's online check-ins.
The rewards are not worth the time of actually collecting manually, so I wasted a lot more time creating this instead!

A majority of settings are customizable, and can be changed in config.py based on how fast or slow your PC runs.
Note: In testing, I found the website to be unreliably slow at times. Because of this, I have set the default
    value for TIME_LOAD_PAGE to a higher than desireable amount.

The script will automatically launch a chrome tab (or instance if necessary) and connect to the desired website.
It will then claim your daily reward, and close the created tab.

To use other browsers, replace the path in BROWSER with a path to your browser of choice, then pray it works.
This should work on any resolution screen, it has only been tested on 2560x1440p though.

The script will NOT run in the background and execute as needed. It is expected for this to be launched manually
or from the Windows Task Scheduler as needed.

I am not responsible for anything that may happen to you, your system, or your account as a result of using this script.
# USE AT YOUR OWN RISK!
