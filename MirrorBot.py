#!/usr/bin/python
import requests
import praw
import re
import time
import random
import os

#####################
# PART 1: THE SETUP #
#####################

#List of words to match GTA Roleplay
wordList = ['nopixel','gta rp', 'gta v rp', ' rp ', 'roleplay', ' family ', 'no pixel', ' np ', 'no-pixel', 'svrp', 'twitchrp', 'aftermathrp', 'aftermath', 'nonstop', 'nonstoprp']

#List of streamers to whitelist (if they have stupid titles without matching the above)
streamerList = ['Shotz', 'CurtisRyan', 'LAGTVMaximusBlack', 'Spaceboy', 'JoblessGarrett', 'PENTA', 'RatedEpicz', 'summit1g', 'buddha', 'UberHaxorNova', 'Lord_Kebun', 'Ramee', 'dasMEHDI', 'koil', 's0upes', 'NewFaceSuper', 'AfriicanSnowball', 'mantisobagan', 'Madmoiselle', 'Viviana', 'JoeSmitty123', 'Xaphgnok', 'JdotField', 'the_halfhand', 'Choi', 'Armeeof1', 'NotoriousNorman', 'Jayce', 'kfruntrfrunt', 'YoinksOG', 'aXed_U', 'xReklez', 'MasterMisuri', 'Coolio']

#Streamers to hide from the sidebar
ignoreList = ['Vader', 'Zombie_Barricades', 'RiceGum']

#Reddit setup
reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENTID'],
                     client_secret=os.environ['REDDIT_CLIENTSECRET'],
                     password=os.environ['REDDIT_PASSWORD'],
                     user_agent='Mirrorbot V2 by /u/powerjaxx and /u/skyrossm',
                     username=os.environ['REDDIT_USERNAME'])

subreddit = reddit.subreddit(os.environ['REDDIT_SUBREDDIT'])
settings = subreddit.mod.settings()

#Sidebar template for NEW reddit
newreddit_sidebar = '''
    Streamer | Viewer Count
    ---|---
    [{0}](https://www.twitch.tv/{0}) |{10}
    [{1}](https://www.twitch.tv/{1}) |{11}
    [{2}](https://www.twitch.tv/{2}) |{12}
    [{3}](https://www.twitch.tv/{3}) |{13}
    [{4}](https://www.twitch.tv/{4}) |{14}
    [{5}](https://www.twitch.tv/{5}) |{15}
    [{6}](https://www.twitch.tv/{6}) |{16}
    [{7}](https://www.twitch.tv/{7}) |{17}
    [{8}](https://www.twitch.tv/{8}) |{18}
    **Random Streamer:** |[{9}](https://www.twitch.tv/{9})
    '''

#Sidebar template for OLD reddit
oldreddit_sidebar = '''
[](https://discord.gg/pbHERV6y87)

--------------------------------
**[CLICK HERE FOR RULES](https://www.reddit.com/r/RPClipsGTA/wiki/subreddit/rules)**
---

-------------------------------------------------------------
**Top GTA RP Streamers live**
---
Streamer | Viewer Count
    ---|---
    [{0}](https://www.twitch.tv/{0}) |{10}
    [{1}](https://www.twitch.tv/{1}) |{11}
    [{2}](https://www.twitch.tv/{2}) |{12}
    [{3}](https://www.twitch.tv/{3}) |{13}
    [{4}](https://www.twitch.tv/{4}) |{14}
    [{5}](https://www.twitch.tv/{5}) |{15}
    [{6}](https://www.twitch.tv/{6}) |{16}
    [{7}](https://www.twitch.tv/{7}) |{17}
    [{8}](https://www.twitch.tv/{8}) |{18}
    **Random Streamer:** |[{9}](https://www.twitch.tv/{9})

-------------------------------------------------------------
'''


