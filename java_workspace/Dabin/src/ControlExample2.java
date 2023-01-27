
public class ControlExample2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		char ch = 65;
		
		int ab = 12;
		
		// 12
		// 0000 1100
		// << 2
		
		// 48
		// 0011 0000		
		
		System.out.println(ch);
		
		// -----------------------------
		
		// 10
		
		int month = 10;
		
		// -----------------------------
		
		String c = " ";
		String s;
		
		int a = 10;
		int b = 15;
		
		s = ++a >= b ? (c = " a가 크다") : (c = " b가 크다");
		System.out.println(s);
		
		s = ++a >= b ? "a" : "b";
		
	}
}
