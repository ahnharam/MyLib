package ClassStudy;

public class Car implements CarInterface{
	@Override
	public void Front(String str) {
		System.out.println(str + " Front");
	}
	
	@Override
	public void Back(String str) {
		System.out.println(str + " Back");
	}
	
	@Override
	public void Left(String str) {
		System.out.println(str + " Left");
	}
	
	@Override
	public void Right(String str) {
		System.out.println(str + " Right2");
	}
}
