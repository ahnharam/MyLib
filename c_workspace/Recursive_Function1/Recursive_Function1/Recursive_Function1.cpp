#include <stdio.h>

int res_function(int num);
int for_function(int num);

void main() {
	int res;
	//res = res_function(10);
	res = for_function(10);
	printf("result : %d\n", res);
}

int res_function(int num) {
	char str[] = "else";

	//num = 9
	if (num == 1) return 1;		// i != 1 
	else return (num /*9*/ + res_function(num - 1 /*8*/));

	// num == 10
	// return (10 + res_function(9))

	// num == 9
	// return (9 + res_function(8))

	// num == 8
	// return (8 + res_function(7))
}

int for_function(int num) {
	
	// 1. summary 변수 필요
	// 2. num 만큼 반복
	// 3. summary 반환
	int summary = 0;

	for (; num > 0; num--) {
		summary += num;
	}
	return summary;
}