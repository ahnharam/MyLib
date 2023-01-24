// haramProject			카멜케이스		- 현재방식 - 자바
// HaramProject			파스칼케이스	- 현재방식 - 자바
// haram_project		스네이크케이스 - 옛날방식 - C언어
// haram-project		케밥케이스		- 현재방식 - 잘안씀
// hProject				헝가리안케이스 - 옛날방식 - 잘안씀
// getter setter
// get / set			- 직관적으로 알수 있는 경우

public class Ex1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Hello world");
		
		// 논리형
		// 형식  이름    값(데이터)
		boolean bool1 = false; 
		boolean bool2 = true;
		
		// 문자형
		// 형식 	이름  	값(데이터)
		// 문자
		   char	char1 = 'a';
		// 문자열
		   String str = "문자열";
			
		// 정수형
//		   	+	64	32	16	8	4	2	1
//		   	0	0	0	0	0	0	1	0 = 2
//		   					
//		   	-	64	32	16	8	4	2	1
// 1byte 	1	0	0	0 	0	0	0	0 = -1
		   		
		//   byte : -128 ~ 127  		0+
		   					
		   					
//			1GB
//			1000MB
//			1000000KB
//			1,000,000,000B
			
		//  2byte 0000 0000 0000 0000		   							   				
		//   short : 
		   					
		//	4byte 0000 0000 0000 0000 0000 0000 0000 0000
		//   int  - default  // -21억~ +21억
			
		//	8byte 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
		//   long	- int로 데이터를 담을 수 없을 때
		//  windows 8bit == 1byte 
		// 현재 - 64 => 8byte
			//   32 -> 4byte
		//  c언어 -> int == long -> 4byte
		// 
		   
		
		// 실수형
//		float 	- 4byte
//		double	- 8byte
		
// 		float float1 = 0.10f;
//		형식		이름 	데이터
//		고정		자기맘	자기맘
	   double double1 = 0.1;
	   double st1 = 0.2;
	}
}
