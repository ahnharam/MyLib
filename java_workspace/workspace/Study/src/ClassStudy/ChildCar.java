package ClassStudy;

import java.util.Scanner;

public class ChildCar extends Car{

	public void Front() {
		System.out.print("Speed Input : ");
		Scanner s = new Scanner(System.in);
		String speed = s.nextLine();
		
		System.out.println("Front Speed : " + speed);
	}
	
	public int Back2(int num) {
		
		return num+num;
	}
}
