
public class 반복문연습문제3 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		System.out.println("----------Java Run----------");
		
		for(int i = 1 ; i <= 9 ; i++) {
			
			for(int j = 2 ; j <= 9 ; j++) {
				
				// \t : tab
				// \n : 줄바꿈
				// \0 : 끝맺음
				
				System.out.print(j + "*" + i + "=" + j * i + "\t");
			}
			
			System.out.println();
		}
		
		// while문으로 변경 / 숙제
		
	}
}

