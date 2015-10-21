import json
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import configparser
Config=configparser.ConfigParser()

"""
All runs bc of twurl --

After authenticating, can run:
    "twurl /1.1/statuses/user_timeline.json"

    I add ("?screen_name=" + screenname) to the end of this.

This prog reads the text (or json or whatever) file and stores it as json data
You can then search the json data for just the tweets, retweets, whatever... keywords here.
"""

def parseData(sn, pages, pmf):


    data = []
    cmd = "twurl \"/1.1/statuses/user_timeline.json?screen_name=" + sn + "&page=\""

    #Upper bound of range is how many pages of tweets checked
    #More pages is preferable, but slower.
    for i in range (1,pages):
        output = subprocess.check_output((cmd + str(i)), shell=True) #page=1; page=2...
  
        try:
            tweets = json.loads(output.decode())
               
        except:
            print ("Something went wrong")
            return
           

        for i in range (len(tweets)):
            try:
                data.append(str(tweets[i]['text'])) #pull the text of the tweet
            except:
                pass

    #for j in range (len(data)): #debug
        #print(data[j])

    #mention counters
    economics = 0
    foreign = 0
    immigration = 0
    transpac = 0
    education = 0
    crime = 0

    #TODO: Ignore case when searching
    #TODO: More keywords

    #keywords, e=economic keywords, f = foreign policy...
    e = ["banks", "corporat", "money", "companies", "company", "working class", "Wall Street", "billionaire", 
                "wealth", "income", "econom", "wage", "Social Security"]
    f = ["Syria", "China", "Chinese", "Iraq", "Iran", "war"]
    t = ["TPP", "Pacific Partnership"]
    i = ["citizen", "documented", "immigration"]
    ed = ["education", "loan", "student", "college", "university", "school", "teacher"]
    c = ["marijuana", "criminal", "crime", "policing", "police", "jail", "prison", "incarcerat"]

    #maybe jobs = unions, work, jobs

    #TODO: this could probably be more efficient
    for j in range (len(data)): 
        twt = data[j]
        if any (x in twt for x in e): #if any words in e appear in twt...
            economics += 1
        if any (x in twt for x in f): #if any words in f appear in twt...
            foreign += 1
        if any (x in twt for x in i): 
            immigration += 1
        if any (x in twt for x in t): 
            transpac += 1
        if any (x in twt for x in ed): 
            education += 1
        if any (x in twt for x in c): 
            crime += 1

    #Labels for the graph
    topics = ["Economics", "Foreign Policy", "Immigration", "Transpac. Partnersh.", "Education", "Crime/Drugs"]
    mentions = [economics, foreign, immigration, transpac, education, crime]

    if (pmf):
        PMF(topics, mentions)
    else:
        graphData(topics,mentions)

#stolen from matplotlib documentation
def graphData(topics, mentions, PMFunc = False):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ## the data
    N = len(topics)

    ## necessary variables
    ind = np.arange(N)                # the x locations for the groups
    width = .85                   # the width of the bars

    ## the bars
    rects1 = ax.bar(ind, mentions, width, color='blue')

    ylimit = max(mentions)  #biggest one 
    ylimit = ylimit + float(ylimit)/4 #plus some space

    # axes and labels
    ax.set_xlim(-width,len(ind)+width)
    ax.set_ylim(0, ylimit)
    ax.set_ylabel('Mentions')
    #ax.set_xlabel('Topics')
    if (PMFunc):
        ax.set_title("Percentage of Tweets per Issue", fontsize="large")
    else:
        ax.set_title("Issues Mentioned in Tweets", fontsize="large")
    ax.set_xticks(ind + width/2)
    xtickNames = ax.set_xticklabels(topics)
    plt.setp(xtickNames, rotation=5, fontsize=8)


    #CT Zhu on StackOverflow explained this, link at bottom
    #this could be looped depending on how many topics we get -- B, R, G, B
    ax.get_children()[3].set_color('r')
    ax.get_children()[4].set_color('g')
    ax.get_children()[6].set_color('r')
    ax.get_children()[7].set_color('g')

    plt.show()

#wrapper converts mentions to ratio of mentions/mentions_of_all_topics
#Probability mass function
def PMF(topics, mentions):

    count = 0
    ratio = 0 #debug
    pmfmen = [0]*len(mentions) #mentions for purposes of PMF

    for i in range (len(mentions)):
        count += mentions[i]
    for i in range (len(mentions)):
        pmfmen[i] = float(mentions[i])/count
        ratio += pmfmen[i] #debug

    #print (ratio) #debug
    graphData(topics, pmfmen, PMFunc=True)



def main():
    try:
        Config.read('tweet-graph.config')
    except:
        raise Exception("Couldn't connect to config file")

    pages = int(Config.get('conf','pages'))
    sn = Config.get('conf','screenname')
    pmf = int(Config.get('conf', 'pmf'))
    
    parseData(sn, pages, pmf)




if __name__ == "__main__":
    main()



# try:
#     Config.read('alarm.config')
# except:
#     raise Exception("Couldn't connect to alarm config file")

# db = int(Config.get('main','debug'))


#CT Zhu on Stack Overflow: 
#http://stackoverflow.com/questions/18973404/setting-different-bar-color-in-matplotlib-python






