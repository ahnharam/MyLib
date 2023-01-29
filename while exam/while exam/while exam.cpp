#include <stdio.h>

void main() {
	int i;
	for (i = 0; i < 10; i++)
	{
		printf("$\n");
	}
	i = 0;
	printf("\n");

	int a = 1;
	while (a < 1024) {
		a = a * 2;
		printf("$\n");
	}
	a = 0;
	printf("\n");

	int b = 1;
	do
	{
		b = b * 2;
		printf("$\n");
	} while (b < 1024);


}