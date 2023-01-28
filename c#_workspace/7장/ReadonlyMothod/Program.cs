using System;

namespace ReadonluMethod
{
    struct ACSetting
    {
        public double currentInCelsius; // 현재 온도 (°C)
        public double target; // 희망 온도

        public readonly double GetFahrenheit()
        {           // 화씨 (°F) 계상 결과를 target에 저장
            target = currentInCelsius * 1.8 + 32;
            return target; // target 반환
        }
    }

    class MainApp
    {
        static void Main(string[] args)
        {
            ACSetting acs;
            acs.currentInCelsius = 25;
            acs.target = 25;

            Console.WriteLine($"{acs.GetFahrenheit()}");
            Console.WriteLine($"{acs.target}");
        }
    }
}