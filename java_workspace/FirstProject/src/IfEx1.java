import java.util.Scanner;

public class IfEx1 {

	public static void main(String[] args) {
       int su = 0;
       System.out.println("성적을 입력해주세요 : ");
       Scanner scan = new Scanner(System.in);
       su = scan.nextInt();
       
       char str = ' ';
       
       // true
       if(su >= 90) {
    	   str = 'A';
       }
       else if(su >= 80) {
    	   str = 'B';
       }
       else if(su >= 70) {
    	   str = 'C';
       }
       else if(su >= 60) {
    	   str = 'D';
       }
       else {
    	   str = 'F';
       }
       
       System.out.println(str + "입니다");
		// TODO Auto-generated method stub

	}

}
