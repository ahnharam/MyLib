
public class ContinueEx2 {

	public static void main(String[] args) {
		
		label: // 레이블  설정
			for(int i = 0 ; i < 5 ; i++) {
				for(int j = 0 ; j < 5 ; j++) {
					
					if(j == 3)
					continue label;
					System.out.println("i값:"+i+",j값:"+j);
				}
			}
		// TODO Auto-generated method stub

	}

}
