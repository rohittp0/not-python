#include <iostream>
#include <cmath>
int main(int argc, char *argv[]){
float number;
float i;
std::cout<<"Enter number to check if it is prime or not: ";
std::cin>>number;
if(number==1){
std::cout<<"1 is neither prime nor composite";
return 0;
}
i = 2;
while(i<=number/2){
if((int)number%(int)i==0){
std::cout<<number<<" is not a prime number";
return 0;
}
i = i+1;
}
std::cout<<number<<" is a prime number";
return 0;
}
