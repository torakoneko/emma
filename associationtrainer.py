# Name:             Association Trainer
# Description:      Finds and adds associations to Emma's association model
# Section:          LEARNING
import math
import numpy as np

import sqlite3 as sql

import utilities

def find_associations(sentence):
    for count, word in enumerate(sentence):
        # Types 1 & 2
        if "be" in word[0]:     # todo: add "can"?
            prevWord = sentence[count - 1]
            nextWord = sentence[count + 1]
            if "NP" in prevWord[2]:
                if "ADJP" in nextWord[2]:
                    # type 1
                    print "Found association: %s IS-PROPERTY-OF %s." % (nextWord[0], prevWord[0])
                    add_association(nextWord[0], prevWord[0], "IS-PROPERTY-OF")
                elif "NP" in nextWord[2]:
                    for i in range(len(sentence)):
                        chunksCountingForward = sentence[count + i]
                        if chunksCountingForward[1] in utilities.nounCodes:
                            # type 2
                            print "Found association: %s IS-A %s." % (prevWord[0], chunksCountingForward[0])
                            add_association(prevWord[0], chunksCountingForward[0], "IS-A")
                            break
                            
        # Type 3
        if "NP" in word[2] and word[1] in utilities.nounCodes:
            NPchunk = []
            for i in range(count):
                chunksCountingBackward = sentence[count - (i + 1)]
                chunksCountingBackward = chunksCountingBackward[2]
                if "B" in chunksCountingBackward[0]:
                    NPchunk.extend(sentence[count - (i + 1):count])
                    break
            for group in NPchunk:
                if group[1] in utilities.adjectiveCodes:
                    print "Found association: %s IS-PROPERTY-OF %s." % (group[0], word[0])
                    add_association(group[0], word[0], "IS-PROPERTY-OF")

connection = sql.connect('emma.db')
cursor = connection.cursor()
def add_association(word, target, associationType):
    with connection:
        cursor.execute('SELECT * FROM associationmodel WHERE word = \'%s\' AND target = \'%s\' AND association_type = \'%s\';' % (word, target, associationType))
        SQLReturn = cursor.fetchone()
    if SQLReturn:
        # update record
        newWeight = calculate_weight(True, SQLReturn[4])
        with connection:
            cursor.execute('UPDATE associationmodel SET weight = \'%s\' WHERE word = \'%s\' AND target = \'%s\' AND association_type = \'%s\';' % (newWeight, word, target, associationType))
    else:
        # add record
        weight = calculate_weight(False, None)
        with connection:
            cursor.execute('INSERT INTO associationmodel(word, association_type, target, weight) VALUES (\'%s\', \'%s\', \'%s\', \'%s\');' % (word, associationType, target, weight))
            
e = math.exp(1)     # todo: find a way to do this with numpy
def calculate_weight(isUpdate, currentWeight):
    rankingConstant = 3.19722457734
    if isUpdate == True:
        currentWeight = np.log(currentWeight/(1-currentWeight))+rankingConstant
    else:
        currentWeight = 0
    currentWeight += 1
    weight = 1/(1+e**-(currentWeight-rankingConstant))
    return weight