#include <stdio.h>

int rec_func(int n);

int main() {
	int res;
	res = rec_func(10);
	printf("result: %d\n", res);
	return 0;
}

int rec_func(int n) {
	if (n == 1) return 1;
	else return (n + rec_func(n - 1));

}