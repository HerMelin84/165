#ctrl+c handler.
function control_c() {
    echo " "
    echo "Bye Bye"
    exit
}
#infinite loop. prints time every second. interrupted by ctrl+c
while true; do
    date
    sleep 1
    trap 'control_c' SIGINT
done
