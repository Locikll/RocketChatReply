'''
Made by @Locikll for Project Curie for Automated replies to dumb questions
'''

import sys
import datetime
import os
import subprocess
import math
import re
from time import gmtime, strftime
import os.path
import timeit
import json

from rocketchat.api import RocketChatAPI

from rocketchat_API.rocketchat import RocketChat

#Customizable Variables

#Customise message (Fixed flooding from replying to own messages)
messagetosend = 'you have received this error because you are not a Curator, please click on the pin in the chatroom and read the FAQ. This is an automated message, please do not reply.'
yourusername = 'testrocketapi'
password = 'Somepasshere5443'

errorstring = ['1 minute', '1 minutes', '1min','1 min', 'post is too old','too old']


rocket = RocketChat(yourusername, password, server_url='https://steemit.chat/')


#Set up Looped Function to continuously receive messages
def chatfeed():

    chathistory = rocket.channels_history('6fQJWev8X8AHkeme9',count=1).json()
    
    messages = chathistory.get('messages')
    message = messages[0]['msg']
    
    #print(message) #For Debugging purposes and to see message
    
    user = messages[0]['u']['username']
    
    iserrorstringinmessage = [msg for msg in re.findall(r'\w+',message) if msg.lower() in errorstring]
    
    if not not iserrorstringinmessage and user != yourusername:
        
        print(rocket.chat_post_message("@"+user + " " + messagetosend, channel='curie').json()) 


if __name__ == "__main__":
    while True:
        try:
            chatfeed()
        except (KeyboardInterrupt, SystemExit):
            print("Quitting...")
            break
        except Exception as e:
            print("### Exception Occurred: Restarting...")