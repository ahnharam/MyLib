package ClassStudy;

public class MyCalc {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Calc myCalc = new Calc();
		long test10 = 10L;
	    long resultAdd = myCalc.add(test10, 40L);
	    
	    Data testData = new Data();
	    System.out.println("result data 1: " + testData.data1);
	    System.out.println("result data 2: " + testData.data2);
	    System.out.println("result data 3: " + testData.data3);
	    System.out.println("result data 4: " + testData.data4);
	    
	    myCalc.resultData(testData);
	    System.out.println("result data 1: " + testData.data1);
	    System.out.println("result data 2: " + testData.data2);
	    System.out.println("result data 3: " + testData.data3);
	    System.out.println("result data 4: " + testData.data4);
	    
	    System.out.println("result : " + resultAdd);

	}

}
