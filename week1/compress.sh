#check if enought arguments are given
if [[ "$#" -eq "1" || "$#" -gt "1" ]]; then
    #check if the first argument is -h or --help
    if [[ "$1" == "-h" || "$1" == "--help" ]];then
	echo "$0 pathname size(in kilobytes) "
	echo "Example: $0 ~/Pictures 20"
    #check if directory exist
    elif [ -d "$1" ]; then	
	cd $1
	    find \( -size "+$2k" \) | xargs gzip
    else
	echo "Error: Cannot find directory"
    fi
    
else
    echo "Error: Enter path and filesize"
fi
