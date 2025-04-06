#include <stdio.h>

void main() {
	// 반복문 문제
	//문제 1. while 문을 활용하여 $를 10번 출력하는 프로그램 작성
	//문제 2. do~while 문을 활용하여 $를 10번 출력하는 프로그램 작성
	//문제 3. for 문을 활용하여 $를 10번 출력하는 프로그램 작성
	int i = 0;
	for (; i < 10; i++) {
		printf("%d, $\t", i);
	}
	printf("\n");

	i = 0;
	while (i < 10) {
		printf("%d, $\t", i);
		i++;
	}
	printf("\n");

	i = 0;
	do {
		printf("%d, $\t", i);
		i++;
	} while (i < 10);
}