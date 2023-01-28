using System;

namespace AccessModifier
{
    class WaterHeater
    {
        protected int temperature;

        public void SetTemperature(int temperature)
        {
            if (temperature < -5 || temperature > 42)
            {
                throw new Exception("Out of temperature range");
            }

            this.temperature = temperature;
        }

        internal void TurnOnwater()
        {
            Console.WriteLine($"Turn on water : {temperature}");
        }
    }

    class MainApp
    {
        static void Main(string[] args)
        {
            try
            {
                WaterHeater heater = new WaterHeater();
                heater.SetTemperature(20);
                heater.TurnOnwater();

                heater.SetTemperature(-2);
                heater.TurnOnwater();

                heater.SetTemperature(50);
                heater.TurnOnwater();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }
}