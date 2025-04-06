#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int result();
void voidFunction();
void resultWithInt(int x);

void main() {
	resultWithInt(10);
}

int result() {
	return 10;
}

void voidFunction() {

}

void resultWithInt(int x) {

	if (x == 0) return;

	int y = x - 1;

	printf("y : %d\n", y);
	resultWithInt(y);
}