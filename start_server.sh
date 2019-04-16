#!/bin/bash
python server.py config.txt localhost 5001 &
python server.py config.txt localhost 5002 &
python server.py config.txt localhost 5003 &
python server.py config.txt localhost 5004 &
python server.py config.txt localhost 5005 &
echo "sleep 0.5sec to let servers start..."
sleep 0.5
python chaos_client.py upload config.txt matrix &