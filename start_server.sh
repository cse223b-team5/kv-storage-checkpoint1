#!/bin/bash
python3 server.py config.txt localhost 5001 &
python3 server.py config.txt localhost 5002 &
python3 server.py config.txt localhost 5003 &
python3 server.py config.txt localhost 5004 &
python3 server.py config.txt localhost 5005 &
echo "sleep 0.5sec to let servers start..."
sleep 0.5
python3 chaos_client.py upload config.txt matrix &
