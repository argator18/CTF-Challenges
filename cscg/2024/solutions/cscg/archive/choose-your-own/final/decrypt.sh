#!/usr/bin/zsh
PASSKEY=''
RANDOM=$1

echo $RANDOM
add(){
  if (( $RANDOM % 2 )); then
      coin_result="H"
  else
      coin_result="T"
  fi
  PASSKEY+=$coin_result
}
add
add
add
add
add
add


for ((i=1; i<=32; i++))
do
    PASSKEY=$(echo $PASSKEY$RANDOM | md5sum)
done
export PASSKEY=$PASSKEY
echo $PASSKEY

decrypted_output=$(openssl enc -aes-256-cbc -d -pass env:PASSKEY -in encrypt )
echo $decrypted_output
