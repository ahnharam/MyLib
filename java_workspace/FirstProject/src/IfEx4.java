import java.util.Scanner;

public class IfEx4 {

	public static void main(String[] args) {
		
		System.out.println("과일명 : ");
		Scanner scan = new Scanner(System.in);
		String fruit = scan.next();
		String res;
		// String 객체 내용을 비교할 때는 equals() 메서드를 사용한다.
		if(fruit.equals("grape"))
			res = "달다.";
		else if(fruit.equals("watermelon"))
			res = "시원하다.";
		else if(fruit.equals("strawberry"))
			res = "맛있다.";
		else
			res = "기타";
		System.out.println(res);
		// TODO Auto-generated method stub

	}

}
