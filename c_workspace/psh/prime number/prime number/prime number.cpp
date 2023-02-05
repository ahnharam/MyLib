#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
void main() {
	int num = 0, count1 = 0, count2 = 0;
	printf("2 이상의 정수를 입력하세요 : ");
	scanf("%d", &num);
	for (int i = 1; i <= num; i++) {
		for (int j = 1; j < i; j++) {
			if (i % j == 0)
				count1++;
		}

		if (count1 == 1) {
			printf("%5d\t", i);
			count2++;
			
			if (count2 % 5 == 0)
				printf("\n");

		}

		count1 = 0;

	}

	// 소수가 아닌 수를 출력, 7칸 마다 줄 넘기기 
	// while문 사용하기 
	

	
	

}