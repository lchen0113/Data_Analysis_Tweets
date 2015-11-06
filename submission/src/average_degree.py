import json
import itertools
from itertools import islice
import codecs
import time
import os


def read_tweets():
    """ Read the given file line by line, storing values in a list.
    Returns: data (list): content of the tweets stored in a list.
    Exceptions: if failed to read the file, return empty list.
    """
    data = []
    try:
        with open(os.path.dirname(__file__) +  '/../tweet_input/tweets.txt') as f:
            for line in f:
                jfile = json.loads(''.join(line))
                data.append(jfile)
        return data
    except:
        print("File not found")
        return []

def get_current_time_stamp(tweet):
    """ Format current time for later 60 seconds comparison.
    Args: tweet: a raw tweet item.
    Returns: floating point number current_time_stamp.
    """
    current_time = time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    tt=(current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
        current_time.tm_hour, current_time.tm_min, current_time.tm_sec,
        current_time.tm_wday, 0, 0)
    current_time_stamp = time.mktime(tt)
    return current_time_stamp

def get_new_vertex_connection(tweet, current_time_stamp):
    """ Find new vertex and connection and save them in new_vertex and new_connection.
    Args: tweet: a raw tweet item.
          current_time_stamp.
    Returns: new_vertex: a tuple of new coming vertex with format (current_time_stamp, new_vertex).
            new_connection: a tuple of new coming connection with format (current_time_stamp, new_connection). The connection pair is sorted by alphabet order.
    """
    new_coming_vertex = False
    new_vertex = []
    new_connection = []
    string = tweet['text'].encode('ascii','ignore')
    current = string.split(" ")
    for chars in current:
        if chars and chars[0] == '#':
            new_vertex.append((current_time_stamp, chars))
            new_coming_vertex = True
    if len(new_vertex) == 1: # ignore the single vertex in hashtag
        new_vertex.pop()
        new_coming_vertex = False
    if new_coming_vertex:
        number_of_new_vertex = len(new_vertex)
        for x in range(number_of_new_vertex):
            for y in range(x+1,number_of_new_vertex):
                new_pair = [new_vertex[x][1],new_vertex[y][1]]
                new_pair.sort()  # new connection pair is sorted to avoid duplicate
                new_connection.append((current_time_stamp, new_pair))
    return new_vertex, new_connection

def remove_old_vertex_connection(vertex, vertex_table, connection, connection_table, current_time_stamp):
    """ Remove the old vertex and connections earlier than current_time_stamp-60 seconds to save memory.
    """
    while vertex and vertex[0][0]+60<current_time_stamp: # if it exits old vertex whose time is earlier than current_time_stamp-60
        old=vertex.pop(0)
        if vertex_table.get(old[1]) and vertex_table[old[1]]+60<current_time_stamp: # delete the old vertex in vertex_table
            del vertex_table[old[1]]
    while connection and connection[0][0]+60<current_time_stamp: # if it exits old connection whose time is earlier than current_time_stamp-60
        old=connection.pop(0)
        if connection_table.get(str(old[1])) and connection_table[str(old[1])]+60<current_time_stamp: # delete the old connection in connection_table
            del connection_table[str(old[1])]

def add_new_vertex_connection(vertex, vertex_table, new_vertex, connection, connection_table, new_connection):
    """ Add new coming vertex and connections to corresponding list or dictionary.
    """
    while new_vertex:
        new = new_vertex.pop(0)
        vertex.append(new)
        vertex_table[new[1]] = new[0]
    while new_connection:
        new = new_connection.pop(0)
        connection.append(new)
        connection_table[str(new[1])] = new[0]

def get_avg_degree(vertex_table, connection_table):
    """ Calculate the average graph degree based on vertex_table and connection_table.
    """
    if len(vertex_table) == 0:
        avg_degree = 0
    else:
        avg_degree=float(len(connection_table))/float(len(vertex_table))*2
    return avg_degree

def main():
    """ Main function to calculate the degree of hashtag graph within 60 seconds.
    Idea: the program maintains four data structures for graph degree calculation.
        vertex_table: a dictionary whose key is vertex name and value is its newest coming time. The keys in dictionary do not have order.
        vertex: a list of tuples. Each tuple is (current_time_stamp, vertex_name). Since the tuple is order by time, it can provide auxiliary time
        information to remove or add vertex to vertex_table compared to 60 seconds.
        connnection_table: a dictionary whose key is connection edge name and value is its newest coming time.
        connection: a list of tuples whose function is similar to vertex.
    """
    vertex_table = {}  #(vertex_name,newest_time)
    vertex = []  #(time_stamp,vertex name)
    connection_table = {}  #(connection_name,newest_time)
    connection = []  #(time_stamp,connection  name)
    f = open(os.path.dirname(__file__) +  '/../tweet_output/ft2.txt','w')
    data = read_tweets()
    for i in range(len(data)):
        if data[i].get('text'):
            current_time_stamp=get_current_time_stamp(data[i])
            new_vertex, new_connection=get_new_vertex_connection(data[i],current_time_stamp)
            remove_old_vertex_connection(vertex,vertex_table,connection,connection_table,current_time_stamp)
            add_new_vertex_connection(vertex,vertex_table,new_vertex,connection,connection_table,new_connection)
        avg_degree=get_avg_degree(vertex_table,connection_table)
        f.write(str(format(avg_degree,'.2f'))+'\n')
    f.close()

if __name__ == "__main__":
    main()
