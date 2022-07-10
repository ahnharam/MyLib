using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Prism.Mvvm;

namespace PoleServerWithUI.Model
{
    class DeviceModel : BindableBase
    {
        public int No { get; set; }
        public string Screen { get; set; }
        public string Type { get; set; }
        public string Id { get; set; }
        public string Info { get; set; }
        public string Location { get; set; }

        private string ip;
        public string Ip
        {
            get { return ip; }
            set { SetProperty(ref ip, value); }
        }

        public string Port { get; set; }
        public string Value { get; set; }

        public string TxData { get; set; }

        private bool connected;
        public bool Connected
        {
            get { return connected; }
            set { SetProperty(ref connected, value); }
        }
    }
}
