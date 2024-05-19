#!/usr/bin/env zsh

echo "Welcome to the Mystical Coin CTF Adventure!"
echo "In your bag, you carry a special coin, known for always bring you luck. You've been throwing it repeatedly, lost in thought."
echo "After $RANDOM throws, you finally get your most precious sequence:"
sleep 1
echo ""

PASSKEY=""

function mystical_coin_flip {
    echo "An ancient coin lands in your hand. Will it be heads (H) or tails (T)?"
    read "?Your call: " user_call

    # Validate input
    if ! [[ "$user_call" =~ ^[HhTt]$ ]]; then
        echo "Invalid call. Please choose heads (H) or tails (T)."
        exit 1
    fi

    # Simulate a coin flip
    if (( $RANDOM % 2 )); then
        coin_result="H"
    else
        coin_result="T"
    fi
    PASSKEY+=$coin_result
    echo "The coin lands on $coin_result."

    if [[ ${user_call:u} == ${coin_result:u} ]]; then
        echo "Fortune smiles upon you!"
        echo ""
        return 0
    else
        echo "Oh no! The coin has other plans..."
        echo ""
        return 1
    fi
}

mystical_coin_flip
mystical_coin_flip
mystical_coin_flip
mystical_coin_flip
mystical_coin_flip

echo "Distracted by this particular sequence of flips, you suddenly find yourself at the entrance of an ancient and mystical land."
echo "Your destiny in this realm is mysteriously linked to this coin."
sleep 1
echo ""

echo "You stand at a mystical crossroads, with two paths forward: the Portal of Fate (P) or the Oracle's Den (O)."
read "?Choose P for the Portal of Fate or O for the Oracle's Den: " choice


if [[ $choice == [Pp]* ]]; then
    echo "You approach the Portal of Fate, shimmering with ancient energy."
    if mystical_coin_flip; then
        echo "As the portal swirls open, a radiant light envelops you, transporting you to a realm beyond imagination."
        echo "In this realm, you navigate a labyrinth of stars, solve riddles whispered by ancient trees, and unlock a celestial puzzle that aligns the constellations."
        echo "At the heart of the realm, you find a crystal dais. Etched upon it in shimmering light is the flag part: 'PART2}'."
        echo "A voice, as old as time, echoes around you, 'The journey through the stars is a reflection of the journey within. You have navigated both with wisdom.'"
        echo "With a flash of light, you're back at the portal, holding a token from the starry realm as a memento of your adventure."
    else
        echo "The portal catapults you into space, where you become a human comet, blazing through the cosmos!"
        echo "It's a breathtaking sight, but alas, a comet can't collect flag parts."
    fi
else
    echo "You tread cautiously towards the Oracle's Den. The coin is soaring through the air, heading back to your hand."
    if mystical_coin_flip; then
        echo "The Oracle guides you to a hidden library, a sanctuary of ancient secrets."
        echo "Within its silent walls, you discover a curious scroll sealed with a mystic symbol."
        echo "Unfurling the scroll reveals a series of enigmatic symbols and a cryptic cipher:"

        for ((i=1; i<=32; i++))
        do
            PASSKEY=$(echo $PASSKEY$RANDOM | md5sum)
        done
        export PASSKEY=$PASSKEY
        echo "CSCG{FLAG_PART_1_" | openssl enc -aes-256-cbc -e -pass env:PASSKEY 2>/dev/null | hexdump -C

        echo "The Oracle hints that it's a hexadecimal code, part of a larger puzzle."
        echo "She whispers that understanding its meaning requires knowledge found only in the distant lands of your quest."
        echo "This cipher, a fragment of your flag, ignites a deeper curiosity, leading you to seek the wisdom needed to unlock its secrets."
    else
        echo "The Oracle laughs so heartily at your coin call that a gust of wind from her chuckle sweeps you off your feet."
        echo "You find yourself blown into a painting, transforming into a permanent, smiling figure in an idyllic landscape within the frame."
        echo "As you adjust to your new painted existence, surrounded by serene hills and a peaceful river, you realize that while this painted world is beautiful, it holds no flag parts for your quest."
        echo "You become a cherished character in the Oracle's gallery, admired by all who pass by, but your journey for the flag ends in this artistic realm."
    fi
fi
