# Name:             Question Parser
# Description:      Reads sentences with an interrogative domain and tries to break the question into parts we can use
# Section:          REPLY
from colorama import init, Fore
init(autoreset = True)

import utilities
import settings

def read_question(sentence):
    questionType = ""
    if sentence[0][0] == u"what" and sentence[2][0] == u"be":       # WHAT color BE the sky
        interrogativeProperty = sentence[1][0]     # "color"
        for word in sentence[::-1]:     # SKY the be color what
            if word[1] in utilities.nounCodes:
                interrogativeObject = word[0]        # "sky"
                if settings.option('general', 'verboseLogging'): print Fore.GREEN + "Interrogative: WHAT is " + interrogativeProperty + " of " + interrogativeObject
                return (["what", interrogativeProperty, interrogativeObject])

    elif sentence[0][0] in [u"do", u"does"] and sentence[2][0] == u"have":       # DO dog HAVE paw"
        interrogativeProperty = sentence[1][0]      # "dog"
        for word in sentence[::-1]:     # PAW have dog do
            if word[1] in utilities.nounCodes:
                interrogativeObject = word[0]
                if settings.option('general', 'verboseLogging'): print Fore.GREEN + "Interrogative: DO " + interrogativeProperty + " HAVE " + interrogativeObject
                return (["doXhaveY", interrogativeProperty, interrogativeObject])
            
    else: return None