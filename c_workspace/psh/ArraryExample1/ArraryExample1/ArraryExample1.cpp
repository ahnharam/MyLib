#include <stdio.h>

void main() {
	int array[5] = {10,10,10,10,10};
	array[0] = 10; //int=4byte
	array[1] = 10;
	array[2] = 10;
	array[3] = 10;
	array[4] = 10;

	printf("숫자를 입력하세요");
	scanf("%d", &array[0]);

	char ch[10];

	printf("문자를 입력하세요");
	scanf("%c", &ch[0]);

	printf("문자열을 입력하세요");
	scanf("%s", ch);

	for (int i = 0; i < 5;i++) {
		printf("array[%d] : %d\n", i, array[i]);
	}
}