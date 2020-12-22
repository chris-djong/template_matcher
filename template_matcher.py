import mss
import cv2
import time
import numpy as np

detection_threshold = 0.9
placing_bets = False

# Open all the templates
place_bet_template = cv2.imread("./images/bet_placing_template.png")
place_bet_template_gray = cv2.cvtColor(place_bet_template, cv2.COLOR_BGR2GRAY)

number_templates = []
for i in range(37):
    filename = "./images/%d.png" % i
    template = cv2.imread(filename)
    number_templates.append(template)

""" Places the required bets by pressing on the correct screen location """
def place_bets(sct, current_bet):
    print("Placing bets")
    return None

""" Function that checks what the previous win was 
    Returns the number together with its color as either 'r' or 'b' """
def check_winner(sct):
    # First define the window in which the status update are visible
    monitor = {'left': 1300, 'top': 200, 'width': 500, 'height': 100}

    img = sct.grab(monitor)
    mss.tools.to_png(img.rgb, img.size, output="last_wins.png")
    last_wins_window = cv2.imread("last_wins.png")

    # Match to the screen capture and find the location with the highest match
    matches = []
    for template in number_templates:
        match_res = cv2.matchTemplate(last_wins_window, template, cv2.TM_CCOEFF)
        _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
        matches.append([max_val, max_loc])

    matches = np.array(matches)
    best_match = np.argmax(matches[:, 0])
    print(matches)
    print("Found %d as winner" % best_match)

    number = 0
    color = 'b'
    return number, color

""" Returns 1 in case we are allowed to place our bets else 0 """
def obtain_status(sct):
    # First define the window in which the status update are visible
    monitor = {'left': 700, 'top': 900, 'width': 600, 'height': 180}

    img = sct.grab(monitor)
    mss.tools.to_png(img.rgb, img.size, output="status_window.png")
    status_window = cv2.imread("status_window.png")
    status_window_gray = cv2.cvtColor(status_window, cv2.COLOR_BGR2GRAY)

    # Match to the screen capture and find the location with the highest match
    match_res = cv2.matchTemplate(status_window_gray, place_bet_template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)

    # In case we have a threshold detection above the current one then we know that we are placing our bets
    if max_val > 0.9:
        return True
    else:
        return False

desired_color = 'r'
current_bet = 1
old_status = False
switched = False  # to find out whether we are in the same status as before or whether we have switches statusses
# Start recording the screen and keep recording it
with mss.mss() as sct:
    while True:
        # First find out whether we have switched to a new state or not
        status = obtain_status(sct)
        # In case we have switched to the place_bet status we start our logic
        if status != old_status and status == 1:
            winning_number, winning_color = check_winner(sct)
            # In case we won set the bet back to 1
            if winning_color == desired_color:
                current_bet = 1
            # In case we lost multiply the bet by 2
            else:
                current_bet *= 2

            # Then we can place the bets
            place_bets(sct, current_bet)

        # Update the old_status for this loop
        old_status = status

        # Sleep for a second as a higher framerate is not required
        time.sleep(1)




