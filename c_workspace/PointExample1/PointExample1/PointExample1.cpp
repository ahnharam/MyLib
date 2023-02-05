#include <stdio.h>

/*
	포인터 : 변수들을 통째로 옮기는 이동수단

	구조체 : 변수의 집합
*/
void test(int* a);
void array(int* a);

void main() {


	/*int a = 10;
	int* b = &a;

	*b = 20;
	printf("%d", a);*/
	
	int a[10];
	int* b = a;

	*b = 10;
	*(b + 1) = 20;

	printf("%d", a[0]);
	printf("%d", a[1]);
}

// a = 10
void array(int* a) {
	*a = 10;
	printf("%d", *a);
}