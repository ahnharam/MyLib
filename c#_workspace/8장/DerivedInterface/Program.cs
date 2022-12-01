using System;

namespace DerivedInterface
{
    interface ILogger
    {
        void WriteLog(string message);
    }

    interface IformattableLogger : ILogger
    {
        void WriteLog(string format, params object[] args);
    }

    class ConcoleLogger2 : IformattableLogger
    {
        public void WriteLog(string message)
        {
            Console.WriteLine("{0} {1}," +
                DateTime.Now.ToLocalTime(), message);
        }

        public void WriteLog(string format, params Object[] args)
        {
            String message = String.Format(format, args);
            Console.WriteLine("{0} {1}",
                DateTime.Now.ToLocalTime(), message);
        }
    }

    class MainApp
    {
        static void Main(string[] args)
        {
            IformattableLogger logger = new ConcoleLogger2();
            logger.WriteLog("The world is mot flat.");
            logger.WriteLog("{0} + {1} = {2}", 1, 1, 2);
        }
    }
}