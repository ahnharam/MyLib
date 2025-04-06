import java.util.Scanner;

public class 반복문연습문제1 {

	public static void main(String[] args) {
		
		Scanner scan = new Scanner(System.in);
		int age = scan.nextInt();
		String res;
		
		if(0<= age && age < 10)
			res = "10대 미만";
		
		else if(10<= age && age < 20)
			res = "10대";
		
		else if(20<= age && age < 30)
			res = "20대";
		
		else if(30<= age && age < 40)
			res = "30대";
		
		else if(40<= age && age < 50)
			res = "40대";
		
		else if(50<= age && age < 60)
			res = "50대";
		
		else if(60<= age && age < 70)
			res = "60대";
		
		else
			res = "60대 이상";
		
		System.out.println(res);
		
		// TODO Auto-generated method stub

	}

}
