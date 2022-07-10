using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Prism.Mvvm;

namespace PoleServerWithUI.Model
{
    class DatabaseModel : BindableBase
    {
        private string serverIp;
        public string ServerIp
        {
            get { return serverIp; }
            set { SetProperty(ref serverIp, value); }
        }

        private string database;
        public string Database
        {
            get { return database; }
            set { SetProperty(ref database, value); }
        }

        private string uid;
        public string Uid
        {
            get { return uid; }
            set { SetProperty(ref uid, value); }
        }

        private string pwd;
        public string Pwd
        {
            get { return pwd; }
            set { SetProperty(ref pwd, value); }
        }
    }
}
