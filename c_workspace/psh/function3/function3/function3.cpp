﻿#include <stdio.h>
double centi_to_meter(int cm);
int main() {
	double res;
	res = centi_to_meter(187);
	printf("%.2lfm\n", res);
	return 0;
}
double centi_to_meter(int cm) {
	double meter;
	meter = cm / 100.0;
	return meter;
}