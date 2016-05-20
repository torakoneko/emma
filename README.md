     .ooooo.  ooo. .oo.  .oo.   ooo. .oo.  .oo.    .oooo.
    d88' `88b `888P"Y88bP"Y88b  `888P"Y88bP"Y88b  `P  )88b
    888ooo888  888   888   888   888   888   888   .oP"888
    888    .,  888   888   888   888   888   888  d8(  888
    `Y8bod8P' o888o o888o o888o o888o o888o o888o `Y888""8o

    ·~-.¸¸,.-~*¯¨*·~-.¸,.-~*¯¨*·~-.¸¸,.-~*¯¨*·~-.¸¸,.

           ENGLISH MODEL of MAPPED ASSOCIATIONS


     Written by Ellie Cochran & Alexander Howard, with
                contributions by Omri Barak.

      Uses elements from the Natural Language Toolkit.
                 Visit http://www.nltk.org.

Emma is a computer program that generates rough concepts of associations by reading input. She uses these associations, in conjunction with learned sentence structure patterns, to generate a reply.
She is a Summer project created by Digital Media student, programmer, & computer artist Ellie Cochran, and Computer Science & Mathematics student Alexander Howard, with some contributions by Omri Barak.

###Progress towards completion
     [0%]▨▨▨▨▨▨▨▨[25%]▨▨▨▨▨▨▨▨[50%]▢▢▢▢▢▢▢[75%]▢▢▢▢▢▢▢[100%]
     - Emma is able to learn and store concepts and sentence structures
     - The next thing for us to work on is sentence generation and output

##How Emma Works
###Input
* The User submits input. This can be in the form of text ranging from a few words to infinite paragraphs
  * The input is broken down into sentences, if it isn't a sentence already
  * Sentences are broken down into words
    * This means that Emma can handle input one sentence at a time, which helps her to generate her sentence structure models
  * Words are categorized accoring to their part of speech (noun, verb, conjunction, adjective, etc.)
    * "Important words" are set aside and used to train Emma's Concept Graph
      * Important words include nouns, verbs, and adjectives
      * We arrived on these three types of word because we consider them to be the "meat" of a sentence. You could remove everything else and most sentences would still make sense
      
###Learning
* Emma's learning routines include concept generation and sentence type parsing, and occur one sentence at a time
* First, Emma parses the sentence structure to improve her ability to create new sentences
  * The sentence pattern is defined by the order of its parts of speech
  * These parts of speech are stored as the corpus of a 2nd-Order Markov chain, which Emma uses later to generate new sentence structures
  * Punctuation is included in this model, which helps Emma decide when and how to end a sentence
* Emma formulates concepts based on the input text
  * Nouns are plucked out of the sentence, and make up the basis of Emma's knowledge graph
    * This is because nouns are the *most important* important word
  * Nouns are linked with the various adjectives, verbs, and other nouns in the sentence
    * This creates an association in Emma's Concept Graph. For example, a noun-adjective association might include "Cats" and "Furry"
    * **(TODO)** The noun's case is determined according to its type of speech and added to its "case score," which helps Emma decide if she should use lowercase, uppercase, or title case when writing that word
      * **(TODO)** Nouns that are tagged as proper nouns by Emma's part of speech tagger are automatically set to title-case
      * **(TODO)** Nouns at the beginning of sentences do not have an effect on the case score unless they are tagged as proper nouns by Emma's part of speech tagger
    * The noun associations also include what kind of association they are (noun-noun, noun-verb, or noun-adjective), the number of times those words appear together, their average proximity to eachother, and the strength of the association (which is determined by dividing the frequency of the association by the natural log of its average proximity plus one)
  * **(TODO)** If the noun has never been encountered before, Emma will search for it on Tumblr and use the resulting text posts to train her associations
* **(TODO)** Add tone parsing & "feelings"

###Reply Generation
* After all input sentences are parsed, Emma attempts to form a reply
  * A new sentence is generated by first creating a new sentence structure from Emma's sentence structure model
  * The sentence's topic (AKA its choice of nouns) is influenced by the nouns used in the input, and those nouns' associated concepts in Emma's Concept Graph
    * Obviously, the choice of words is influenced by the strength of their association in Emma's Concept Graph
* Each sentence Emma generates is collected into a paragraph, and the output is printed

#Talk to Emma
Emma isn't online yet, but when she is we'll hook up a conversation interface using Tumblr "asks" as a frontend. You will be able to talk to Emma at [emmacanlearn.tumblr.com](http://emmacanlearn.tumblr.com).

##To-Do
The following features are on our list of things to implement once Emma's core feature set is complete:
* Create a paragraph model that is trained on the sentences in the input to help Emma decide when to end paragraphs and what kinds of sentences should follow other sentences.
  * Should the number of sentenes in the input affect the number of sentences attempted in the output?
* Write some way of visualizing the Concept Graph. It'd be so cool to see
  * Association strength could be represented using line opacity
  * Lines could have arrows indicating directionality
* We need to find a special way to handle questions
  * There's not a lot of new information that can be gleaned from questions
  * Questions, by their nature, are information holes requesting to be filled
  * We could generate an "answer" sentence type, or a question could prompt Emma to list things she knows about nouns in the question based on the strongest associations (for example, an input of "What are cats?" would prompt a reply of "Cats are furry, soft, gentile, and sweet. They explore, meow, purr, and sleep")
  
##Contact the Developers
Ellie and Alex are on social media! Ask us about Emma!
Ellie Cochran is [@sharkthemepark](http://sharkthemepark.tumblr.com) on Tumblr and Twitter.
Alexander Howard is [@ale303sh](http://www.twitter.com/ale303sh) on Twitter.
