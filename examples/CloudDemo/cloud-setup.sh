#!/bin/bash
# Author: Sebastian Romero @sebromero
# SEE: https://github.com/arduino/arduino-cloud-cli

THING_NAME="Live MicroPython Demo"
THING_FILE="./cloud_demo_thing.yml"
DASHBOARD_FILE="./cloud_demo_dashboard.yml"
DASHBOARD_NAME=$THING_NAME

# Check if commands exist
command -v arduino-cloud-cli >/dev/null 2>&1 || { echo >&2 "❌ arduino-cloud-cli is required but it's not installed."; exit 1; }

# Check if credentials exist
arduino-cloud-cli credentials find > /dev/null 2>&1

if [ $? -ne 0 ]; then    
    arduino-cloud-cli credentials init
else
    echo "✅ Arduino IoT Cloud credentials found."
fi

# Create build folder to store json response files
mkdir "build" > /dev/null 2>&1

# Check if thing is already created
arduino-cloud-cli thing list --format json | grep '"name": "'"$THING_NAME"'"' > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Creating thing '$THING_NAME' ..."
    arduino-cloud-cli thing create --name "$THING_NAME" --template $THING_FILE --format json > build/thing.json
    if [ $? -ne 0 ]; then
        echo "❌ Couldn't create thing '$THING_NAME'"
        exit 1
    fi
else
    echo "✅ Thing '$THING_NAME' already exists."
fi

THING_ID=$(cat build/thing.json | sed -n "s/.*\"id\": \"\([0-9A-Za-z\-]*\)\".*/\1/p")

function maybeCreateDashboard(){
    local dashboardName=$1
    local dashboardFile=$2
    local thingID=$3
    local outputFilename=$4

    # Check if dashboard already exists
    arduino-cloud-cli dashboard list --format json | grep '"name": "'"$dashboardName"'"' > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Creating dashboard '$dashboardName' using thing ID $THING_ID ..."
        arduino-cloud-cli dashboard create --name "$dashboardName" --template $dashboardFile --override template-thing-id=$thingID --format json > $outputFilename
        if [ $? -ne 0 ]; then
            echo "❌ Couldn't create dashboard '$dashboardName'"
            exit 1
        fi
    else
        echo "✅ Dashboard '$dashboardName' already exists."
    fi
}

maybeCreateDashboard "$DASHBOARD_NAME" "$DASHBOARD_FILE" "$THING_ID" "build/dashboard.json"
echo "✅ Setup completed. Now go to the Arduino IoT Cloud and associate your device with this Thing."
echo "👉 https://create.arduino.cc/iot/things/$THING_ID/setup"