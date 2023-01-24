#define _CRT_SECURE_NO_WARNINGS    // scanf 보안 경고로 인한 컴파일 에러 방지
#include <stdio.h>

void main() {
	// 1. "점수를 입력하세요" 출력해야함
	// 2. 점수를 입력 받아야함
	// 3. 점수 
	/*
		90 >= A
		80 >= B
		70 >= C
		60 >= D
	*/
	// 4. 점수에 맞춰서  A,B,C,D 가 출력되야함
	int score = 0;
	char grade = ' ';

	printf("점수를 입력하세요 : ");
	scanf("%d", &score);

	/*
		if
		else if
		else
	*/

	if (score >= 90) grade = 'A';
	else if (score >= 80) grade = 'B';
	else if (score >= 70) grade = 'C';
	else if (score >= 60) grade = 'D';
	else grade = 'F';

	/*
		switch

		입력값 = 90
		grade = A
	*/

	switch (grade)
	{
		case 'A':
			printf("이 학생은 천재입니다.");
			break;
		case 'B' : 
			printf("이 학생은 영재입니다.");
			break;

		default:
			printf("이 학생은 평범합니다.");
			break;
	}
}
