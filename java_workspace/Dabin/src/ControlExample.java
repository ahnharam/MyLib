import java.util.Scanner;

public class ControlExample {

	public static void main(String[] args) {		
		
		// if
		// else if
		// else
		int su = 0;
		System.out.println("성적을 입력해주세요 : ");
		Scanner scan = new Scanner(System.in);
		su = scan.nextInt();
		
		char str = ' ';
		
		// true
		if(su >= 90) {
			str = 'A';
		}
		else if(su >= 80){
			str = 'B';
		}
		else if(su >= 70){
			str = 'C';
		}
		else if(su >= 60){
			str = 'D';
		}
		else {
			str = 'F';
		}
		
		System.out.println(str + "입니다.");
		
		// switch
		// case
		// break
		// default
		
		switch (str) {
			case 'A': 
				System.out.println("이 학생은 천재입니다.");
				break;
			case 'B': 
				System.out.println("이 학생은 영재입니다.");
				break;		
			default:
				System.out.println("이 학생은 평범합니다.");
				break;		
		}
	}
}
