property muteAudio : "Mute audio"
property unmuteAudio : "Unmute audio"
property startVideo : "Start Video"
property stopVideo : "Stop Video"

if application "zoom.us" is running then
	tell application "System Events"
		tell application process "zoom.us"
			if exists (menu item muteAudio of menu 1 of menu bar item "Meeting" of menu bar 1) then
				# click menu item muteAudio of menu 1 of menu bar item "Meeting" of menu bar 1
				set mic to "Unmuted"
			else
				# click menu item unmuteAudio of menu 1 of menu bar item "Meeting" of menu bar 1
				set mic to "Muted"
			end if
			if exists (menu item startVideo of menu 1 of menu bar item "Meeting" of menu bar 1) then
				# click menu item startVideo of menu 1 of menu bar item "Meeting" of menu bar 1
				set camera to "Off"
			else
				# click menu item stopVideo of menu 1 of menu bar item "Meeting" of menu bar 1
				set camera to "On"
			end if
		end tell
	end tell
else
	set returnValue to ""
end if


return "{ 'mic': '" & mic & "', 'camera': '" & camera & "'}"