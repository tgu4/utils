on LaunchSession(serverName, launchCmd, profileName)
    tell application "System Events"
        set isRunning to exists (processes where name is "iTerm2")
    end tell

    tell application "iTerm"
        if not isRunning then
            log "not running"
            activate -- this will start iTerm

            close the first session of the first tab of the first window
            set _window to (create window with profile profileName)
            tell _window
                set _session to first session of first tab of _window

                select _session
                tell _session
                    set name to serverName
                    write text launchCmd
                end tell
            end tell
        else
            tell application "iTerm"
                activate
                tell current window to set tb to create tab with profile profileName
                tell current session of current window to set name to serverName
                tell current session of current window to write text launchCmd
            end tell
        end if
    end tell
end LaunchSession
