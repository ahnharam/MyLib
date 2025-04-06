
public class ContinueEx1 {

	public static void main(String[] args) {
		
		for(int i = 0 ; i < 10 ; i++) {
			if(i%4 == 0) {// 4의 배수
				// continue를 만나면 해당 for문의 증감식으로 넘어간다.
				// (만약 for문에 증감식이 없다면 조건식으로 넘어간다.)
				continue;
			}
			System.out.println("i값:"+i);
		}
		// TODO Auto-generated method stub

	}

}
