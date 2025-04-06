
public class ClassExample21{
	// 은닉화
	private int age = 0;
	
	private int data1 = 0;
	private String data2 = "";
	
	public int GetAge() {
		return this.age;
	}
	
	public void SetAge(int age) {
		this.age = age;
	}
	
	// 메소드 오버로딩
	// method overload
	
	public void SetDataToInt(int data) {
		this.data1 = data;
	}
	
	public void SetDataToString(String data) {
		this.data2 = data;
	}
	
	public void SetData(int data) {
		this.data1 = data;
	}
	
	public void SetData(String data) {
		this.data2 = data;
	}
}