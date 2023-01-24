#include <stdio.h>

void main() 
{
	printf("hello world\n");
	int num1 = 10;
	long long1 = 10L;
	float num3 = 3.14f;
	printf("%f\n", num3);
	char char1 = 'ab';
	//printf("%s\n", char1);
	double double1 = 3.1415921234567898765432123456789876543212345678987654312;
	printf("%le\n" , double1);
	printf("%.8f\n" , double1);
	printf("%s hello %s hi %s\n" , "mad" , "asd" , "sda");
	int num4 = 7;
		int num5 = 5;
		unsigned int num6 = num4 * num5;
		printf("%d\n", num6);
		char char2[10] = "klllasss";
		printf("%s\n", char2);
		const  int named = 90;
		printf("%d\n" , named);
			int num2;
		num2 = 20;
		printf("%d\n", num2);
		num2 = 30;
		printf("%d\n", num2);
		//named = 100;

}