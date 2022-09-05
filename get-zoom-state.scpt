property muteAudio : "Mute audio"
property unmuteAudio : "Unmute audio"
property startVideo : "Start Video"
property stopVideo : "Stop Video"

set mic to "Muted"
set camera to "Off"

if application "zoom.us" is running then
	tell application "System Events"
		tell application process "zoom.us"
			if exists (menu item muteAudio of menu 1 of menu bar item "Meeting" of menu bar 1) then
				set mic to "Unmuted"
			end if
			#if exists (menu item unmuteAudio of menu 1 of menu bar item "Meeting" of menu bar 1) then
			#	set mic to "Muted"
			#end if
			#if exists (menu item startVideo of menu 1 of menu bar item "Meeting" of menu bar 1) then
			#	set camera to "Off"
			#end if
			if exists (menu item stopVideo of menu 1 of menu bar item "Meeting" of menu bar 1) then
				set camera to "On"
			end if
		end tell
	end tell
end if


return "{ 'mic': '" & mic & "', 'camera': '" & camera & "'}"