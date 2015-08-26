#check if enough arguments are given
if [ "$#" -gt "0" ]; then
    #check if the first argument is -h or --help
    if [[ "$1" == "-h" || "$1" == "--help" ]];then
	echo "$0 pathname"
	echo "Example: $0 ~/Pictures"
    #check if directory exist
    elif [ -d "$1" ]; then 
	echo "Path: $1 "
	cd $1
	find \( -name "*.gz" \) | xargs gunzip  
    else 
	echo "Error: Cannot find directory"
    fi
    
else
    echo "Error: Enter path."
fi
