using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Threading;

namespace PoleServerWithUI.Utils
{
    class LogMessage : BindableBase
    {
        // Property
        private static LogMessage _instance { get; set; }
        public static LogMessage Instance
        {
            get
            {
                return _instance ?? (_instance = new LogMessage());
            }
        }

        private ObservableCollection<string> log = new ObservableCollection<string>();
        public ObservableCollection<string> Log
        {
            get { return log; }
            set { SetProperty(ref log, value); }
        }
    }
    public static class DispatcherService
    {
        public static void Invoke(Action action)
        {
            Dispatcher dispatchObject = Application.Current != null ? Application.Current.Dispatcher : null;
            if (dispatchObject == null || dispatchObject.CheckAccess())
                action();
            else
                dispatchObject.Invoke(action);
        }
    }


}
