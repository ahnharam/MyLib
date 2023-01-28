using System;

namespace WithExp
{
    record RTransaction
    {
        public string From { get; set; }
        public string To { get; set; }
        public int Amount { get; set; }

        public override string ToString()
        {
            return $"{From,-10} -> {To,-10} : ${Amount}";
        }
    }

    class MainApp
    {
        static void Main(string[] args)
        {
            RTransaction tr1 = new RTransaction
            {
                From = "Alice",
                To = "Bob",
                Amount = 100
            };
            RTransaction tr2 = tr1 with
            {
                To = "Charlie"
            };
            RTransaction tr3 = tr2 with
            {
                From = "Dave",
                Amount = 30
            };

            Console.WriteLine(tr1);
            Console.WriteLine(tr2);
            Console.WriteLine(tr3);
        }
    }
}