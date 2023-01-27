
public class WhileExample2 {

	public static void main(String[] args) {
		int a = 0;
				
		// 무한 루프
		while (a < 10) {
			a++;
			
			if(a == 5) continue;
			
			System.out.println("a : " + a);
			
		}
		
	}

}
