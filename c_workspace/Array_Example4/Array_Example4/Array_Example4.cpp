#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>

void main() {

	// 1. 문자열을 입력받는다

	// 2. 문자열 개수만큼 반복문을 돌린다.

	// 3. 아스키 코드값이 65보다 크거나 같고 90보다 작거나 같을 경우 대문자이다
	//	  아스키 코드값이 97보다 크거나 같고 122보다 작거나 같을 경우 소문자이다.

	char ch = 'A';
	char ch2 = ch + 32;
	printf("%c", ch2);

	// 4. 대문자일 경우 count++ 을 해준다.
	//    대문자일 경우 소문자로 치환한다.

	// 5. 바뀐문장과 개수를 출력한다.


}