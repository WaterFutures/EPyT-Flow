/*******************************************************************************
**  MODULE:        MSXFUNCS.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   compiles chemistry functions to a shared dynamic library.
**  COPYRIGHT:     Copyright (C) 2007 Feng Shang, Lewis Rossman, and James Uber.
**                 All Rights Reserved. See license information in LICENSE.TXT.
**  AUTHORS:       see AUTHORS
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2014
*******************************************************************************/

#include <stdio.h>

// --- define WINDOWS

#undef WINDOWS
#ifdef _WIN32
  #define WINDOWS
#endif
#ifdef __WIN32__
  #define WINDOWS
#endif
#ifdef WIN32
  #define WINDOWS
#endif

#ifdef WINDOWS
#include <windows.h>
HMODULE hDLL;
#else
  #include <dlfcn.h>
  void *hDLL; 
#endif

#include "msxfuncs.h"


MSXGETRATES    MSXgetPipeRates = NULL;
MSXGETRATES    MSXgetTankRates = NULL;
MSXGETEQUIL    MSXgetPipeEquil = NULL;
MSXGETEQUIL    MSXgetTankEquil = NULL;
MSXGETFORMULAS MSXgetPipeFormulas = NULL;
MSXGETFORMULAS MSXgetTankFormulas = NULL;



//=============================================================================

int MSXfuncs_load(char * libName)
/*
**  Purpose:
**    loads compiled chemistry functions from a named library
**
**  Input:
**    libName = path to shared library
**
**  Returns:
**    an error code (0 if no error).
*/
{

#ifdef WINDOWS
	hDLL = LoadLibraryA(libName);
	if (hDLL == NULL) return 1;

	  MSXgetPipeRates    = (MSXGETRATES)    GetProcAddress(hDLL, "MSXgetPipeRates");
    MSXgetTankRates    = (MSXGETRATES)    GetProcAddress(hDLL, "MSXgetTankRates");
    MSXgetPipeEquil    = (MSXGETEQUIL)    GetProcAddress(hDLL, "MSXgetPipeEquil");
    MSXgetTankEquil    = (MSXGETEQUIL)    GetProcAddress(hDLL, "MSXgetTankEquil");
    MSXgetPipeFormulas = (MSXGETFORMULAS) GetProcAddress(hDLL, "MSXgetPipeFormulas");
    MSXgetTankFormulas = (MSXGETFORMULAS) GetProcAddress(hDLL, "MSXgetTankFormulas");

#else
    hDLL = dlopen(libName, RTLD_LAZY);
    if (hDLL == NULL) return 1;
	
    MSXgetPipeRates    = (MSXGETRATES)    dlsym(hDLL, "MSXgetPipeRates");
    MSXgetTankRates    = (MSXGETRATES)    dlsym(hDLL, "MSXgetTankRates");
    MSXgetPipeEquil    = (MSXGETEQUIL)    dlsym(hDLL, "MSXgetPipeEquil");
    MSXgetTankEquil    = (MSXGETEQUIL)    dlsym(hDLL, "MSXgetTankEquil");
    MSXgetPipeFormulas = (MSXGETFORMULAS) dlsym(hDLL, "MSXgetPipeFormulas");
    MSXgetTankFormulas = (MSXGETFORMULAS) dlsym(hDLL, "MSXgetTankFormulas");
#endif

    if (MSXgetPipeRates == NULL || MSXgetTankRates == NULL ||
        MSXgetPipeEquil == NULL || MSXgetTankEquil == NULL ||
        MSXgetPipeFormulas == NULL || MSXgetTankFormulas == NULL)
    {
        MSXfuncs_free();
        hDLL = NULL;
        return 2;
    }
    return 0;
}

//=============================================================================

void MSXfuncs_free()
/*
**  Purpose:
**    frees the handle to the shared function library
**
**  Input:
**    none
**
**  Returns:
**    none
*/
{
#ifdef WINDOWS
    if (hDLL) FreeLibrary(hDLL);
#else
    if (hDLL) dlclose(hDLL);
#endif
}

//=============================================================================

int MSXfuncs_run(char* cmdLine)
/*
**  Purpose:
**    executes a program and waits for it to end
**
**  Input:
**    cmdLine = command line string that executes the program
**
**  Returns:
**    the program's exit code (or -1 if the program was not run)
*/
{
#ifdef WINDOWS

  unsigned long exitCode;
  STARTUPINFOA si;
  PROCESS_INFORMATION  pi;

  // --- initialize data structures

  memset(&si, 0, sizeof(si));
  memset(&pi, 0, sizeof(pi));
  si.cb = sizeof(si);

  // --- hide the window that the program runs in

  si.dwFlags = STARTF_USESHOWWINDOW;
  si.wShowWindow = SW_HIDE;

  // --- execute the command line in a new console window
  exitCode = CreateProcess(NULL, cmdLine, NULL, NULL, 0,
		 CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi);
  if (exitCode == 0)
  {
	  exitCode = GetLastError();
	  return exitCode;
  }

  // --- wait for program to end

  exitCode = WaitForSingleObject(pi.hProcess, INFINITE);

  // --- retrieve the error code produced by the program

  BOOL rt = GetExitCodeProcess(pi.hProcess, &exitCode);

  // --- release handles

  CloseHandle(pi.hProcess);
  CloseHandle(pi.hThread);
  return exitCode;

#else
  return -1;
#endif
}

