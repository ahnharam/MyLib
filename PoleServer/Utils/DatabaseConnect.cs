using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using PoleServerWithUI.Model;
using System.Collections.ObjectModel;

namespace PoleServerWithUI.Utils
{
    class DatabaseConnect
    {
        private MySqlConnection _conn;
        private bool _dbState = false;
        private string _dbTable = string.Empty;

        public bool ConnectDB(DatabaseModel DatabaseModel)
        {
            string connectString = 
                string.Format("Server={0};Database={1};Uid ={2};Pwd={3};CharSet=utf8;",
                DatabaseModel.ServerIp,
                DatabaseModel.Database,
                DatabaseModel.Uid,
                DatabaseModel.Pwd);

            _conn = new MySqlConnection(connectString);

            try
            {
                _conn.Open();
                _dbState = true;
                _dbTable = DatabaseModel.Database;
                return _dbState;
            }
            catch (Exception)
            {
                _dbState = false;
                return _dbState;
            }
        }

        public ObservableCollection<DeviceModel> SelectDB()
        {
            ObservableCollection<DeviceModel> deviceModels = new ObservableCollection<DeviceModel>(); 
            string sql = "Select * from device_info";

            if (_dbState)
            {
                MySqlCommand cmd = new MySqlCommand(sql, _conn);
                using (var reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        deviceModels.Add(new DeviceModel
                        {
                            No = Convert.ToInt32(reader["NO"]),
                            Screen = reader["screen"].ToString(),
                            Type = reader["Type"].ToString(),
                            Id = reader["Id"].ToString(),
                            Info = reader["Info"].ToString(),
                            Location = reader["Location"].ToString(),
                            Ip = reader["Ip"].ToString(),
                            Port = reader["Port"].ToString(),
                            Value = reader["Value"].ToString(),
                            TxData = reader["txdata"].ToString()
                        }); 
                    }
                }
                return deviceModels;
            }
            else
            {
                return null;
            }
        }

        public void InsertDB(PoleLogModel poleLogModel)
        {
            string sql = string.Format(
                "Insert Into pole_log" +
                "(no, name, screen, Type, id, bat, wireless, error, temp, humi, wind, genneration, charge, statistic, usercount, embel, cumulative_charge, cumulative_gen, netzero, info, location, value) " +
                "values " +
                "({0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}',{14},{15},{16},{17},'{18}','{19}','{20}','{21}')",
                poleLogModel.No,
                poleLogModel.Name,
                poleLogModel.Screen,
                poleLogModel.Type,
                poleLogModel.Id,
                poleLogModel.Bat,
                poleLogModel.Wireless,
                poleLogModel.Error,
                poleLogModel.Temp,
                poleLogModel.Humi,
                poleLogModel.Wind,
                poleLogModel.Genneration,
                poleLogModel.Charge,
                poleLogModel.Statistic,
                poleLogModel.UserCount,
                poleLogModel.Embel,
                poleLogModel.CumulativeCharge,
                poleLogModel.CumulativeGen,
                poleLogModel.Netzero,
                poleLogModel.Info,
                poleLogModel.Location,
                poleLogModel.Value);

            if (_dbState)
            {
                MySqlCommand cmd = new MySqlCommand(sql, _conn);
                int insertCheck = cmd.ExecuteNonQuery();

                if (insertCheck != -1)
                {
                    Console.WriteLine("Insert Complete");
                }
                else
                {
                    Console.WriteLine("Insert Error");
                }
            }
            else
            {
                Console.WriteLine("Connection Error");
            }
        }
    }
}