#Reply template for Mirror bot
reply_template = '''
[MIRROR: {0}](https://streamable.com/{1})


Credit to {2} for the content.

{3}

-----------------------------
^(I am a bot. Beepity Boopity)
'''


#######################
# PART 2: SIDEBAR BOT #
#######################

#Returns the top RP streamers from the GTA section on Twitch
def get_streamer_list():
    #Twitch API headers/url to get top GTA streams
    api_url = 'https://api.twitch.tv/kraken/streams?limit=99&language=en'
    headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': os.environ['TWITCH_CLIENTID']}
    payload = { 'broadcaster_language': 'en', 'game': 'grand theft auto v',}
    r = requests.get(api_url, headers=headers, params=payload)

    #Data of the top 100 streams in GTA
    stream_data = r.json()

    #Get the top streamer names
    names = [x['channel']['display_name']
    for x in stream_data['streams']
        if (any(s in x['channel'].get('status', '').lower() for s in wordList)
        or any(u in x['channel'].get('display_name', '') for u in streamerList))
        and x['broadcast_platform']=='live'
        and not any(u in x['channel'].get('display_name', '') for u in ignoreList)]

    #Same code but for view count
    viewer_count = [x['viewers']
    for x in stream_data['streams']
        if (any(s in x['channel'].get('status', '').lower() for s in wordList)
        or any(u in x['channel'].get('display_name', '') for u in streamerList))
        and x['broadcast_platform']=='live'
        and not any(u in x['channel'].get('display_name', '') for u in ignoreList)]

    #Check for null values in the top 10 list (if not enough streamers online)
    for i in range(10):
        try:
            gotdata = names[i]
        except IndexError:
            names.append(' ')
            viewer_count.append(0)

    #Get list of streamers less than 250 viewers
    randomList = sorted(i for i in viewer_count if i <= 250)
    if len(randomList) != 0:
        ran = random.choice(randomList)
    else:
        ran = viewer_count[-1]
    newindex = viewer_count.index(ran)
    #Only need the name for the random stream
    random_stream = names[newindex]

    global oldsidebarformatted
    oldsidebarformatted = oldreddit_sidebar.format(names[0], names[1], names[2], names[3], names[4], names[5], names[6], names[7], names[8], random_stream, viewer_count[0], viewer_count[1], viewer_count[2], viewer_count[3], viewer_count[4], viewer_count[5], viewer_count[6], viewer_count[7],  viewer_count[8])
    return newreddit_sidebar.format(names[0], names[1], names[2], names[3], names[4], names[5], names[6], names[7], names[8], random_stream, viewer_count[0], viewer_count[1], viewer_count[2], viewer_count[3], viewer_count[4], viewer_count[5], viewer_count[6], viewer_count[7],  viewer_count[8])

def update_sidebar(updateText):
    #Update new sidebar
    custom = None
    widgets = subreddit.widgets
    for widget in widgets.sidebar:
        if isinstance(widget, praw.models.CustomWidget):
            if (widget.shortName == "TOP GTA STREAMERS"):
                custom = widget
                break
    custom.mod.update(text=updateText)
    
    #Update old sidebar
    subreddit.wiki['config/sidebar'].edit(oldsidebarformatted)

######################
# PART 3: MIRROR BOT #
######################

