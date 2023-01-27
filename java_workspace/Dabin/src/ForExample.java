
public class ForExample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// 반복문
		
		/*
		 * For - for, foreach
		 * 
		 * While - while, do~while
		 */
		
		// 초기문,	조건문,		증감문
		
		// ++
		// i = i + 1;
		
		// 계속 반복되는 현상 -> 무한 루프
		
		/*
		 * i : 0
		 * j : 0
		 * 
		 * i : 1
		 * j : 1
		 * 
		 */
		
				
		for(int i = 0; i < 5 ; i++) {
			System.out.print("i : ");
		 	System.out.print(i);
		 	System.out.println("번째 수행");
		 	// i : 0	
		 	
		 			
		 	// 반복		조건문이 false가 되면 종료
		 	// 반복 - 5회
		 	// 무한 루프
		 	for(int j = 0; j < 5 ; j++) {
		 		// j : 0
		 		// j : 1
		 		// j : 2
		 		// j : 3
		 		// j : 4
			 	System.out.print("j : ");
			 	System.out.print(j);
			 	System.out.println("번째 수행");
			 	
			 	break;
			 	// 끝
			} // j++
		 	
		 	System.out.println("끝");
		 	// 끝
		}
		
	}

}
