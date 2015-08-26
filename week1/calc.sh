#check if enought arguments are given
if [ $# -gt 0 ]; then
    if [[ "$1" == "-h" || "$1" == "--help" ]];then
	echo '$0 "what to calculate"'
	echo 'Example: $0 "5+5"'
    else
	input=$((($1)))	
	echo "$1=$input"
    fi
else
    echo "Not enough arguments given"
    echo "Give me something to calculate."
fi
