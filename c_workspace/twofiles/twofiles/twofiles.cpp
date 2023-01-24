#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
void main() {
	int num1 , num2;
	printf("키와 몸무게를 입력해주세요.: ");
	scanf("%d%d",&num1,&num2);
	printf("입력하신 키는 %d , 입력하신 몸무게는 %d입니다.", num1 , num2);
	char num3[7];
	printf("이름을 입력하세요.:");
	scanf("%s", num3);
	printf("입력하신 이름은 %s 입니다", num3);
}