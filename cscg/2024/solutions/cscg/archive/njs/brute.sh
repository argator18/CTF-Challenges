#!/bin/bash

# Set the keyword you are looking for
keyword="CS"


offset=100

doit(){
  if [ $# -gt 1 ]; then
    python3 exploit.py $(python -c "print($1)")> /dev/null
    echo test
  fi
  python3 join.py $1
}





# Function to check if an array contains a specific element
array_contains () {
    local array="$1[@]"
    local seeking=$2
    local in=1
    for element in "${!array}"; do
        if [[ $element == "$seeking" ]]; then
            in=0
            break
        fi
    done
    return $in
}

initial_strings=("")
# Loop indefinitely until the keyword is found
for (( i=1; i<=4000; i++ )); do
    # Inner loop that executes 100 times for each i
    for (( j=1; j<=1; j++ )); do
      # Execute your command here, and pipe its output to grep
      # Replace `your_command_here` with the command you want to execute
      if [[ j -eq 1 ]]; then 
        output=$(doit $i $j | tr -d '\000')
      else
        output=$(doit $i | tr -d '\000')
      fi
      string="$(echo $output | strings)"

      readarray -t array_new_strings <<< "$string"
      #echo "${array_new_strings[@]}"

      # Loop through new strings and check if they are in the initial array
      for str in "${array_new_strings[@]}"; do
          array_contains initial_strings "$str"
          if [ $? -eq 1 ]; then
              # If the string is not found, add it to the array and print it
              initial_strings+=("$str")
              echo "$i + $str"
          fi
      done
      
      output=$(echo $output | grep "$keyword")

      # Check the exit status of grep
      if [ $? -eq 0 ]; then
          echo "Keyword found: stopping the loop."
          break  # Exit the loop if grep found the keyword
      fi
    done
done

echo "Loop has been exited."



