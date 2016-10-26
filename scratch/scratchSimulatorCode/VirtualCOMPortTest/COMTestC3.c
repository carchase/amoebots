#include    <windows.h>
#include    <stdlib.h>
#include    <stdio.h>
#include    <string.h>
#include    <commdlg.h>
//#include  <windef.h>
 
int nread,nwrite;
 
 
void main()
{
    HANDLE hSerial;
    COMMTIMEOUTS timeouts;
    COMMCONFIG dcbSerialParams;
    char *words, *buffRead, *buffWrite;
    DWORD dwBytesWritten, dwBytesRead;
 
    hSerial = CreateFile("COM9",GENERIC_READ | GENERIC_WRITE,0,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL);
 
    if ( hSerial == INVALID_HANDLE_VALUE) 
    {
        if (GetLastError() == ERROR_FILE_NOT_FOUND)
        {
            printf(" serial port does not exist \n");
        }
        printf(" some other error occured. Inform user.\n");
    }
 
 
    //DCB    dcbSerialParams ;
    //GetCommState( hSerial, &dcbSerialParams.dcb);
    if (!GetCommState(hSerial, &dcbSerialParams.dcb)) 
    {
        printf("error getting state \n");
    }
 
    dcbSerialParams.dcb.DCBlength = sizeof(dcbSerialParams.dcb);
 
 
    dcbSerialParams.dcb.BaudRate = CBR_9600;
    dcbSerialParams.dcb.ByteSize = 8;
    dcbSerialParams.dcb.StopBits = ONESTOPBIT;
    dcbSerialParams.dcb.Parity = NOPARITY;
 
    dcbSerialParams.dcb.fBinary = TRUE;
    dcbSerialParams.dcb.fDtrControl = DTR_CONTROL_DISABLE;
    dcbSerialParams.dcb.fRtsControl = RTS_CONTROL_DISABLE;
    dcbSerialParams.dcb.fOutxCtsFlow = FALSE;
    dcbSerialParams.dcb.fOutxDsrFlow = FALSE;
    dcbSerialParams.dcb.fDsrSensitivity= FALSE;
    dcbSerialParams.dcb.fAbortOnError = TRUE;
 
    if (!SetCommState(hSerial, &dcbSerialParams.dcb)) 
    {
        printf(" error setting serial port state \n");
    }
 
 
    GetCommTimeouts(hSerial,&timeouts);
    //COMMTIMEOUTS timeouts = {0};
 
    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 50;
    timeouts.WriteTotalTimeoutMultiplier= 10;
 
    if(!SetCommTimeouts(hSerial, &timeouts)) 
    {
        printf("error setting port state \n");
    }
 
 
 
 
 
    //****************Write Operation*********************//
    words = "This is a string to be written to serial port COM1";
    nwrite = strlen(words);
 
    buffWrite = words;
    dwBytesWritten = 0;
 
    if (!WriteFile(hSerial, buffWrite, nwrite, &dwBytesWritten, NULL)) 
    { 
        printf("error writing to output buffer \n");
    }
//printf("Data written to write buffer is \n %s \n",buffWrite);
 
 
 
//***************Read Operation******************//
    //buffRead = 0;
    dwBytesRead = 0;
    nread = strlen(words);
 
    if (!ReadFile(hSerial, buffRead, nread, &dwBytesRead, NULL)) 
    {
        printf("error reading from input buffer \n");
    }
    printf("Data read from read buffer is \n %s \n",buffRead);
 
 
    CloseHandle(hSerial);
 
}