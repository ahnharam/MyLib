using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Modbus.Device;
using System.IO.Ports;
using System.Net.Sockets;
using PoleServerWithUI.Model;
using System.Collections.ObjectModel;
using System.Net;

namespace PoleServerWithUI.Utils
{
    class GateWayConnect
    {
        List<TcpClient> _tcpClients;
        TcpListener _server;
        Queue<bool> _gatewayData = new Queue<bool>();
        public Queue<PoleLogModel> _poleLogData = new Queue<PoleLogModel>();

        // Gateway 연결
        public async void GatewayConnect(ObservableCollection<DeviceModel> deviceModels)
        {
            _tcpClients = new List<TcpClient>();
            const int bindPort = 502;
            _server = null;
            try
            {
                _server = new TcpListener(IPAddress.Any, bindPort);

                _server.Start();


               LogMessage.Instance.Log.Add("서버 시작...");

                await Task.Run(() =>
                {
                    while (true)
                    {
                        TcpClient client = _server.AcceptTcpClient();
                        DispatcherService.Invoke((System.Action)(() =>
                        {
                            LogMessage.Instance.Log.Add(String.Format("클라이언트 접속: {0} ", ((IPEndPoint)client.Client.RemoteEndPoint).Address.ToString()));
                        }));
                            _tcpClients.Add(client);

                        DeviceModel data = null;
                        foreach(var device in deviceModels)
                        {
                            if (device.Ip.Equals(((IPEndPoint)client.Client.RemoteEndPoint).Address.ToString()))
                            {
                                device.Connected = true;
                                data = device;
                                DispatcherService.Invoke((System.Action)(() =>
                                {
                                    LogMessage.Instance.Log.Add(String.Format("클라이언트 IP : {0}, Connection : {1}", data.Ip, data.Connected));
                                }));
                            }
                        }

                        Task.Delay(100);
                    }
                });
            }
            catch (SocketException e)
            {
                Console.WriteLine(e);
            }

        }

        public async void DataPolling(ObservableCollection<DeviceModel> deviceModels)
        {
            await Task.Run( async () =>
            {
                while (true)
                {
                    try
                    {
                        foreach (var client in _tcpClients)
                        {
                            //string sendData = string.Empty;
                            //DeviceModel dataModel;
                            foreach (var device in deviceModels)
                            {
                                if (device.Ip.Equals(((IPEndPoint)client.Client.RemoteEndPoint).Address.ToString()))
                                {
                                    DataLoad(device.TxData, device, client);
                                }
                                else
                                {
                                    continue;
                                }
                            }
                        }
                    }
                    catch (Exception e)
                    {
                        DispatcherService.Invoke((System.Action)(() =>
                        {
                            LogMessage.Instance.Log.Add("Data Read Error : " + e);
                        }));
                    }

                    await Task.Delay(10000);
                }
            });
        }


        // Gateway 를 통한 데이터 로드
        public async void DataLoad(string sendData, DeviceModel device, TcpClient client)
        {
            await Task.Run(() => 
            {
                try
                {
                    DeviceModel dataModel;
                    if (device.Ip.Equals(((IPEndPoint)client.Client.RemoteEndPoint).Address.ToString()))
                    {
                        dataModel = device;
                        sendData = device.TxData;
                    }
                    else
                    {
                        return;
                    }

                    if (string.IsNullOrEmpty(sendData))
                        return;

                    NetworkStream stream = client.GetStream();

                    byte[] msg = Encoding.Default.GetBytes(sendData);
                    stream.Write(msg, 0, msg.Length);
                    DispatcherService.Invoke((System.Action)(() =>
                    {
                        LogMessage.Instance.Log.Add(String.Format("송신: {0}", sendData));
                    }));

                    byte[] datas = new byte[256];

                    stream.ReadTimeout = 10000;
                    string responseData = "";

                    var Result = stream.Read(datas, 0, datas.Length);

                    responseData = Encoding.Default.GetString(datas, 0, Result);
                    DispatcherService.Invoke((System.Action)(() =>
                    {
                        LogMessage.Instance.Log.Add(String.Format("수신 : {0}", responseData));
                    }));

                    DataSave(responseData);
                    _gatewayData.Enqueue(true);
                }
                catch (Exception e) 
                {
                    device.Connected = false;
                    DispatcherService.Invoke((System.Action)(() =>
                    {
                        LogMessage.Instance.Log.Add(String.Format("Data Error : {0}", e));
                    }));
                    _gatewayData.Enqueue(false);
                }
            });
        }

        public PoleLogModel DataSave(string responseData)
        {
            PoleLogModel poleLogModel = new PoleLogModel();

            string[] datas = responseData.Split(' ');
            DispatcherService.Invoke((System.Action)(() =>
            {
                LogMessage.Instance.Log.Add(String.Format("Data Length : {0}", datas.Length));
            }));

            if (datas.Length == 25)
            {
                poleLogModel.Id = Convert.ToInt32(datas[0], 16).ToString();
                poleLogModel.Name = Convert.ToInt32(datas[3], 16).ToString();
                poleLogModel.Screen = Convert.ToInt32(datas[4], 16).ToString();
                poleLogModel.Type = Convert.ToInt32(datas[5], 16).ToString();
                poleLogModel.Id = Convert.ToInt32(datas[6], 16).ToString();
                poleLogModel.Bat = Convert.ToInt32(datas[7], 16).ToString();
                poleLogModel.Wireless = Convert.ToInt32(datas[8], 16).ToString();
                poleLogModel.Error = Convert.ToInt32(datas[9], 16).ToString();
                poleLogModel.Temp = Convert.ToInt32(datas[10], 16).ToString();
                poleLogModel.Humi = Convert.ToInt32(datas[11], 16).ToString();
                poleLogModel.Wind = Convert.ToInt32(datas[12], 16).ToString();
                poleLogModel.Genneration = Convert.ToInt32(datas[13], 16).ToString();
                poleLogModel.Charge = Convert.ToInt32(datas[14], 16).ToString();
                poleLogModel.Statistic = Convert.ToInt32(datas[15], 16).ToString();
                poleLogModel.UserCount = Convert.ToInt32(datas[16], 16);
                poleLogModel.Embel = Convert.ToInt32(datas[17], 16);
                poleLogModel.CumulativeCharge = Convert.ToInt32(datas[18], 16);
                poleLogModel.CumulativeGen = Convert.ToInt32(datas[19], 16);
                poleLogModel.Netzero = Convert.ToInt32(datas[20], 16).ToString();
                poleLogModel.Info = Convert.ToInt32(datas[21], 16).ToString();
                poleLogModel.Location = Convert.ToInt32(datas[22], 16).ToString();
                poleLogModel.Value = Convert.ToInt32(datas[23], 16).ToString();
                
                _poleLogData.Enqueue(poleLogModel);
            }

            //DispatcherService.Invoke((System.Action)(() =>
            //{
            //    foreach(var data in datas)
            //    {
            //        LogMessage.Instance.Log.Add(String.Format("Split Data : {0}", data));
            //    }
            //}));

            return poleLogModel;
        }

        public bool GatewayDisConnect()
        {
            foreach(var tcp in _tcpClients)
            {
                tcp.Close();
            }
            return true;
        }
    }
}
