URL = "https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us"
BROWSER = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
BOOTSTRAP_HEIGHT = 50  # Pixels tall the bootstrap header is
HORIZONTAL_OFFSET = 150  # Empty space horizontally between icons
VERTICAL_OFFSET = 275  # Empty space vertically between bottom icons
CLICK_Y_OFFSET = -100  # Offset the cursor vertically before clicking (pos down, neg up)
CLICK_X_OFFSET = 0  # Offset cursor horizontally before clicking (pos right, neg left)
MOVEMENT_DURATION = 0.69  # Number of seconds it takes to move the cursor to its target location (nice)
TIME_LOAD_PAGE = 3  # Seconds to wait for page to load
CONFIRM_LOAD = 1  # Seconds to wait for confirm dialog to appear
SHORT_LOAD = 0.75  # Seconds to wait between performing actions (i.e. clicking, dragging)
ZOOM_STEP = 0  # Steps to zoom the browser in/out by (Steps to get browser to 100% magnification)
RUN_DAILY = True  # Keep the script sleeping in background and run at the same time daily
RUN_INTERVAL = 24  # Hours to wait before running script again (Default is 24 hours/1 day)
MAX_SEARCHES = 3  # Maximum times to scroll down searching for rewards before quitting
CONFIDENCE = 0.75  #  The confidence with which LocateAllOnScreen() should search