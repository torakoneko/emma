import json
import time
import random

from GUI import Window, Label, CheckBox, Button, application
from GUI.StdColors import grey
from colorama import init, Fore
init(autoreset = True)

import settings
import emma
import tumblrclient
import utilities

def run_emma():
    # If we aren't in chat mode, every 15 minutes, try to make a post. Replying to asks is most likely, followed by dreams, and reblogging a post is the least likely
    if settings.option('general', 'enableChatMode'): emma.chat()
    else:
        if settings.option('tumblr', 'fetchRealAsks'): askList = tumblrclient.get_asks()
        else: 
            print Fore.YELLOW + "!!! Real ask fetching disabled in settings. Using fake asks instead."
            askList = utilities.fakeAsks

        print "Choosing activity..."
        activities = []
        if settings.option('tumblr', 'enableReblogs'): activities.append('reblogPost')
        if settings.option('tumblr', 'enableDreams'): activities.extend(['dream'] * 2)
        if settings.option('tumblr', 'enableAskReplies') and askList != []: activities.extend(['replyToAsks'] * 3)

        activity = random.choice(activities)
        if activity == 'reblogPost':
            print "Reblogging a post..."
            emma.reblog_post()
        elif activity == 'dream':
            print "Dreaming..."
            emma.dream()
        elif activity == 'replyToAsks':
            print "Replying to asks in queue..."
            emma.reply_to_asks(askList)
        
        if settings.option('general', 'enableSleep'):
            print "Sleeping for 15 minutes..."
            time.sleep(900)
        else:
            print Fore.YELLOW + "!!! Sleep disabled in settings -- execution will continue normally in 2 seconds..."
            time.sleep(2)

def loop_emma():
    win.hide()
    while True: run_emma()

settingsList = settings.load_settings()

# Emma GUI-related functions
def make_label(text, **kwds): return Label(text=text, **kwds)
def update_setting(option):
    settingsList = settings.load_settings()
    generalCheckboxMap = {'enableChatMode': enableChatModeBox.on, 'enableSleep': enableSleepBox.on, 'verboseLogging': verboseLoggingBox.on}
    tumblrCheckboxMap = {'publishOutput': publishOutputBox.on, 'enablePostPreview': enablePostPreviewBox.on, 'enableAskReplies': enableAskRepliesBox.on, 'enableAskDeletion': enableAskDeletionBox.on, 'fetchRealAsks': fetchRealAsksBox.on, 'enableReblogs': enableReblogsBox.on, 'enableDreams': enableDreamsBox.on}

    if option in generalCheckboxMap.keys():
        group = 'general'
        value = generalCheckboxMap[option]
    elif option in tumblrCheckboxMap.keys():
        group = 'tumblr'
        value = tumblrCheckboxMap[option]

    settingsList[group][option] = value
    with open('settings.json', 'w') as settingsFile: json.dump(settingsList, settingsFile)
    
## Set up and display Emma's GUI
# General
generalLabel = make_label("General", color=grey, x=20, y=15)
enableChatModeBox = CheckBox(x=20, y=generalLabel.bottom, title="Chat mode", action=(update_setting, 'enableChatMode'))
enableSleepBox = CheckBox(x=20, y=enableChatModeBox.bottom, title="Enable sleep", action=(update_setting, 'enableSleep'))
verboseLoggingBox = CheckBox(x=20, y=enableSleepBox.bottom, title="Verbose Logging", action=(update_setting, 'verboseLogging'))

# Tumblr
tumblrLabel = make_label("Tumblr", color=grey, x=20, y=verboseLoggingBox.bottom+15)
publishOutputBox = CheckBox(x=20, y=tumblrLabel.bottom, title="Publish output", action=(update_setting, 'publishOutput'))
enablePostPreviewBox = CheckBox(x=20, y=publishOutputBox.bottom, title="Show post preview", action=(update_setting, 'enablePostPreview'))
enableAskRepliesBox = CheckBox(x=20, y=enablePostPreviewBox.bottom + 10, title="Enable Ask replies", action=(update_setting, 'enableAskReplies'))
enableAskDeletionBox = CheckBox(x=20, y=enableAskRepliesBox.bottom, title="Enable Ask deletion", action=(update_setting, 'enableAskDeletion'))
fetchRealAsksBox = CheckBox(x=20, y=enableAskDeletionBox.bottom, title="Fetch real Asks", action=(update_setting, 'fetchRealAsks'))
enableReblogsBox = CheckBox(x=20, y=fetchRealAsksBox.bottom + 10, title="Enable Reblogs", action=(update_setting, 'enableReblogs'))
enableDreamsBox = CheckBox(x=20, y=enableReblogsBox.bottom, title="Enable dreams", action=(update_setting, 'enableDreams'))

if settings.option('general', 'enableChatMode'): enableChatModeBox.on = True
if settings.option('general', 'enableSleep'): enableSleepBox.on = True
if settings.option('general', 'verboseLogging'): verboseLoggingBox.on = True
if settings.option('tumblr', 'publishOutput'): publishOutputBox.on = True
if settings.option('tumblr', 'enablePostPreview'): enablePostPreviewBox.on = True
if settings.option('tumblr', 'enableAskReplies'): enableAskRepliesBox.on = True
if settings.option('tumblr', 'enableAskDeletion'): enableAskDeletionBox.on = True
if settings.option('tumblr', 'fetchRealAsks'): fetchRealAsksBox.on = True
if settings.option('tumblr', 'enableReblogs'): enableReblogsBox.on = True
if settings.option('tumblr', 'enableDreams'): enableDreamsBox.on = True

loopButton = Button(x=15, y=enableDreamsBox.bottom + 15, width=170, title="Start Emma Loop", style='default', action=loop_emma)
runOnceButton = Button(x=15, y=loopButton.bottom + 5, width=170, title="Start Emma Once", style='normal', action=run_emma)

win = Window(width=200, height=runOnceButton.bottom + 20, title="Emma", auto_position=True, )

win.add(generalLabel)
win.add(enableChatModeBox)
win.add(enableSleepBox)
win.add(verboseLoggingBox)

win.add(tumblrLabel)
win.add(publishOutputBox)
win.add(enablePostPreviewBox)
win.add(enableAskRepliesBox)
win.add(enableAskDeletionBox)
win.add(fetchRealAsksBox)
win.add(enableReblogsBox)
win.add(enableDreamsBox)

win.add(loopButton)
win.add(runOnceButton)

win.show()
application().run()