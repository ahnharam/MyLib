package ClassStudy;

import java.util.Scanner;

public class ClassTest1 {

	public static void main(String[] args) {
		Car k7 = new Car();
		Car k9 = new Car();
		
		ChildCar k5 = new ChildCar(); 
		
		
		boolean check;
		
		do {			
			System.out.print("Car Name :");
			Scanner s = new Scanner(System.in);
			String input = s.nextLine();
			
			if(input.equals("k7")) {
				k7.Front("k7");
				k7.Back("k7");
				k7.Left("k7");
				check = true;
			}
			else if(input.equals("k9")) {
				k9.Front("k9");
				k9.Back("k9");
				k9.Left("k9");
				check = true;
			}
			else if(input.equals("k5")) {
				k5.Front();
				k5.Front("k5");
				
				int a = k5.Back2(10);
				
				System.out.println("a : " + a);
				
				check = true;
			}
			else {
				System.out.println("input error");
				check = false;
			}
		}while(check == false);
		
	}

}
