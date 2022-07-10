using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PoleServerWithUI.Model
{
    class PoleLogModel
    {
        public int No { get; set; }
        public string Name { get; set; }
        public string Screen { get; set; }
        public string Type { get; set; }
        public string Id { get; set; }
        public string Bat { get; set; }
        public string Wireless { get; set; }
        public string Error { get; set; }
        public string Temp { get; set; }
        public string Humi { get; set; }
        public string Wind { get; set; }
        public string Genneration { get; set; }
        public string Charge { get; set; }
        public string Statistic { get; set; }
        public int UserCount { get; set; }
        public int Embel { get; set; }
        public int CumulativeCharge { get; set; }
        public int CumulativeGen { get; set; }
        public string Netzero { get; set; }
        public string Info { get; set; }
        public string Location { get; set; }
        public string Value { get; set; }
    }
}
