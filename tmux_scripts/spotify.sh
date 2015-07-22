
is_open=`osascript -e 'tell application "System Events" to (name of processes) contains "Spotify"'`;
if [ $is_open = "true" ]; then
    state=`osascript -e 'tell application "Spotify" to player state as string'`;
    if [ $state = "playing" ]; then
        artist=`osascript -e 'tell application "Spotify" to artist of current track as string'`;
        track=`osascript -e 'tell application "Spotify" to name of current track as string'`;
        echo "#[bold] ♬ $artist#[nobold] - $track";
    fi
fi


