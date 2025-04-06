class Human {
    public void info() {
        System.out.println("나는 사람입니다.");
    }
    // Method A
    // Method B
    // Method C
    // Method D    
}

// 캐릭터 제작자 	- 개발자 
// 도화가, 아르카나 기능은 같고, 하는 행동만 달라

// 스토리라인 		- 기획자
// 스토리에서 ~~   기능을 사용한다 - 행동을 뭐하는지는 몰라

class Female extends Human {
    public void info() {
        System.out.println("나는 여자입니다.");
    }
}

class Male extends Human {
    public void info() {
        System.out.println("나는 남자입니다.");
    }
}

public class ClassTest2 {
    public static void main(String[] args) {
        // 객체 타입과 참조변수 타입이 일치
        Human human = new Human();
        Human female = new Female();
        // 객체 타입과 참조변수 타입이 불일치
        Human male = new Male();

        human.info();		//	나는 사람입니다.
        female.info();		//	나는 여자입니다.
        male.info();		//	나는 남자입니다.
    }
}