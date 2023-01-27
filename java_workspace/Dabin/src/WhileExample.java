
public class WhileExample {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// 반복문
		
		// for
		// 초기문, 조건문, 증감문
		
		
		// 조건문 true 일 때만 실행
		// while
		
		int a = 0;
		
		while(a < 10) {
			System.out.println("a : " + a);
			a++;
		}
		
		// do ~ while
		// 한번은 무조건 실행을 해라
		// 조건문 true 일 때 실행
		
		int b = 0;
		
		do {
			System.out.println("b : " + b);
			b++;
		} while(b < 10);
	}

}
