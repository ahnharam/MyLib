
public class ClassExample2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		ClassExample21 c21 = new ClassExample21();
		c21.SetAge(10);
		System.out.println("하라미 나이 : " + c21.GetAge());
		
//		c21.SetDataToInt(10);
//		c21.SetDataToString("String");
		
		c21.SetData(10);
		c21.SetData("String");
	}
}
