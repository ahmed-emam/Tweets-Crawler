__author__ = 'ahmedemam'
import re
import os
files_list = os.listdir("/home/amtibaa/Twitter_Crawler/crawled_result/")

languages = []
languages_count = []
users = []

for file in files_list:
    file = open("crawled_result/"+file, "r")
    print("Getting status from file: %s" % file.name)
    for line in file:
        # line = file.read()
    # print(line)
        m = re.match(r'\{\[(.*)]}', line)
    # print(m.groups())
        if m:
            x = re.match(r'(.*)/:/(.*)/:/(.*)/:/(.*)/:/(.*)', m.group(1))

            if x:
                username = x.group(1)
                tweetId = x.group(2)
                time = x.group(3)
                language = x.group(4)
                tweet = x.group(5)
                try:
                    lang_index = languages.index(language)
                    languages_count[lang_index] += 1
                except ValueError:
                    lang_index = -1
                    languages.append(language)
                    languages_count.append(1)

                try:
                    users.index(username)
                except ValueError:
                    users.append(username)
                # if lang_index == -1:
                #     languages.append(language)
                #     languages_count.append(1)
                # else:
                #     languages_count[lang_index] += 1
                # print(username)
                # print(tweetId)
                # print(time)
                # print(language)
                # print(tweet)
            # print("#########################")

    for idx in range(0, len(languages)):
        print("%s : %d" % (languages[idx], languages_count[idx]))

    print(len(users))
