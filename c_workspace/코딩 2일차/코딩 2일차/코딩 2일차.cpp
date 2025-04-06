#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

void main() {
	int num;
	printf("점수를 입력하세요.");
	scanf("%d", &num);
	if (num >= 90) printf("A");
	else if (num >= 80) printf("B");
	else if (num >= 70) printf("C");
	else if (num >= 60) printf("D");
	else printf("F");

	printf("\n");
	switch (num)
	{
	case 'A':
		printf("이 학생은 천재입니다.");
		break;
	case 'B':
		printf("이 학생은 영재입니다.");
		break;

	default:
		printf("이 학생은 평범합니다.");
		break;
	}



}
