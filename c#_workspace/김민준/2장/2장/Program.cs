namespace Chapter2{
    public class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World");
        }
    }
}


// 정수
// -1,2,3,4,5

// ulong         - 8byte/4byte           - C언어  : 4byte
//                                      - C++, C#: 8byte
// int          - 4byte                 : 2^16  = 42억   -21 ~ +21   0 <- 조금 이따가
// uint                         0~42억
// 절대값

// unsigned short        - 2byte
// byte         - 1byte    = 8bit       0~255
// sbyte                          -128 ~ 127

/*
 *      0 <-  0 0
 *      1 <- -1 1
 *      
 *      0000
 *      0001
 *      0010
 *      0011
 *      0100
 *      1111 1111 = 255
 *      컴퓨터는 부호개념이 없어
 *      
 *      첫번째자리를 부호표시로 생각한다
 *      0111 1111 = 127 양수
 *      1               음수
 */


/*
 * 컴파일러 <- 자연어를 기계어로 바꿔
 * 어셈블리어 - 거의 기계어
 * 
 * 0101001110101010 기계어
 */



// 실수
// -1.1, 1.2,   112312312312312.312312312312312313123
//              1.1213e24
/*
 * double       : 8byte
 * float        : 4byte
 * 
 * 정수부, 지수부
 * 
 */

// 문자
// a, b, c, 안, 하, 람
// char         : 2byte         <- ㅇㅅㅋ코드

// 문자열
// 안하람
// 스트링
// string       : 없어요

// 논리
// 참, 거짓
// bool

// object   <- 정수                  - 타입을 안적은 포장
// var      <- 오브젝트랑 비슷한데   - 타입을 적어놓은 포장

var b = 1.1; // 컴퓨터가 유추를 해        - 

int c = 1;              // 정수
double dd = 1.1;        // 정수 + 지수
string s = "1";
char c2 = '1';

object e = (object)1;
int f = (int)e;

// 상수 : 변하지 않는 수
const int g = 10;

// 열거 : 죽 들어서 말하는 것.    'a' 'b' 'c' 'd'
enum Enum1{ YES = 101, NO, OTHER }       //  <- 코드의 가독성 읽기 쉽게

// empty <- 비슷한 단어 
// NULL
// 내용이 없다

int? aa = null;
string bb = null;


// 저장되는 방식이 값 형식, 참조 형식

/*
 * int, char, double        직접적으로 데이터를 저장한다
 * 
 * string, object, var      간접적으로 데이터를 저장한다
 * 
 * 3장에 있는 예제를 전부 타이핑해
 * 연습문제도 풀어
 */