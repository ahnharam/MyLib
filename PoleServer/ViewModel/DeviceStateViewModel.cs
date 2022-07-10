using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using PoleServerWithUI.Model;
using System.Collections.ObjectModel;
using Prism.Mvvm;
using PoleServerWithUI.Utils;
using Prism.Commands;

namespace PoleServerWithUI.ViewModel
{
    class DeviceStateViewModel : BindableBase
    {
        private GateWayConnect _gateWayConnect;
        private DatabaseConnect _databaseConnect;

        private DatabaseModel databaseModel;
        public DatabaseModel DatabaseModel
        {
            get { return databaseModel; }
            set { SetProperty(ref databaseModel, value); }
        }

        private ObservableCollection<DeviceModel> devices;
        public ObservableCollection<DeviceModel> Devices
        {
            get { return devices; }
            set { SetProperty(ref devices, value); }
        }

        private ObservableCollection<DeviceStateModel> deviceStateModels;
        public ObservableCollection<DeviceStateModel> DeviceStateModels
        {
            get { return deviceStateModels; }
            set { SetProperty(ref deviceStateModels, value); }
        }

        public DeviceStateViewModel()
        {
            DatabaseModel = new DatabaseModel();

            //DatabaseModel.ServerIp = "192.168.50.2";
            //DatabaseModel.Database = "smart_pole";
            //DatabaseModel.Uid = "root";
            //DatabaseModel.Pwd = "solnetworks12!@";

            DatabaseModel.ServerIp = "175.193.137.114";
            DatabaseModel.Database = "smart_pole";
            DatabaseModel.Uid = "root";
            DatabaseModel.Pwd = "root";

            _gateWayConnect = new GateWayConnect();
            _databaseConnect = new DatabaseConnect();
        }

        private DelegateCommand<object> databaseConnectButton;
        public DelegateCommand<object> DatabaseConnectButton
        {
            get
            {
                if (databaseConnectButton == null)
                    databaseConnectButton = new DelegateCommand<object>(DatabaseConnect);
                return databaseConnectButton;
            }
        }

        private void DatabaseConnect(object obj)
        {
            if(DatabaseModel.ServerIp == null
                || DatabaseModel.Database == null
                || DatabaseModel.Uid == null
                || DatabaseModel.Pwd == null)
            {

                LogMessage.Instance.Log.Add("DB 데이터 입력 필요");
                return;
            }

            bool dbState = _databaseConnect.ConnectDB(DatabaseModel);


            LogMessage.Instance.Log.Add("DB connect : " + dbState);
            Devices = _databaseConnect.SelectDB();

            if (Devices == null)
            {

                LogMessage.Instance.Log.Add("Device is Empty");
                return;
            }
            
            LogMessage.Instance.Log .Add("Device Count : " + Devices.Count);
        }

        private DelegateCommand<object> gatewayConnectButton;
        public DelegateCommand<object> GatewayConnectButton
        {
            get
            {
                if (gatewayConnectButton == null)
                    gatewayConnectButton = new DelegateCommand<object>(GatewayConnect);
                return gatewayConnectButton;
            }
        }

        private void GatewayConnect(object obj)
        {
            _gateWayConnect.GatewayConnect(Devices);
        }

        private DelegateCommand<object> gatewaySendDataButton;
        public DelegateCommand<object> GatewaySendDataButton
        {
            get
            {
                if (gatewaySendDataButton == null)
                    gatewaySendDataButton = new DelegateCommand<object>(GatewaySendData);
                return gatewaySendDataButton;
            }
        }

        private void GatewaySendData(object obj)
        {
            _gateWayConnect.DataPolling(Devices);

            Task.Run(async () =>
            {
                await Task.Delay(10000);
                                
                if(_gateWayConnect._poleLogData.Count != 0)
                {
                    DispatcherService.Invoke((System.Action)(() =>
                    {
                        LogMessage.Instance.Log.Add("Data Count : " + _gateWayConnect._poleLogData.Count);
                    }));
                }

                while(_gateWayConnect._poleLogData.Count != 0)
                {
                    _databaseConnect.InsertDB(_gateWayConnect._poleLogData.Dequeue());
                }
            });
        }

        public void UnLoaded()
        {
            _gateWayConnect.GatewayDisConnect();
        }
    }
}
