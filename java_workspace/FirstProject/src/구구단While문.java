
public class 구구단While문 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		int i = 0;
		while(i++ < 9) {
			int j = 1;
			while(j++ < 9) {
				System.out.print(j+"*"+i+"="+j*i+"\t");
			}
			System.out.println();
		}
	}

}
