using System;

namespace MethodHiding
{
    class Base
    {
        public void MyMethod()
        {
            Console.WriteLine("Base.MyMethod()");
        }
    }

    class Derived : Base
    {
        public new void MyMothod()
        {
            Console.WriteLine("Derived.MyMethod()");
        }
    }

    class MainApp
    {
        static void Main(string[] args)
        {
            Base baseObj=new Base();
            baseObj.MyMethod();

            Derived derivedObj=new Derived();
            derivedObj.MyMothod();

            Base baseOrDerived = new Derived();
            baseOrDerived.MyMethod();
        }
    }
}