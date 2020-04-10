# Zoom-bot
This script attends your zoom meetings automatically at a specified time.

This has only been tested on mac so it might require a bit of tweaking before it works on linux or windows.

___

## Instructions

### Step 1: Installation
This script requires python3 and chrome installed on your system.

Then, clone or download the repo to your system.

After that, run the following command on your terminal

'''python
>>> pip3 install selenium

'''
This should have everything set up to run the python script

### Step 2: Fill out info

Open the <mark>zoom_bot_prod.py</mark> file and update the following variables with relevant info.

| Variable        | Description           |
| ------------- |:-------------:|
| USERNAME     | your zoom username |
| PASSWORD      | your zoom password      |  
| NAME | the name that will be shown in the meeting      |  
| zoom_key | your meeting key |
| zoom_password | your meeting password (leave blank if not required) |
| meeting_time | your meeting time (HH:MM:SS) |
| operating_system | choose between 'mac', 'windows' or 'linux' |

### Step 3: Run the script

Go to your terminal, navigate to the git directory and run the following command.

'''python
>>> python3 zoom_bot_prod.py

'''

This should start up the bot and as long as it is running in the background, it will automatically join your specified zoom meeting. It is recommended that you run the script once with you at your machine to take care of any unexpected inputs such as pop ups.
