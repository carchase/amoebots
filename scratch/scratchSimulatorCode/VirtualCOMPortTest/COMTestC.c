#include <stdio.h>
#include <windows.h>


int main(){
	HANDLE hcomm;
		
	hcomm = CreateFile("\\\\.\\CNCA1"),
						GENERIC_READ | GENERIC_WRITE,
						0,
						NULL,
						OPEN_EXITING,
						0,
						NULL);
						
	if (hcomm == INVALID_HANDLE_VALUE)
		printf("Error in opening serial port");
	else
		printf("Opening serial port successful.");
	
	CloseHandle(hcom);
	
	return 0;
}