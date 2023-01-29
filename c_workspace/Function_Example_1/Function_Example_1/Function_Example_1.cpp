#include <stdio.h>

// 선언
void print(int c);
int sum(int x, int y);

void main() {
	// 함수 == function
	int a = 10;
	int b = 20;

	// 호출
	int c = sum(a, b);

	// 호출
	print(c);
}

// 정의
void print(int x) {
	printf("출력\n %d", x);
}

//			10		20
// 정의
int sum(int x, int y) {
	printf("출력 %d\n", x);
	printf("출력 %d\n", y);
	printf("출력 %d\n", x + y);
	//		30
	return x + y;
}