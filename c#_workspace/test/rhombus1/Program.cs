using System;

namespace rhombus1
{
    class MainApp
    {
        static void Main(string[] args)
        {
            Console.WriteLine("숫자 입력 : ");
            int num =int.Parse(Console.ReadLine());
            for (int i = 0; i < num; i++)
            {
                for (int j = num; j > i; j--)
                {
                    Console.Write(" ");
                }
                for (int j = 0; j <= i * 2 ; j++)
                {
                    Console.Write("*");
                }
                Console.WriteLine();
            }
            for (int i = num-2; i >= 0; i--)
            {
                for (int j = num; j > i; j--)
                {
                    Console.Write(" ");
                }
                for (int j = 0; j < i * 2 + 1; j++)
                {
                    Console.Write("*");
                }
                Console.WriteLine();
            }
        }
    }
}



