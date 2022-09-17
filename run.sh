address=http://192.168.86.34
while true
do
    sleep 2
    state=$(osascript ~/bin/zoom.scpt)
    time=$(date +%H:%M:%S)
    echo $time $state
    curl -s -X POST $address -d "$state"
done

