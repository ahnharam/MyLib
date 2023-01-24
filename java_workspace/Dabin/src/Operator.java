
public class Operator {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// 연산자
		
		// ++ --
		
		// 사칙연산 + %
		
		// 시프트 연산자
		
		// 2진수 
		// 8진수
		// 10진수
		// 16진수
		
		// 128 64 32 16 	8 4 2 1
		// 0000 			1 1 0 1		<- 2진수 
		//								10진수 = 13
		
		//								16진수 - 0~F 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F 
		//								16진수 = D
		
		// << >> >>>
		//		  0000 0000 0000 0000 0000 0000 0000 0001
		int num1 = 1;

		//		  0000 0000 0000 0000 0000 0000 0000 0010
		num1 = num1 << 1;
		
		//		  0000 0000 0000 0000 0000 0000 0000 0001
		num1 = num1 >> 1;
		
		//		  0000 0000 0000 0000 0000 0000 0000 1000
		num1 = num1 << 3;
		
		
		// 비교연산자
		
		// a > b = a는 b보다 크다
		// ==, !=	
		// == : 두 값이 같다
		// != : 두 값이 다르다
		
		// 비트 연산자
		// &, |, ^
		
		//		  	1101 1001
		//		  	0100 1010 &
		// 			---------
		//			0100 1000
		

		//		  	1101 1001
		//		  	0100 1010 |
		// 			---------
		//			1101 1011	

		//		  	1101 1001
		//		  	0100 1010 ^
		// 			---------
		//			1001 0011		
		
		// 논리연산자
		int a = 1;
		int b = 10;
		int c = 5;
				
		// a < b && b < c
		// !(false && false) => false => true;
		// !(true || false) => true => false;
		
		boolean ba = true;
		boolean bb = !ba;
		// bb == false
		
		// 조건연산자 (삼항연산자)
		// 비교 ? true일때 : false일때
		(a < b) ? System.out.println("true"); : System.out.println("false");
		
		// 대입연산자 
		// = 
		
		int num3 = 10;
		num3 *= 3;
		// num3 = num3 * 3;
		
		int num4 = 10;
		num4 += 10;
		// num4 = num4 + 10;
	}

}
