namespace Bluno_Nano_Idea
{
    partial class MainMenu
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.txt_Robot1COM = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.txt_Robot2COM = new System.Windows.Forms.TextBox();
            this.txt_Robot3COM = new System.Windows.Forms.TextBox();
            this.txt_Robot4COM = new System.Windows.Forms.TextBox();
            this.txt_Robot5COM = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.btn_Start = new System.Windows.Forms.Button();
            this.RobotSerial1 = new System.IO.Ports.SerialPort(this.components);
            this.RobotSerial2 = new System.IO.Ports.SerialPort(this.components);
            this.RobotSerial3 = new System.IO.Ports.SerialPort(this.components);
            this.RobotSerial4 = new System.IO.Ports.SerialPort(this.components);
            this.RobotSerial5 = new System.IO.Ports.SerialPort(this.components);
            this.label7 = new System.Windows.Forms.Label();
            this.txt_Robot5Baud = new System.Windows.Forms.TextBox();
            this.txt_Robot4Baud = new System.Windows.Forms.TextBox();
            this.txt_Robot3Baud = new System.Windows.Forms.TextBox();
            this.txt_Robot2Baud = new System.Windows.Forms.TextBox();
            this.txt_Robot1Baud = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // txt_Robot1COM
            // 
            this.txt_Robot1COM.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot1COM.Location = new System.Drawing.Point(117, 36);
            this.txt_Robot1COM.Name = "txt_Robot1COM";
            this.txt_Robot1COM.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot1COM.TabIndex = 0;
            this.txt_Robot1COM.Text = "COM1";
            // 
            // label1
            // 
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(12, 39);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(69, 24);
            this.label1.TabIndex = 0;
            this.label1.Text = "Robot 1";
            // 
            // label2
            // 
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(12, 71);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(69, 24);
            this.label2.TabIndex = 1;
            this.label2.Text = "Robot 2";
            // 
            // label3
            // 
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(12, 103);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(69, 24);
            this.label3.TabIndex = 2;
            this.label3.Text = "Robot 3";
            // 
            // label4
            // 
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(12, 135);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(69, 24);
            this.label4.TabIndex = 3;
            this.label4.Text = "Robot 4";
            // 
            // label5
            // 
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(12, 167);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(69, 24);
            this.label5.TabIndex = 4;
            this.label5.Text = "Robot 5";
            // 
            // txt_Robot2COM
            // 
            this.txt_Robot2COM.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot2COM.Location = new System.Drawing.Point(117, 68);
            this.txt_Robot2COM.Name = "txt_Robot2COM";
            this.txt_Robot2COM.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot2COM.TabIndex = 5;
            this.txt_Robot2COM.Text = "COM2";
            // 
            // txt_Robot3COM
            // 
            this.txt_Robot3COM.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot3COM.Location = new System.Drawing.Point(117, 100);
            this.txt_Robot3COM.Name = "txt_Robot3COM";
            this.txt_Robot3COM.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot3COM.TabIndex = 6;
            this.txt_Robot3COM.Text = "COM3";
            // 
            // txt_Robot4COM
            // 
            this.txt_Robot4COM.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot4COM.Location = new System.Drawing.Point(117, 132);
            this.txt_Robot4COM.Name = "txt_Robot4COM";
            this.txt_Robot4COM.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot4COM.TabIndex = 7;
            this.txt_Robot4COM.Text = "COM4";
            // 
            // txt_Robot5COM
            // 
            this.txt_Robot5COM.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot5COM.Location = new System.Drawing.Point(117, 164);
            this.txt_Robot5COM.Name = "txt_Robot5COM";
            this.txt_Robot5COM.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot5COM.TabIndex = 8;
            this.txt_Robot5COM.Text = "COM5";
            // 
            // label6
            // 
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(113, 9);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(104, 24);
            this.label6.TabIndex = 9;
            this.label6.Text = "COM Port";
            // 
            // btn_Start
            // 
            this.btn_Start.Font = new System.Drawing.Font("Microsoft Sans Serif", 20.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btn_Start.Location = new System.Drawing.Point(16, 242);
            this.btn_Start.Name = "btn_Start";
            this.btn_Start.Size = new System.Drawing.Size(331, 40);
            this.btn_Start.TabIndex = 10;
            this.btn_Start.Text = "Start";
            this.btn_Start.UseVisualStyleBackColor = true;
            this.btn_Start.Click += new System.EventHandler(this.btn_Start_Click);
            // 
            // RobotSerial1
            // 
            this.RobotSerial1.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.RobotSerial1_DataReceived);
            // 
            // RobotSerial2
            // 
            this.RobotSerial2.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.RobotSerial2_DataReceived);
            // 
            // RobotSerial3
            // 
            this.RobotSerial3.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.RobotSerial3_DataReceived);
            // 
            // RobotSerial4
            // 
            this.RobotSerial4.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.RobotSerial4_DataReceived);
            // 
            // RobotSerial5
            // 
            this.RobotSerial5.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.RobotSerial5_DataReceived);
            // 
            // label7
            // 
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(228, 9);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(104, 24);
            this.label7.TabIndex = 16;
            this.label7.Text = "Baud Rate";
            // 
            // txt_Robot5Baud
            // 
            this.txt_Robot5Baud.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot5Baud.Location = new System.Drawing.Point(232, 164);
            this.txt_Robot5Baud.Name = "txt_Robot5Baud";
            this.txt_Robot5Baud.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot5Baud.TabIndex = 15;
            this.txt_Robot5Baud.Text = "9600";
            // 
            // txt_Robot4Baud
            // 
            this.txt_Robot4Baud.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot4Baud.Location = new System.Drawing.Point(232, 132);
            this.txt_Robot4Baud.Name = "txt_Robot4Baud";
            this.txt_Robot4Baud.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot4Baud.TabIndex = 14;
            this.txt_Robot4Baud.Text = "9600";
            // 
            // txt_Robot3Baud
            // 
            this.txt_Robot3Baud.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot3Baud.Location = new System.Drawing.Point(232, 100);
            this.txt_Robot3Baud.Name = "txt_Robot3Baud";
            this.txt_Robot3Baud.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot3Baud.TabIndex = 13;
            this.txt_Robot3Baud.Text = "9600";
            // 
            // txt_Robot2Baud
            // 
            this.txt_Robot2Baud.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot2Baud.Location = new System.Drawing.Point(232, 68);
            this.txt_Robot2Baud.Name = "txt_Robot2Baud";
            this.txt_Robot2Baud.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot2Baud.TabIndex = 12;
            this.txt_Robot2Baud.Text = "9600";
            // 
            // txt_Robot1Baud
            // 
            this.txt_Robot1Baud.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_Robot1Baud.Location = new System.Drawing.Point(232, 36);
            this.txt_Robot1Baud.Name = "txt_Robot1Baud";
            this.txt_Robot1Baud.Size = new System.Drawing.Size(100, 26);
            this.txt_Robot1Baud.TabIndex = 11;
            this.txt_Robot1Baud.Text = "9600";
            // 
            // MainMenu
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(367, 294);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.txt_Robot5Baud);
            this.Controls.Add(this.txt_Robot4Baud);
            this.Controls.Add(this.txt_Robot3Baud);
            this.Controls.Add(this.txt_Robot2Baud);
            this.Controls.Add(this.txt_Robot1Baud);
            this.Controls.Add(this.btn_Start);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.txt_Robot5COM);
            this.Controls.Add(this.txt_Robot4COM);
            this.Controls.Add(this.txt_Robot3COM);
            this.Controls.Add(this.txt_Robot2COM);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.txt_Robot1COM);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "MainMenu";
            this.Text = "Main Menu";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox txt_Robot1COM;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox txt_Robot2COM;
        private System.Windows.Forms.TextBox txt_Robot3COM;
        private System.Windows.Forms.TextBox txt_Robot4COM;
        private System.Windows.Forms.TextBox txt_Robot5COM;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Button btn_Start;
        private System.IO.Ports.SerialPort RobotSerial1;
        private System.IO.Ports.SerialPort RobotSerial2;
        private System.IO.Ports.SerialPort RobotSerial3;
        private System.IO.Ports.SerialPort RobotSerial4;
        private System.IO.Ports.SerialPort RobotSerial5;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox txt_Robot5Baud;
        private System.Windows.Forms.TextBox txt_Robot4Baud;
        private System.Windows.Forms.TextBox txt_Robot3Baud;
        private System.Windows.Forms.TextBox txt_Robot2Baud;
        private System.Windows.Forms.TextBox txt_Robot1Baud;
    }
}

