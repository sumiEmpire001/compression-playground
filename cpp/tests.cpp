#include "core.hpp"
#include <cassert>
#include <cstdint>
int main(){
 using lord_sumi::Rle;
 uint8_t input[]={7,7,7,2,2,9},encoded[32],decoded[32];
 std::size_t n=0,m=0;
 assert(Rle::encode(input,6,encoded,32,n)&&n==10);
 assert(Rle::decode(encoded,n,decoded,32,m)&&m==6);
 for(int i=0;i<6;++i)assert(decoded[i]==input[i]);
 assert(!Rle::encode(input,6,encoded,5,n)&&n==0);
 uint8_t invalid[]={'R','L','E','1',0,7};
 assert(!Rle::decode(invalid,6,decoded,32,m));
 assert(!Rle::decode(encoded,9,decoded,32,m));
 assert(!Rle::decode(encoded,10,decoded,2,m));
 assert(Rle::encode(nullptr,0,encoded,32,n)&&n==4);
 assert(Rle::decode(encoded,n,decoded,32,m)&&m==0);
}