package ClassStudy;

public class Calc {
   long add(long a, long b){
       return a+b;
   }
   long subtract (long a, long b){
       return a-b;
   }
   long multi(long a, long b){
       return a*b;
   }
   double divide(double a, double b){
       return a/b;
   }
   
   void resultData(Data data) {
	   data.data1 = 10;
	   data.data2 = 20;
	   data.data3 = 30;
	   data.data4 = 40;
   }
}
