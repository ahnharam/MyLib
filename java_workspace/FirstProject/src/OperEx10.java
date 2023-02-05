
public class OperEx10 {

	public static void main(String[] args) {
		int a = 10;
		int b = 15;
		String c = " ";
		String s;
		
		// 오류 유도
		//s = ++a >= b ? c = " a가 크다" : c = " b가 크다";
		
		s = ++a >= b ? (c = " a가 크다") : (c = " b가 크다");
		System.out.println(s);
		// TODO Auto-generated method stub

	}

}
