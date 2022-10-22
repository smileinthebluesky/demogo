#!/bin/sh

#The handler needs to be running continuously to receive events from Lambda so we put it in a loop
while true
do
	HEADERS="$(mktemp)"
	 # Grab an invocation event and write to temp file, this step will be blocked by Lambda until an event is received
	curl -sS -LD "$HEADERS" -X GET "http://${AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime/invocation/next" -o /tmp/event.data
	
	# Extract request ID by scraping response headers received above
	REQUEST_ID=$(grep -Fi Lambda-Runtime-Aws-Request-Id "$HEADERS" | tr -d '[:space:]' | cut -d: -f2)
	# Extract OPA variables from temp file created event and delete temp file
	tier=$(jq -r '.tier' </tmp/event.data)
	role=$(jq -r '.role' </tmp/event.data)
	rm /tmp/event.data
							   
	# Pass Payload to OPA and Get Response
        echo $tier
	echo $role

	RESPONSE="dump"
	while [[ "$RESPONSE" ==  "dump" || -z "$RESPONSE" ]] 
	do
		RESPONSE=$(curl -s -X POST "http://localhost:8181/v1/data/demogo/service" -d '{ "input" : { "tier" : '"\"${tier}\""', "role" : '"\"${role}\""' } }' -H "Content-Type: application/json")

	done

	echo $RESPONSE

	# Send Response to Lambda
	curl -s -X POST "http://${AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime/invocation/$REQUEST_ID/response"  -d "$RESPONSE"  -H "Content-Type: application/json"

done
