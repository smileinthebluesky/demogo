#!/bin/sh
exit_script() {
	echo "Shutting down..."
	trap - SIGINT SIGTERM # clear the trap
}
trap exit_script SIGINT SIGTERM

echo "Starting Open Policy Agent"
exec /opa/opa run -s /opa/ & 
echo "Running on Lambda - Starting Handler..."
exec /var/runtime/opa-lambda.sh
