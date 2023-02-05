#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>

void main() {
	char str1[80] = "cat";

	strcpy_s(str1, "tiger");

	printf_s("%s", str1);

	char str[10];
	puts("입력된 문자열 : ");
	gets_s(str);
	puts(str);

}