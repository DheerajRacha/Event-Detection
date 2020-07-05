import twint
import csv
#python3 stream_follower.py >  /dev/null 2>&1

with open("/home/sai/Documents/DATA MINING/PROJECT/DATA/NEW/data.csv","r") as f :
	print("hello1")
	reader = csv.reader(f, delimiter = ";")
	#print("hello2")
	for i, line in enumerate(reader) :
		if i >= 628571 :
			#print("hello3")
			print(len(line))
			s = line[0].split(";")
			print(type(s[9]))
			print(s[9])
			a = s[9]
			#print("hello4")
			username = a.split("/")[3]
			#print("hello5")
			print(username)
			c = twint.Config()
			c.Username = username
			c.Pandas = True
			twint.run.Followers(c)
			Followers_df = twint.storage.panda.Follow_df
			list_of_followers = Followers_df['followers'][username]
			list_of_followers.insert(0, username)
			#print(type(list_of_followers))
			#print(list_of_followers)
			with open("/home/sai/Documents/DATA MINING/PROJECT/DATA/NEW/stream_followers.csv", "a") as fp:
			    wr = csv.writer(fp, dialect='excel')
			    if list_of_followers != "" :
			    	wr.writerow(list_of_followers)
			    else :
			    	print("stop")
