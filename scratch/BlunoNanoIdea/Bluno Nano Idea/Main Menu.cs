// This program just shows an idea of a GUI and some data received handlers to program the robots
// Since all Bluno Nano data comes through "COM" serial ports, any programming language with a serial communication framework can be used.
using System;
using System.Windows.Forms;

namespace Bluno_Nano_Idea
{
    public partial class MainMenu : Form
    {
        public MainMenu()
        {
            InitializeComponent();
        }

        #region Data Received Handlers
        private void RobotSerial1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            // Do stuff if the BLE link receives data
        }

        private void RobotSerial2_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            // Do stuff if the BLE link receives data
        }

        private void RobotSerial3_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            // Do stuff if the BLE link receives data
        }

        private void RobotSerial4_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            // Do stuff if the BLE link receives data
        }

        private void RobotSerial5_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            // Do stuff if the BLE link receives data
        }
        #endregion

        private void btn_Start_Click(object sender, EventArgs e)
        {
            try
            {
                initialize_robots();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                if (RobotSerial1.IsOpen) RobotSerial1.Close();
                if (RobotSerial2.IsOpen) RobotSerial2.Close();
                if (RobotSerial3.IsOpen) RobotSerial3.Close();
                if (RobotSerial4.IsOpen) RobotSerial4.Close();
                if (RobotSerial5.IsOpen) RobotSerial5.Close();
            }
        }

        private void initialize_robots()
        {
            // Port names, baud rates, and open the ports.
            RobotSerial1.PortName = txt_Robot1COM.Text;
            RobotSerial2.PortName = txt_Robot2COM.Text;
            RobotSerial3.PortName = txt_Robot3COM.Text;
            RobotSerial4.PortName = txt_Robot4COM.Text;
            RobotSerial5.PortName = txt_Robot5COM.Text;

            RobotSerial1.BaudRate = int.Parse(txt_Robot1Baud.Text);
            RobotSerial2.BaudRate = int.Parse(txt_Robot2Baud.Text);
            RobotSerial3.BaudRate = int.Parse(txt_Robot3Baud.Text);
            RobotSerial4.BaudRate = int.Parse(txt_Robot4Baud.Text);
            RobotSerial5.BaudRate = int.Parse(txt_Robot5Baud.Text);

            if (!RobotSerial1.IsOpen) RobotSerial1.Open();
            if (!RobotSerial2.IsOpen) RobotSerial2.Open();
            if (!RobotSerial3.IsOpen) RobotSerial3.Open();
            if (!RobotSerial4.IsOpen) RobotSerial4.Open();
            if (!RobotSerial5.IsOpen) RobotSerial5.Open();
        }
    }
}
