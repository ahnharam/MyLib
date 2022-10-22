using static System.Console;

namespace StringSearch
{
    class MainApp
    {
        static void Main(string[] args)
        {
            string greeting = "Good Morning";

            WriteLine(greeting);
            WriteLine();

            // IndexOf()
            WriteLine("IndexOf 'Good' : {0}", greeting.IndexOf("Good"));
            WriteLine("IndexOf 'o' : {0}", greeting.IndexOf('o'));

            // LastIndexOf()
            WriteLine("LastIndexOf 'Good' : {0}", greeting.IndexOf("Good"));
            WriteLine("LastIndexOf 'o' : {0}", greeting.LastIndexOf("o"));

            // StartsWith()
            WriteLine("StratsWith 'Good' : {0}", greeting.StartsWith("Good"));
            WriteLine("StartsWith 'Morning' : {0}", greeting.StartsWith("Mirning"));

            //EndsWith()
            WriteLine("EndsWith 'Good' : {0}", greeting.EndsWith("Good"));
            WriteLine("EndsWith 'Morning' : {0}", greeting.EndsWith("Morning"));

            // Contains()
            WriteLine("Contains 'Evenig' : {0}", greeting.Contains("Exening"));
            WriteLine("Contains 'Morning' : {0}", greeting.Contains("Morning"));

            // Replace()
            WriteLine("Replaced 'Morning' with 'Evening': {0}",
                greeting.Replace("Morning", "Evening"));
        }
    }
}