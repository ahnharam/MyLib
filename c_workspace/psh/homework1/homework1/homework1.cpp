﻿#include <stdio.h>
void main(){
	int i;
	int j;
	for (i = 0; i < 5; i++) {
		for (j = 0; j < 5; j++){ 
			if ((i == j || i + j == 4))
				printf("*");
			else printf(" ");
			
			
		}
		printf("\n");
	 }
	
	}