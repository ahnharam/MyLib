#include <stdio.h>

void main() {
	int a = 10;

	// while 문
	// 처음부터 조건을 확인하고 들어간다
	// 처음에 조건이 거짓이면 실행을? 안한다

	// 실행되는 횟수 : 10번
	while (a > 0) {
		printf("a : %d\n", a);
		a--;
	}

	// a 출력되는 마지막 값 : 1

	// 현재 a의 값은 ?
	// 0
	//---------------------------
	printf("\n");
	printf("a : %d\n", a);

	// do while 문
	// 맨처음은 무조건 실행

	// 음식점에 처음가면 보는게 메뉴판
	// 

	do {
		printf("\n");

		printf("a : %d\n", a);
	} while (a == 0);
}