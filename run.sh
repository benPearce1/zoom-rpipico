address=http://192.168.86.35
while true
do
    sleep 2
    state=$(osascript ~/bin/zoom.scpt)
    curl -X POST $address -d "$state"
done

