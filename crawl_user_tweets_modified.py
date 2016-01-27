import ata
import cjson
import json
import codecs
import time
import datetime
import sets

# APP_CONSUMER_KEY = "K5ght1jy6fI1w8mpUCeiQ"
# APP_CONSUMER_SECRET = "TdXtIb5upWPuLoFAJFWjalhmIgqcoZLNvw1IaTWTGS4"
# ACCESS_TOKEN = "1260900631-3N7q5aSs9FgJxC3gwML0aRkQWiB4bTxuXzUYvjI"
# ACCESS_SECRET = "x0DsZIvOX08AIwPLev4KyphulqI9n7HphlT0BDnYI"

# APP_CONSUMER_KEY = "TogXGAljDNjfkyrAfloa20w73"
# APP_CONSUMER_SECRET = "1hbvBFuQq0UkIarUmhLQ8Vr7FxbpSt9zmSeB194rEqNND8ODat"
# ACCESS_TOKEN = "243062187-2aCvuuLiAyEZRfhTI1kHi5lh46ByZaL5Z8Ui9ZP6"
# ACCESS_SECRET = "0CjgfwDSAgJvcLdjO2mwC56krHujKLNTAvaEzThei5UDH"

APP_CONSUMER_KEY = "vwQtjvvKuHff1biuqll2hj9oD"
APP_CONSUMER_SECRET = "nygCebHA3klU8zyH26u8Z9slFP7AXfgsxAJeFOKLmA5EuQXDXo"
ACCESS_TOKEN = "243062187-CIckFBDPmGV5bxAAW681bxoq90ezfyEf1NzUeaqr"
ACCESS_SECRET = "Eio3WBGuYd8Opo5q1tMxhkKWmm8ZXm0jk60FJrlDR3rIV"
access_twitter_api = ata.Main(APP_CONSUMER_KEY, APP_CONSUMER_SECRET)
def read_user_ids(filename):
    in_file = open(filename, 'r')
    lines = in_file.readlines()
    in_file.close()
    theSet = set()
    user_ids = []
    counter = 0
    for line in lines:
        line = line.split()

        if line[0].strip() not in theSet:
            user_ids.append([])
            try:
                therest = line[2:]
            except:
                therest = [""]

            #extract the username
            user_ids[counter].append(line[0].strip())
            #extract latest tweet ID
            user_ids[counter].append(str(line[1].strip()))

           # print "The line:"+" ".join(therest)
            user_ids[counter].append(" ".join(therest))
            counter += 1
            theSet.add(line[0].strip())
    return user_ids


def fetch_tweets(user, latestId, out_file, stats):

    URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    if latestId != -1:
        params = "include_entities=true&include_rts=true&user_id=%s&max_id=%s&count=200" % (user[0], latestId)
    else:
        params = "include_entities=true&include_rts=true&user_id=%s&count=200" % (user[0])
    #print "getting tweets of user %s" % (str(user[0]))

    content = access_twitter_api.request(URL,
                                         params,
                                         ACCESS_TOKEN, ACCESS_SECRET,
                                         sleep_rate_limit_exhausted="False")

    num_tweets = 0.0
    arabic_tweets = 0.0
    fetchAfterThisPoint = latestId
    if content:
        content = cjson.decode(content)
        #user_tweets.extend(content)
        #print "Crawled user tweets: %s" % (user[0])


        thefinal = [[tweet["id_str"], tweet["created_at"], tweet["lang"], tweet["text"].encode("utf-8"), tweet["user"]] for tweet in content]

        #######################################
        # Formatting the results
        for e in thefinal:
            num_tweets += 1

            e[4] = e[4]["screen_name"]

            if str(e[2]) == "ar":
                arabic_tweets += 1

            # print fetchAfterThisPoint, " ",int(e[0])
            # keep track of the largest tweet id for future api calls
            if fetchAfterThisPoint != -1:
                if int(e[0]) < fetchAfterThisPoint:
                    fetchAfterThisPoint = int(e[0])

            if fetchAfterThisPoint == -1:
                fetchAfterThisPoint = int(e[0])


            st = "{["+e[4]+"/:/"+e[0]+"/:/"+e[1]+"/:/"+e[2]+"/:/"+e[3].decode("utf-8")+"]}\n"

            # print st
            out_file.write(st)

        ########################################
        percentage = 0.0
        if num_tweets != 0:
        #    print (arabic_tweets/num_tweets)
            percentage = (arabic_tweets/num_tweets)*100

        #add previous statistics to the new one
        stats = stats+" "+str(num_tweets)+" "+str(percentage)+"%"

        #print user[2]
        print "User: %s has %d arabic tweets out of %d tweets. The latest ID: %d" % (user[0], arabic_tweets, num_tweets, fetchAfterThisPoint)

        # print content
        # rate_limit = access_twitter_api.request("https://api.twitter.com/1.1/application/rate_limit_status.json",
        #                                         "", ACCESS_TOKEN, ACCESS_SECRET,
        #                                         sleep_rate_limit_exhausted="False")
        # rate_limit = cjson.decode(rate_limit)
        # print rate_limit['resources']['statuses']['\\/statuses\\/user_timeline']
    return [num_tweets, fetchAfterThisPoint, stats]


def get_user_tweets(users):

    users = users

    theCurrentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    users_out_file = open("user_withId_list_fetchall.txt", 'w')

    #print users
    user_tweets = []
    # "https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=username&count=5"
    URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    for user in users:
        out_file = codecs.open("crawled_result/tweet_"+user[0]+".txt",'w',encoding='utf-8')
        lists = fetch_tweets(user, int(user[1]), out_file, user[2])
        print "first loop"
        while True:
            print int(lists[0]) < 200
            if int(lists[0]) < 200:
                print "in if statement"
                break
            lists = fetch_tweets(user, lists[1], out_file, lists[2])

        users_out_file.write(user[0]+" "+str(lists[1])+" "+lists[2]+"\n")
    #print user[1]

    out_file.close()
    return user_tweets

def output_user_files(user_profiles, filename):
    out_file = open(filename, 'w')
    for user_profile in user_profiles:
        json.dump(user_profile, out_file)
        out_file.write("\n")
    out_file.close()

def main():
    users = []
    theday = datetime.date(2014, 8, 10)

    # while True:
    #     today = datetime.date.today()
    #
    #     if today == theday:
    #         print "same day"
    #         break
    users = read_user_ids("user_withId_list_fetchall.txt")
    user_tweets = []
    user_tweets = get_user_tweets(users)
        # writeTweetsToFile(user_tweets)
        #output_user_files(user_tweets, "user_data/user_tweets.json")

if __name__ == "__main__":
    main()
