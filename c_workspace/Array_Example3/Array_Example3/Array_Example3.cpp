#include <stdio.h>

void main() {
	int A[3] = { 1, 2, 3 }; // 초기화된 A 배열
	int B[10];				// 초기화되지 않은 B 배열
	int i;

	int count = sizeof(B) / sizeof(B[0]);

	// for
	// 정의 -> 조건 -> 증감

	for (i = 0; i < count; i++) {	// 반복하는 부분
		// B 배열에 A배열 값을 순차적으로 넣는데 
		// A[0] -> A[1] -> A[2] -> A[0]

		// if문
		if (i % 3 == 0) B[i] = A[0];
		else if (i % 3 == 1) B[i] = A[1];
		else if (i % 3 == 2) B[i] = A[2]; 

		// switch 문
		switch (i % 3)
		{
			case 0: B[i] = A[0]; break;
			case 1: B[i] = A[1]; break;
			case 2: B[i] = A[2]; break;
		}

		// 연산자만 활용
		B[i] = A[i % 3];
	}

	for (i = 0; i < count; i++) {
		printf("%d\t", B[i]);
	}
}