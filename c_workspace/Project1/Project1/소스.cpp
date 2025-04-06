#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

void main() {
    int sum = 0;
    int n;
    char arr[100];
    scanf("%d", &n);
    scanf("%s", &arr);
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    printf("%d", sum);




}