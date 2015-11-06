# Data_Analysis_Tweets
Submission for a code challenge whose target is to analyze the community Twitter users. The program has two features:
1. Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.
2. Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.


Usage:
Tweets can be obtained through Twitter's API in JSON format. We assume a file named tweets.txt inside a directory named tweet_input.
Two python codes are in a directory named src. tweets_cleaned.py is for clean the unwanted unicode in tweets.txt. average_degree.py is for calculating the average degree of Twitter hashtag graph for the last 60 seconds.
The outputs are saved in a directory named tweet_output. 
A bash script run.sh is created to excute the programs.

Dependencies: Python 2.7




