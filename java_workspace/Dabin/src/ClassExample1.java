// class  : 파일 1개
// method : 기능 1개

/*
 * class : 자동차 1대
 * 
 * method : 자동차의 기능들
 * 
 * 전진, 후진, 좌회전, 우회전
 * 
 */

public class ClassExample1 {
	
	String age;

	// 메인 (메소드)
	
// 	접근한정자 - 다른 class에서 호출/사용할 수 있는가
	
//	public, protected, default, private
/*
 * 	public 		: 모든 곳에서 접근 가능
 * 	protected 	: 같은 패키지에 있을 경우 접근 가능, 상속 개체 포함 
 * 	default 	: 같은 패키지에 있을 경우 접근 가능, 상속 개체 미포함
 *  private 	: 같은 클래스에 있을 경우 접근 가능
 */
	
//	접근한정자	스태틱한정자	리턴값의형식	이름		매개변수  (매개변수타입	매개변수이름)
	public 	static 		void 		main(			String[] 	args	) {
		int age = 10;
		String a = test1(age);
		
		System.out.println(a);
		
	}
	
/*
 * void
 * int
 * String
 * double
 * float
 * ~~~~~~~~~~~~~~~~~~~~~
 * class
 * 
 */
	
	private static String test1(int age) {
		return "안녕" + age;
	}
	
	// 그외 메소드
	
	
}
