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



// 접근한정자		class		이름(클래스 헤더)
public 			class 		ClassExample1 {
	
	// 멤버필드 or 전역변수
	// 상수 / 메모리 고정
	public static final int num = 10;
	
	// 변수
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
		
		// 지역변수 / 멤버변수
		int age = 10;
		

		System.out.println(ClassExample1.num);
		
		// 클래스 타입		이름			 새로만든다	ClassExample1 이 친구로
		// 인스턴스화 
		ClassExample1 	c1 		=	 new 		ClassExample1();
		
		// c1 - 인스턴스
		
		c1.age = "hello";

		String a = c1.test1(10);
		
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
	
	// 멤버메소드  
	// 한정자		반환자 타입	이름		파라미터
	private 	String 		test1	(int age) {
		return "안녕" + age;
	}
	  
	// 한정자		반환자 타입	이름		파라미터
	private 	int 		test2	(int age) {
		return age;
	}
}
