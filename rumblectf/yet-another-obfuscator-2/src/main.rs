mod circuit;
mod garble;
mod rng;
mod cut_and_choose;
mod hashable;
mod oblivious_transfer;

use std::{fs, net::TcpListener, thread};

use circuit::Circuit;
use cut_and_choose::CutAndChooseServer;
use kctf_pow::KctfPow;
const INPUTLEN: usize = 128;

const POW_DIFFICULTY: u32 = 1337;

fn to_bits(bytes: impl IntoIterator<Item=u8>) -> Vec<bool>{
    let bytes = bytes.into_iter();
    let mut bits = if let Some(n) = bytes.size_hint().1 {
        Vec::with_capacity(8*n)
    } else {
        Vec::new()
    };
    for b in bytes {
        for i in 0..8 {
            bits.push(b & (1<<i) != 0)
        }
    }
    bits
}

fn main() {
    let mut circuit = Circuit::new(INPUTLEN,INPUTLEN);
    let alice = circuit.get_alice_inputs();
    let bob = circuit.get_bob_inputs();
    let diff = circuit.bitwise_xor(&alice, &bob);
    let any_diff = circuit.or_nary(&diff);
    let out = circuit.not(any_diff);
    circuit.add_output(out);
    let circuit = Box::leak(Box::new(circuit)) as &Circuit;

    let pow = Box::leak(Box::new(KctfPow::new())) as &KctfPow;

    let flag = fs::read_to_string("./flag.txt").expect("Could not read flag").trim().to_string();
    let input = to_bits(flag.bytes());
    assert_eq!(input.len(), INPUTLEN);
    let input = Box::leak(Box::new(input)) as &[bool];


    
    let listener = TcpListener::bind("0.0.0.0:7133").expect("Could not start listener");
    for client in listener.incoming() {
        match client {
            Ok(stream) => {
                thread::spawn(move || { 
                let challenge = pow.generate_challenge(POW_DIFFICULTY);
                if let Err(_) = bincode::serialize_into(&stream, &challenge.to_string()) {
                    println!("Couldn't send pow");
                    return;
                }
                let pow_solution: String = match bincode::deserialize_from(&stream) {
                    Ok(s) => s,
                    Err(err) => {println!("Couldn't read pow: {}", err); return}
                };
                if challenge.check(&pow_solution) != Ok(true) { 
                    println!("Invalid POW");
                }



                let server = CutAndChooseServer::new(circuit, input);
                match server.run(&stream) {
                    Ok(_) => {}
                    Err(err) => {
                        println!("Execution error: {:?}", err);
                    }
                }
                
            });}
            Err(err) =>  {
                println!("Connection error: {:?}", err);
            }
        }
    }
}
