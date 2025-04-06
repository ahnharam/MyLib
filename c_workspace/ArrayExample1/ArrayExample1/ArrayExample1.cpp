#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

void main() {
	int array[5] = {10, 10, 10, 10, 10};
	array[0] = 10; // 4byte
	array[1] = 10;// 4byte
	array[2] = 10;// 4byte
	array[3] = 10;// 4byte
	array[4] = 10;// 4byte

	/*printf("숫자를 입력하세요");
	scanf("%d", &array[0]);

	char ch[10];

	printf("문자를 입력하세요");
	scanf("%c", &ch[0]);


	printf("문자열를 입력하세요");
	scanf("%s", ch);*/

	//printf("array[0] : %d\n", array[0]);
	//printf("array[1] : %d\n", array[1]);
	//printf("array[2] : %d\n", array[2]);
	//printf("array[3] : %d\n", array[3]);
	//printf("array[4] : %d\n", array[4]);

	int count = sizeof(array) / sizeof(array[0]);

	printf("%d\n", count);

	for (int i = 0; i < count; i++) {
		printf("array[%d] : %d\n", i, array[i]);
	}
}