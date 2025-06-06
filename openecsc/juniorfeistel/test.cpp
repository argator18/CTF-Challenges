#include <bits/stdc++.h>
#include <bitset>

#define ROUNDS 1
#define BITS 32
#define MASK ((1LL<<BITS)-1)
#define MUL(x,y) ((x*y) & MASK)
#define ADD(x,y) ((x+y) & MASK)
#define SUB(x,y) ((x-y+(1LL<<BITS)) & MASK)
#define ROL(x,r) (((x << (r)) | (x >> (BITS - (r)))) & MASK)
#define ROR(x,r) (((x >> (r)) | ((x << (BITS - (r))))) & MASK)

using namespace std;

const uint RC[] = {2667589438, 3161395992, 3211084506, 3202806575, 827352482, 3632865942, 1447589438, 3161338992};

uint round_f(uint x, uint k, int i){
    return MUL(3, ROL(ADD(k, x), 19)) ^ MUL(5, ROR(SUB(k, x), 29)) ^ ADD(k, MUL((uint)i, 0x13371337LL));
}

vector<uint> key_schedule(uint key_l, uint key_r, int n_rounds){
    vector<uint> keys;
    keys.push_back(key_l);

    for(int i = 0; i<n_rounds-2; i++){
        uint tmp = key_l;
        key_l = key_r;
        key_r = ADD(tmp, round_f(key_r, RC[i], i+1));
        keys.push_back(key_l);
    }

    keys.push_back(key_r);
    return keys;
}

array<uint, 2> encrypt_block(uint l, uint r, vector<uint>& round_keys, int n_rounds){
    for(int i = 0; i < n_rounds; i++){
        uint tmp = l;
        l = r;
        r = ADD(tmp, round_f(r, round_keys[i], i+1));
    }

    return {l, r};
}

unsigned long long key_from_urandom(){
    ifstream urandom("/dev/urandom", ios::in|ios::binary);
    unsigned long long ret = -1;
    if(urandom){
        urandom.read(reinterpret_cast<char*>(&ret), 8);
        if(!urandom) ret = -1;
        urandom.close();
    }
    return ret;
}

int main(){
    //unsigned long long master_key = key_from_urandom();
    unsigned long long master_key = 0xdeadbeefcafebabe;
    unsigned long long user_guess;
    vector<uint> keys = key_schedule(master_key >> BITS, master_key & MASK, ROUNDS);
    vector<pair<uint, uint>> user_inputs;

    if(master_key == -1){
        cout << "Something wrong..." << endl;
        return 1;
    }

    //long input1 = 0x1;
    for (long input1=0; input1 < 10000; input1++){
      uint first = input1 >> BITS;
      uint second = input1 & MASK;

      array<uint, 2> res1 = encrypt_block(first, second, keys, ROUNDS);
      //cout << res[0] << ", " << res[1] << endl;
      
      long difference = 0x1;
      long input2 = input1 ^ difference;
      first = input2 >> BITS;
      second = input2 & MASK;

      array<uint, 2> res2 = encrypt_block(first, second, keys, ROUNDS);
      //cout << res[0] << ", " << res[1] << endl;
      
      std::bitset<64> binary(input1 ^ input2);
      
      //cout << "Input difference:  " << binary << endl;
      //cout << "Output difference: " << (res1[0] ^ res2[0]) << (res1[1] ^ res2[1]) << endl;
      std::bitset<32> binary1((res1[0] ^ res2[0]));
      std::bitset<32> binary2((res1[1] ^ res2[1]));
      cout << "Out diff " << input1 << " : " << binary1 << binary2 << " res1: " << res1[0]<< ":" <<res1[1] <<" res2: " << res2[0]<< ":" <<res2[1] << endl;
    }
    return 0;
}
