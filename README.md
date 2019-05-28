# cse223b-project-checkpoint1
A fault-tolerant distributed k/v storage system based on RAFT

Team member:
1. Ling Hong
2. Shuwei Liang
3. Jie Lu

Related site: http://cseweb.ucsd.edu/~gmporter/classes/sp19/cse223b/techreport/

**Use Guide**
   
   **Start Servers** 
   
   COMMAND: *bash start_server.sh*
   
   Run start_server.sh to initialize the servers. Specifically, it i) starts 5 
   servers (specified by config.txt) and automatically configure their IPs and ports. It also ii) 
   uploads the Connection Matrix (location: matrix) to all 5 servers. One can modify the 
   config.txt and matrix to simulate using servers with different configurations and expect
   to see different performance.
   
   **Client request**
   
   COMMAND: *python client.py CONFIG OPERATION ARGVs*
   
   Examples:
   
   1. *python client.py config.txt put 3 2*
   
   2. *python client.py config.txt get 3*
   
   To start a request from client, run client.py and input parameters. To get the value of a certain key,
   input **get** and followed by the **key** (shown as example1); to put a key/value pair into to dictionary, 
   input **put** and followed by the k/v pair (shown as example2.)
   
   **Modify Connection Matrix**
   
   COMMAND: *python chaos_client.py OPERATION CONFIGURE ARGVs*
   
   Examples: 
   
   1. *python chaos_client.py upload config.txt matrix*
   
   2. *python chaos_client.py edit config.txt 0 2 0.4*
   
   This command allows to interactively modify the Connection Matrix (ConnMat) to simulate the dynamic network conditions.
   New ConnMat can be applied to all servers at one command. Example1 uploads a new ConnMat to all servers, and example2 
   uses 0.4 to substitute the value at position <0,2> in ConnMat.