#Send request to Streamable
def streamable(clip_url, submission, comment):
    #Get clip info
    clipinfo(clip_url, submission)
    api_url = 'https://api.streamable.com/import'
    payload = {'url': clip_url, "title": title_clip + " - Clip from " + broadcaster_url}
    headers = {'User-Agent': 'A bot that creates mirrors of clips'}
    r = requests.get(api_url, params=payload, auth=(os.environ['STREAMABLE_USER'], os.environ['STREAMABLE_PW']), headers=headers)
    if r.status_code == 200:
        #Successfully created mirror
        data = r.json()
        #Gets the video ID
        shortcode = data['shortcode']
        reply_text = reply_template.format(title_clip, shortcode, broadcaster_url, vod_link)
        if comment is None:
            #Reply to the submission on reddit and sticky.
            reply = submission.reply(reply_text)
            reply.mod.distinguish(sticky=True)
            reply.mod.lock()
            print("Replied to submission.")
        else:
            #Reply to the comment on reddit
            reply = comment.reply(reply_text)
            reply.mod.distinguish()
            print("Replied to comment")
        #Create private backup of clip.
        #time.sleep(10) #10s for rate limiting.
        #payload = {'url': clip_url, "title": "[PRIVATE] " + title_clip + " - Clip from " + broadcaster_url}
        #r_private = requests.get(api_url, params=payload, auth=(os.environ['STREAMABLE_USER'], os.environ['STREAMABLE_PW']), headers=headers)
        #if r_private.status_code == 200:
        #    priv_data = r_private.json()
        #    print("Private clip created: http://streamable.com/{0}".format(priv_data['shortcode']))
    else:
        print("Error getting streamable clip.")
        pass

#Gets the clip title, user, etc.
def clipinfo(clip_url, submission):
    global broadcaster_url
    global title_clip
    global vod_link
    #HTTPS clip
    if clip_url.startswith('https://clips.twitch.tv'):
        url_end = clip_url[24:] #Should just get it with regex but whatever
        print(url_end) #debug so we know the clips that have been mirrored
    elif clip_url.startswith('http://clips.twitch.tv'): #This happens sometimes
        url_end = clip_url[23:]
        print(url_end)
    else:
        #TODO: add support for Facebook, YT, etc.
        pass
    #Request params
    headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': os.environ['TWITCH_CLIENTID']}
    api_url = 'https://api.twitch.tv/kraken/clips/{0}'.format(url_end)

    #Send request
    r = requests.get(api_url, headers=headers)

    data = r.json()

    #link to their twitch channel
    broadcaster_url = data["broadcaster"]["channel_url"]
    title_clip = data["title"]
    try:
         vod_link = '[Continue watching](' + data["vod"]["url"] + ')'
    except TypeError:
        print("No vod link")
        vod_link = ''

def process_submission(submission, comment):
    clip_url = submission.url
    sid = submission.id
    if not submission.archived:
        if clip_url.startswith('https://clips.twitch.tv'):
            streamable(clip_url, submission, comment)
        elif clip_url.startswith('http://clips.twitch.tv'):
            streamable(clip_url, submission, comment)
        elif re.match('https://www.twitch.tv/.*/clip/.*', clip_url):
            new_url = 'https://clips.twitch.tv/' + clip_url.split("clip/")[1]
            print("Fixed broken twitch url");
            #Could also configure to auto remove post
            streamable(new_url, submission, comment)
        print('Replied to {0}'.format(sid))
    else:
        pass

################################
# PART 4: BRINGING IT TOGETHER #
################################

#Submission stream for the subreddit (Only includes new submissions)
submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)

#Comment stream for the subreddit (Only includes new comments)
comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)

while True:
    #Check for new posts
    for submission in submission_stream:
        if submission is None:
            print("No new submissions")
            break
        print(submission.title)
        process_submission(submission, None)
        #prevent rate limiting (>1 request per second)
        time.sleep(300)
    #Check for new mirror requests
    for comment in comment_stream:
        if comment is None:
            print("No new mirror requests")
            break
        comment_text = str(comment.body).strip()
        if comment.distinguished and (comment_text == "u/RPClipsBackupBot backup" or comment_text == "!newmirror" or comment_text == "u/RPClipsBackupBot mirror"):
            print("processing comment")
            process_submission(comment.submission, comment)
            #prevent rate limiting (>1 request per second)
            time.sleep(5)

    #Update the sidebar
    update_sidebar(get_streamer_list())
    print("Updated sidebars")

    #Sleep for 5 minutes. (30s for testing)
    time.sleep(300)
