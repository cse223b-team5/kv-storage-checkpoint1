# cse223b-project
A fault-tolerant distributed k/v storage system based on RAFT

Team member:
1. Ling Hong
2. Shuwei Liang
3. Jie Lu

Related site: http://cseweb.ucsd.edu/~gmporter/classes/sp19/cse223b/techreport/

Guide:

Client:
Get: python client.py config_file get key
  example: python client.py config.txt get 3
Put: python client.py config_file put key value
  example: python client.py config.txt put 3 1
