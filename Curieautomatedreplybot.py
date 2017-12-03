'''
Made by @Locikll for Project Curie for Automated replies to dumb questions

Requires packages: 
pip install rocketchat_API
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
import time

from rocketchat_API.rocketchat import RocketChat

#Customizable Variables

# 5 Minute delay
delay = 5 * 60

#Customise message (Fixed flooding from replying to own messages)

#Direct Message on Join
DMMesage = "Welcome to the Curie Channel. First off, to avoid any confusion here, please make sure to read the pinned messages to the top right hand side of the group chat, especially the FAQ. If you're an author looking to promote yourself or your post, please don't post in #curie channel. Curie is a group for curators who find great content by others. Some information: \n 1.) To become a Curator you must be recommended by a current curator, please check the Steemit blog posts of 'Top Curators' to see if they have any public openings and how to apply. If they do not have any please do not bother them with unsolicited messages or by messaging the Curie group, doing so could ruin your reputation within the Curation community. \n 2.) DO NOT post any articles/posts in the Curie chat, or promote yourself as an author. This is *NOT* post promotion. \n 3.) If you've read all of this and the pinned messages then welcome, please feel free to learn more about the project by reading the; Curie blog, and Locikll (my creator's) Blog and if you have any further questions about the project (which are not covered by the FAQ pinned) please feel free to ask.  \n Have a wonderful day :) " 
#Error Message
messagetosend = 'You have received this error because you are not a recommended Curator, please click on the pin in the chatroom and read the FAQ. Only recommended curators can submit posts. This is an automated message, please do not reply.'
#Enquiry for Curator Message
enquirymessagetosend = 'To become a Curator you must be recommended, please read ALL information from the pinned notice at the right hand pannel. This is an automated message, have a nice day :)'

#Channel ID, Since most RocketCHATAPI Wrappers for Python suck dick, you have to create a new account, log into a channel and use list(rocket.channels_list_joined())   to find the channel ID of new channels to add. GGWP Python RocketChatAPI....
channelID = '6fQJWev8X8AHkeme9'

yourusername = 'curiereplybot'
password = ''

#Strings for Errors and enquiries, please use LOWER CASE for new messages.
enquirystring = ['how do i become a curator?','how do i become a curator','how do i become a curator','how to become curator','how to be a curator','how do you become recommended curator', 'become curator', 'can i submit','want to submit']
errorstring = ['1 minute', '1 minutes', '1min','1 min', 'post is too old','too old']


rocket = RocketChat(yourusername.lower(), password, server_url='https://steemit.chat/')

#Get Own User ID:
UID = rocket.me().json()['_id']

userhasbeenDMd = []

userrepliedtoGEN = []
userrepliedtoERR = []

#Set up Looped Function to continuously receive messages
def chatfeed():
    
    
    chathistory = rocket.channels_history(channelID,count=10).json()
    
    messages = chathistory.get('messages')
    message = messages[0]['msg']
    
    #print(message) #For Debugging purposes and to see message
    
    user = messages[0]['u']['username']
    
    if message == user and user not in userhasbeenDMd:
        #Find User ID:
        JoinUID = messages[0]['u']['_id']
        
        #Open Chat room with User and private message:
        
        print(rocket.chat_post_message(DMMesage,"@"+user).json())
        
        userhasbeenDMd.append(user)
        
        
    #Error Messages
    errorstringmessages = []
    
    for errmsg in range(0,len(errorstring)):
        iserrorstringinmessage = errorstring[errmsg] in message.lower()
        
        errorstringmessages.append(iserrorstringinmessage)
        
    #General Enquiries
    genenqmessages = []
    for enqmsg in range(0,len(enquirystring)):
        enqstringinmessage = enquirystring[enqmsg] in message.lower()
        genenqmessages.append(enqstringinmessage)
            
            
    
    if (True in errorstringmessages) and user != yourusername and (user not in userrepliedtoERR):
        
        print(rocket.chat_post_message("@"+user + " " + messagetosend, channel='curie').json()) 
        
        userrepliedtoERR.append(user)
        
    if (True in genenqmessages) and user != yourusername and (user not in userrepliedtoGEN):
        print(rocket.chat_post_message("@"+user + " " + enquirymessagetosend, channel='curie').json()) 
        
        userrepliedtoGEN.append(user)


if __name__ == "__main__":
    while True:
        try:
            chatfeed()
            time.sleep(delay)
        except (KeyboardInterrupt, SystemExit):
            print("Quitting...")
            break
        except Exception as e:
            print("### Exception Occurred: Restarting...")
