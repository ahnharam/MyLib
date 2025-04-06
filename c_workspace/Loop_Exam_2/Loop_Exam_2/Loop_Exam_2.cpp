#define _CRT_SECURE_NO_WARNINGS    // scanf 보안 경고로 인한 컴파일 에러 방지
#include <stdio.h>

void main() {

	int i = 0;
	int j = 0;

	for (i = 0; i < 10; i++) {
		printf("i = %d\t", i);
		for (j = 0; j < 10; j++) {

			if(j == 5) continue;
			printf("j = %d\t", j);
		}

		printf("\n");
	}
}