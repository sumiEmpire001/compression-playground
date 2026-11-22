#pragma once
#include <cstddef>
#include <cstdint>
namespace lord_sumi {
struct Rle {
 static bool encode(const uint8_t* input,std::size_t size,uint8_t* output,std::size_t capacity,std::size_t& written){
  written=0;if((size&&!input)||!output||capacity<4)return false;
  std::size_t needed=4;
  for(std::size_t i=0;i<size;){std::size_t run=1;
   while(run<255&&run<size-i&&input[i+run]==input[i])++run;
   if(needed>capacity||capacity-needed<2)return false;
   needed+=2;i+=run;
  }
  output[0]='R';output[1]='L';output[2]='E';output[3]='1';written=4;
  for(std::size_t i=0;i<size;){std::size_t run=1;
   while(run<255&&run<size-i&&input[i+run]==input[i])++run;
   output[written++]=static_cast<uint8_t>(run);output[written++]=input[i];i+=run;
  }
  return true;
 }
 static bool decode(const uint8_t* input,std::size_t size,uint8_t* output,std::size_t capacity,std::size_t& written){
  written=0;
  if(!input||size<4||!output||input[0]!='R'||input[1]!='L'||input[2]!='E'||input[3]!='1'||((size-4)%2))return false;
  std::size_t needed=0;
  for(std::size_t i=4;i<size;i+=2){if(input[i]==0||needed>capacity||capacity-needed<input[i])return false;needed+=input[i];}
  for(std::size_t i=4;i<size;i+=2)for(unsigned j=0;j<input[i];++j)output[written++]=input[i+1];
  return true;
 }
};
}