#include <stdio.h>

void main() {
	int a = 10;

	// while 문
	// 처음부터 조건을 확인하고 들어간다.
	// 처음에 조건이 거짓이면 실행 x

	while (a > 0) {
		printf("a:%d\n", a);
		a--;
	}
	a = 0;

	// do while 문
	// 맨처음은 무조건 실행 
	// 

	do {
		printf("a:%d\n", a);
		a--;
	} while (a == 10);
}