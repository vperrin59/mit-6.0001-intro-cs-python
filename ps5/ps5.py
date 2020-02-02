# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, desc, link, pubdate):
        """
            guid: string
            title: string
            desc: string
            link: string
            pubdate: datetime
        """
        self.guid = guid
        self.title = title
        self.desc = desc
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

    def get_description(self):
        return self.desc
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        """
        Valid phrase: "purple cow"
        """
        self.phrase = phrase.lower().split()

    def is_phrase_in(self, text):
        # Generate list of words from text
        text_to_parse = text.lower()
        for p in string.punctuation:
            text_to_parse = text_to_parse.replace(p, " ")
        text_to_parse = text_to_parse.split()
        # Check if phrase is in text
        for k in range(len(text_to_parse) - len(self.phrase) + 1):
            # if w == self.phrase[0]:
            match = True
            for i, p in enumerate(self.phrase):
                if text_to_parse[k + i] == p:
                    pass
                else:
                    match = False
                    break
            
            if match:
                return True

        return False




# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time_s):
        """
        time_s: string, 3 Oct 2016 17:00:10
        """
        self.time = datetime.strptime(time_s, "%d %b %Y %H:%M:%S")

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.time > story.get_pubdate()

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.time < story.get_pubdate()
    
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, not_trig):
        self.not_trig = not_trig
    
    def evaluate(self, story):
        return not self.not_trig.evaluate(story)
        

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trig_a, trig_b):
        self.trig_a = trig_a
        self.trig_b = trig_b
        
    def evaluate(self, story):
        return self.trig_a.evaluate(story) and self.trig_b.evaluate(story)

# Problem 9
# TODO: OrTrigger
        
class OrTrigger(Trigger):
    def __init__(self, trig_a, trig_b):
        self.trig_a = trig_a
        self.trig_b = trig_b
        
    def evaluate(self, story):
        return self.trig_a.evaluate(story) or self.trig_b.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    res = []
    for s in stories:
        for t in triggerlist:
            if t.evaluate(s):
                res.append(s)
                break
    return res



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    
    triggs = {}
    final_triggers = []
    for line in lines:
        words = line.split(",")
        print(words)
        if words[0] == "ADD":
            print(triggs)
            for i in range(1, len(words)):
                final_triggers.append(triggs[words[i]])
        else:
            if words[1] == "TITLE":
                triggs[words[0]] = TitleTrigger(words[2])
            elif words[1] == "DESCRIPTION":
                triggs[words[0]] = DescriptionTrigger(words[2])
            elif words[1] == "AFTER":
                triggs[words[0]] = AfterTrigger(words[2])
            elif words[1] == "BEFORE":
                triggs[words[0]] = BeforeTrigger(words[2])
            elif words[1] == "AND":
                triggs[words[0]] = AndTrigger(words[2], words[3])
            elif words[1] == "OR":
                triggs[words[0]] = OrTrigger(words[2], words[3])
            elif words[1] == "NOT":
                triggs[words[0]] = NotTrigger(words[2])
                
    for t in final_triggers:
        print(t) # for now, print it so you see what it contains!
    return final_triggers


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
#        t1 = TitleTrigger("election")
#        t2 = DescriptionTrigger("Trump")
#        t3 = DescriptionTrigger("Clinton")
#        t4 = AndTrigger(t2, t3)
#        triggerlist = [t1, t4]

#        t2 = DescriptionTrigger("crochet")
#        triggerlist = [t2]
        
        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
#        exit()
        triggerlist = read_trigger_config('triggers.txt')


        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

