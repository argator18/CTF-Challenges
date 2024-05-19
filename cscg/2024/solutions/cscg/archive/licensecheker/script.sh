#!/bin/bash

# Characters to iterate over
chars=( {0..9} {A..Z} )

try=0
# Nested loop for each 'X' placeholder
for char1 in "${chars[@]}"; do
    for char2 in "${chars[@]}"; do
        for char3 in "${chars[@]}"; do
                    echo -ne "\rtry: $try"
                    ((try++))
                    # Construct the string by replacing each 'X' with the current character from its loop
                    modifiedString="A1K3B-AAFL1-BB82C-X0GXX-BC8NC"
                    modifiedString="${modifiedString/X/$char1}"
                    modifiedString="${modifiedString/X/$char2}"
                    modifiedString="${modifiedString/X/$char3}"
                    
                    # Output or use the fully constructed string
                    commandOutput=$( licensecheck "$modifiedString"| grep "is valid") 
                    
                    # If "Valid" is found in the command output, print the modified string and exit the script
                    if [ ! -z "$commandOutput" ]; then
                        echo "Valid string found: $modifiedString"
                        exit 0
                    fi
        done
    done
done

