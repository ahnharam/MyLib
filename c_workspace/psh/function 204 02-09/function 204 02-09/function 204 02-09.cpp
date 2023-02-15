#include <stdio.h>

void sum(int a);

int main() {
	sum(10);
	sum(100);
	return 0;
}

 void sum(int a) {
	 int i, tot = 0;
	 for (i = 1; i <= a; i++) {
		 tot += i;
		 
	 }
	 printf("1부터 %d까지의 합은 %d입니다.\n",a, tot);
}