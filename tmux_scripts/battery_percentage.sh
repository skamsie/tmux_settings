#!/usr/bin/env bash

command_exists() {
    local command="$1"
    type "$command" >/dev/null 2>&1
}

print_battery_percentage() {
    # percentage displayed in the 2nd field of the 2nd row
    if command_exists "pmset"; then
        pmset -g batt | awk 'NR==2 { gsub(/;/,""); print $2 }'
    elif command_exists "upower"; then
        for battery in $(upower -e | grep battery); do
            upower -i $battery | grep percentage | awk '{print $2}'
        done | xargs echo
    elif command_exists "acpi"; then
        acpi -b | grep -Eo "[0-9]+%"
    fi
}

main() {
    full='■■■■■'
    ninety='■■■■◧'
    eighty='■■■■□'
    seventy="■■■◧□"
    sixty='■■■□□'
    fifty='■■◧□□'
    fourty='■■□□□'
    thirty='■◧□□□'
    twenty='■□□□□'
    ten='◧□□□□'
    empty="#[fg=red]□□□□□#[fg=default]"

    bp=$(print_battery_percentage)
    x=${bp%?}
    if (($x <= 9)); then
        icon=$empty
    elif (($x <= 19)); then
        icon=$ten
    elif (($x <= 29)); then
        icon=$twenty
    elif (($x <= 39)); then
        icon=$thirty
    elif (($x <= 49)); then
        icon=$fourty
    elif (($x <= 59)); then
        icon=$fifty
    elif (($x <= 69)); then
        icon=$sixty
    elif (($x <= 79)); then
        icon=$seventy
    elif (($x <= 89)); then
        icon=$eighty
    elif (($x <= 99)); then
        icon=$ninety
    elif (($x == 100)); then
        icon=$full
    fi
    echo "$icon $(print_battery_percentage)"

}
main
