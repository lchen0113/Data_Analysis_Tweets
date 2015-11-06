import json
import itertools
from itertools import islice
import codecs
import time
import os

data=[]
with open(os.path.dirname(__file__) +  '/../tweet_input/tweets.txt') as f:
    for line in f:
        # slice the next 1 lines from the iterable, as a list.
        lines = [line] + list(itertools.islice(f,0))
        jfile = json.loads(''.join(lines))
        data.append(jfile)

vertex_table={} #(vertex_name,newest_time)
vertex=[] #(time_stamp,vertex name)
connection_table={} #(connection_name,newest_time)
connection=[] #(time_stamp,connection  name)

f = open(os.path.dirname(__file__) +  '/../tweet_output/ftt2.txt','w')

for i in range(len(data)):
    if data[i].get('text'):
        string=data[i]['text'].encode('ascii','ignore')
        current=string.split(" ")
        current_time=time.strptime(data[i]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        tt=(current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
            current_time.tm_hour, current_time.tm_min, current_time.tm_sec,
            current_time.tm_wday, 0, 0)
        current_time_stamp=time.mktime(tt)

        new_coming_vertex=False
        new_vertex=[]
        new_connection=[]

        for chars in current:
            if chars and chars[0]=='#':
                new_vertex.append((current_time_stamp,chars))
                new_coming_vertex=True
        if len(new_vertex)==1:
            new_vertex.pop()
            new_coming_vertex=False
        if new_coming_vertex:
            number_of_new_vertex=len(new_vertex)
            for x in range(number_of_new_vertex):
                for y in range(x+1,number_of_new_vertex):
                    new_pair=[new_vertex[x][1],new_vertex[y][1]]
                    new_pair.sort()
                    new_connection.append((current_time_stamp,new_pair))

            #########################################
            #remove 60-sec old vertex and connection#
            #########################################
            while vertex and vertex[0][0]+60<current_time_stamp:
                old=vertex.pop(0)         
                if vertex_table.get(old[1]) and vertex_table[old[1]]+60<current_time_stamp:
                    del vertex_table[old[1]]
            while connection and connection[0][0]+60<current_time_stamp:
                old=connection.pop(0)
                if connection_table.get(str(old[1])) and connection_table[str(old[1])]+60<current_time_stamp:
                    del connection_table[str(old[1])]

            ################################
            #add new vertex and connections#
            ################################
            while new_vertex:
                new=new_vertex.pop(0)
                vertex.append(new)
                vertex_table[new[1]]=new[0]
            while new_connection:
                new=new_connection.pop(0)
                connection.append(new)
                connection_table[str(new[1])]=new[0]
    if len(vertex_table)==0:
        avg_connections=0
    else:
        avg_connections=float(len(connection_table))/float(len(vertex_table))*2
    f.write(str(format(avg_connections,'.2f'))+'\n')
            
f.close()   
