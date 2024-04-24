/*******************************************************************************
**  MODULE:        MSXINP.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Input data processor for the EPANET Multi-Species Extension
**                 toolkit.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   08/20/2022
*******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "msxtypes.h"
#include "msxutils.h"
#include "msxdict.h"
#include "epanet2.h"

//  Constants
//-----------
#define MAXERRS 100                    // Max. input errors reported
#define MAXTOKS  40                    // Max. items per line of input
#define SEPSTR  " \t\n\r"              // Token separator characters

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data

//  Local variables
//-----------------
static char *Tok[MAXTOKS];             // String tokens from line of input
static int  Ntokens;                   // Number of tokens in line of input
static double **TermArray;             // Incidence array used to check Terms  

enum InpErrorCodes {                   // Error codes (401 - 409)
    INP_ERR_FIRST        = 400,
    ERR_LINE_LENGTH,
    ERR_ITEMS, 
    ERR_KEYWORD,
    ERR_NUMBER,
    ERR_NAME,
    ERR_RESERVED_NAME,
    ERR_DUP_NAME,
    ERR_DUP_EXPR, 
    ERR_MATH_EXPR,
    ERR_UNSUPPORTED_OPTION,
    INP_ERR_LAST};

static char  *InpErrorTxt[INP_ERR_LAST-INP_ERR_FIRST] = {
    "",
    "Error 401 (too many characters)",
    "Error 402 (too few input items)",
    "Error 403 (invalid keyword)",
    "Error 404 (invalid numeric value)",
    "Error 405 (reference to undefined object)",
    "Error 406 (illegal use of a reserved name)",
    "Error 407 (name already used by another object)",
    "Error 408 (species already assigned an expression)", 
    "Error 409 (illegal math expression)",
    "Error 410 (option no longer supported)"};

//  Imported functions
//--------------------
int    MSXproj_addObject(int type, char *id, int n);
int    MSXproj_findObject(int type, char *id);
char * MSXproj_findID(int type, char *id);

//  Exported functions
//--------------------
int    MSXinp_countMsxObjects(void);
int    MSXinp_countNetObjects(void);
int    MSXinp_readNetData(void);
int    MSXinp_readMsxData(void);
void   MSXinp_getSpeciesUnits(int m, char *units);

//  Local functions
//-----------------
static int    getLineLength(char *line);
static int    getNewSection(char *tok, char *sectWords[], int *sect);
static int    addSpecies(char *line);
static int    addCoeff(char *line);
static int    addTerm(char *id);
static int    addPattern(char *id);
static int    checkID(char *id);
static int    parseLine(int sect, char *line);
static int    parseOption(void);
static int    parseSpecies(void);
static int    parseCoeff(void);
static int    parseTerm(void);
static int    parseExpression(int classType);
static int    parseTankData(void);
static int    parseQuality(void);
static int    parseParameter(void);
static int    parseSource(void);
static int    parsePattern(void);
static int    parseReport(void);
static int    parseDiffu(void);
static int    getVariableCode(char *id);
static int    getTokens(char *s);
static void   writeInpErrMsg(int errcode, char *sect, char *line, int lineCount);

static int    checkCyclicTerms(void);                                          
static int    traceTermPath(int i, int istar, int n);                          

//=============================================================================

int MSXinp_countMsxObjects()
/*
**  Purpose:
**    reads multi-species input file to determine number of system objects.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    char  line[MAXLINE+1];             // line from input data file     
    char  wLine[MAXLINE+1];            // working copy of input line   
    char  *tok;                        // first string token of line          
    int   sect = -1;                   // input data sections          
    int   errcode = 0;                 // error code
    int   errsum = 0;                  // number of errors found                   
    long  lineCount = 0;

// --- write name of input file to EPANET report file
    
    strcpy(MSX.Msg, "Processing MSX input file ");
    strcpy(line, MSX.MsxFile.name);
    strcat(MSX.Msg, line);
    ENwriteline(MSX.Msg);
    ENwriteline("");

// --- make pass through EPANET-MSX data file counting number of each object

    while ( fgets(line, MAXLINE, MSX.MsxFile.file) != NULL )
    {

    // --- skip blank lines & those beginning with a comment

        errcode = 0;
        lineCount++;
        strcpy(wLine, line);           // make working copy of line
        tok = strtok(wLine, SEPSTR);   // get first text token on line
        if ( tok == NULL || *tok == ';' ) continue;
        if ( getNewSection(tok, MsxSectWords, &sect) ) continue;

    // --- read id names from SPECIES, COEFFS, TERMS, & PATTERNS sections

        if ( sect == s_SPECIES ) errcode = addSpecies(line);
        if ( sect == s_COEFF )   errcode = addCoeff(line);
        if ( sect == s_TERM )    errcode = addTerm(tok);
        if ( sect == s_PATTERN ) errcode = addPattern(tok);


    // --- report any error found

        if ( errcode )
        {
            writeInpErrMsg(errcode, MsxSectWords[sect], line, lineCount);
            errsum++;
            if (errsum >= MAXERRS ) break;
        }
    }

// --- return error code

    if ( errsum > 0 ) return ERR_MSX_INPUT;
    return errcode;
}

//=============================================================================

int  MSXinp_countNetObjects()
/*
**  Purpose:
**    queries EPANET data base to determine number of network objects.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int errcode = 0;

// --- retrieve number of network elements

    CALL(errcode, ENgetcount(EN_NODECOUNT, &MSX.Nobjects[NODE]));
    CALL(errcode, ENgetcount(EN_TANKCOUNT, &MSX.Nobjects[TANK]));
    CALL(errcode, ENgetcount(EN_LINKCOUNT, &MSX.Nobjects[LINK]));
    return errcode;
}

//=============================================================================

int MSXinp_readNetData()
/*
**  Purpose:
**    retrieves required input data from the EPANET project data.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int   errcode = 0;
    int   i, k, n, t = 0;
    int   n1 = 0, n2 = 0;
    long  qstep;
    float diam = 0.0, len = 0.0, v0 = 0.0, xmix = 0.0, vmix = 0.0;

    float roughness = 0.0;   

// --- get flow units & time parameters

    CALL(errcode, ENgetflowunits(&MSX.Flowflag));
    if ( MSX.Flowflag >= EN_LPS ) MSX.Unitsflag = SI;
    else                          MSX.Unitsflag = US;
    CALL(errcode, ENgettimeparam(EN_QUALSTEP, &qstep));
    MSX.Qstep = qstep * 1000;
    CALL(errcode, ENgettimeparam(EN_REPORTSTEP, &MSX.Rstep));
    CALL(errcode, ENgettimeparam(EN_REPORTSTART, &MSX.Rstart));
    CALL(errcode, ENgettimeparam(EN_PATTERNSTEP, &MSX.Pstep));
    CALL(errcode, ENgettimeparam(EN_PATTERNSTART, &MSX.Pstart));
    CALL(errcode, ENgettimeparam(EN_STATISTIC, &MSX.Statflag));

// --- read tank/reservoir data

    n = MSX.Nobjects[NODE] - MSX.Nobjects[TANK];
    for (i=1; i<=MSX.Nobjects[NODE]; i++)
    {
        k = i - n;
        if ( k > 0 )
        {
            CALL(errcode, ENgetnodetype(i, &t));
            CALL(errcode, ENgetnodevalue(i, EN_INITVOLUME, &v0));
            CALL(errcode, ENgetnodevalue(i, EN_MIXMODEL,   &xmix));
            CALL(errcode, ENgetnodevalue(i, EN_MIXZONEVOL, &vmix));
            if ( !errcode )
            {
                MSX.Node[i].tank = k;
                MSX.Tank[k].node = i;
                if ( t == EN_RESERVOIR ) MSX.Tank[k].a = 0.0;
                else                     MSX.Tank[k].a = 1.0;
                MSX.Tank[k].v0       = v0;
                MSX.Tank[k].mixModel = (int)xmix;
                MSX.Tank[k].vMix     = vmix;
            }
        }
    }

// --- read link data

    for (i=1; i<=MSX.Nobjects[LINK]; i++)
    {
        CALL(errcode, ENgetlinknodes(i, &n1, &n2));
        CALL(errcode, ENgetlinkvalue(i, EN_DIAMETER, &diam));
        CALL(errcode, ENgetlinkvalue(i, EN_LENGTH, &len));
        CALL(errcode, ENgetlinkvalue(i, EN_ROUGHNESS, &roughness));  
        if ( !errcode )
        {
            MSX.Link[i].n1 = n1;
            MSX.Link[i].n2 = n2;
            MSX.Link[i].diam = diam;
            MSX.Link[i].len = len;
            MSX.Link[i].roughness = roughness;  
        }
    }
    return errcode;
}

//=============================================================================

int  MSXinp_readMsxData()
/*
**  Purpose:
**    reads multi-species data from the EPANET-MSX input file.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    char  line[MAXLINE+1];             // line from input data file
    char  wLine[MAXLINE+1];            // working copy of input line
    int   sect = -1;                   // input data sections
    int   errsum = 0;                  // number of errors found
    int   inperr = 0;                  // input error code
    long  lineCount = 0;               // line count

// --- create the TermArray for checking circular references in Terms         

	TermArray = createMatrix(MSX.Nobjects[TERM]+1, MSX.Nobjects[TERM]+1);      
	if ( TermArray == NULL ) return ERR_MEMORY;                                

// --- read each line from MSX input file

    rewind(MSX.MsxFile.file);
    while ( fgets(line, MAXLINE, MSX.MsxFile.file) != NULL )
    {
    // --- make copy of line and scan for tokens

        lineCount++;
        strcpy(wLine, line);
        Ntokens = getTokens(wLine);

    // --- skip blank lines and comments

        if ( Ntokens == 0 || *Tok[0] == ';' ) continue;

    // --- check if max. line length exceeded

        if ( getLineLength(line) >= MAXLINE )
        {
            inperr = ERR_LINE_LENGTH;
            writeInpErrMsg(inperr, MsxSectWords[sect], line, lineCount);
            errsum++;
        }

    // --- check if at start of a new input section

        if ( getNewSection(Tok[0], MsxSectWords, &sect) ) continue;

    // --- parse tokens from input line

        inperr = parseLine(sect, line);
        if ( inperr > 0 )
        {
            errsum++;
            writeInpErrMsg(inperr, MsxSectWords[sect], line, lineCount);
        }

    // --- stop if reach end of file or max. error count

        if (errsum >= MAXERRS) break;
    }   // End of while

// --- check for errors

    if ( checkCyclicTerms() ) errsum++;                                        
    freeMatrix(TermArray);                                                    
    if (errsum > 0) return ERR_MSX_INPUT;                                     
    return 0;
}

//=============================================================================

void   MSXinp_getSpeciesUnits(int m, char *units)
/*
**  Purpose:
**    constructs the character string for a species concentration units.
**
**  Input:
**    m = species index
**
**  Output:
**    units = character string with species concentration units
*/
{
    strcpy(units, MSX.Species[m].units);
    strcat(units, "/");
    if ( MSX.Species[m].type == BULK ) strcat(units, "L");
    else strcat(units, AreaUnitsWords[MSX.AreaUnits]);
}

//=============================================================================

int  getLineLength(char *line)
/*
**  Purpose:
**    determines number of characters of data in a line of input.
**
**  Input:
**    line = line of text from an input file
**
**  Returns:
**    number of characters in the line (with comment ignored).
*/
{
    char *comment;
    int lineLength = (int)strlen(line);
    if ( lineLength >= MAXLINE )
    {
    // --- don't count comment if present
        comment = strchr(line, ';');
        if ( comment ) lineLength = (int)(comment - line);    // Pointer math here
    }
    return lineLength;
}

//=============================================================================

int  getNewSection(char *tok, char *sectWords[], int *sect)
/*
**  Purpose:
**    checks if a line begins a new section in the input file.
**
**  Input:
**    tok = a string token 
**    sectWords = array of input file section keywords
**
**  Output:
**    sect = index code of section matching tok (or -1 if no match)
**
**  Returns:
**    1 if a section is found, 0 if not
*/
{
	int newsect;

// --- check if line begins with a new section heading

    if ( *tok == '[' )
    {
    // --- look for section heading in list of section keywords

        newsect = MSXutils_findmatch(tok, sectWords);
        if ( newsect >= 0 ) *sect = newsect;
        else *sect = -1;
        return 1;
    }
    return 0;
}

//=============================================================================

int addSpecies(char *line)
/* 
**  Purpose:
**    adds a species ID name to the project.
**
**  Input:
**    line = line of input data
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int errcode = 0;
    Ntokens = getTokens(line);
    if ( Ntokens < 2 ) return ERR_ITEMS;
    errcode = checkID(Tok[1]);
    if ( errcode ) return errcode;
    if ( MSXproj_addObject(SPECIES, Tok[1], MSX.Nobjects[SPECIES]+1) < 0 )
        errcode = 101;
    else MSX.Nobjects[SPECIES]++;
    return errcode;
}

//=============================================================================

int addCoeff(char *line)
/* 
**  Purpose:
**    adds a coefficient ID name to the project.
**
**  Input:
**    line = line of input data
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int k;
    int errcode = 0;

// --- determine the type of coeff.

    Ntokens = getTokens(line);
    if ( Ntokens < 2 ) return ERR_ITEMS;
    if      (MSXutils_match(Tok[0], "PARAM")) k = PARAMETER;
    else if (MSXutils_match(Tok[0], "CONST")) k = CONSTANT;
    else return ERR_KEYWORD;

// --- check for valid id name

    errcode = checkID(Tok[1]);
    if ( errcode ) return errcode;
    if ( MSXproj_addObject(k, Tok[1], MSX.Nobjects[k]+1) < 0 )
        errcode = 101;
    else MSX.Nobjects[k]++;
    return errcode;
}

//=============================================================================

int addTerm(char *id)
/* 
**  Purpose:
**    adds an intermediate expression term ID name to the project.
**
**  Input:
**    id = name of an intermediate expression term 
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int errcode = checkID(id);
    if ( !errcode )
    {
        if ( MSXproj_addObject(TERM, id, MSX.Nobjects[TERM]+1) < 0 )
            errcode = 101;
        else MSX.Nobjects[TERM]++;
    }
    return errcode;
}

//=============================================================================

int addPattern(char *id)
/* 
**  Purpose:
**    adds a time pattern ID name to the project.
**
**  Input:
**    id = name of a time pattern
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int errcode = 0;

    // --- a time pattern can span several lines

    if ( MSXproj_findObject(PATTERN, id) <= 0 )
    {
        if ( MSXproj_addObject(PATTERN, id, MSX.Nobjects[PATTERN]+1) < 0 )
            errcode = 101;
        else MSX.Nobjects[PATTERN]++;
    }
    return errcode;
}

//=============================================================================

int checkID(char *id)
/* 
**  Purpose:
**    checks that an object's name is unique
**
**  Input:
**    id = name of an object 
**
**  Returns:
**    an error code (0 if successful)
*/
{
// --- check that id name is not a reserved word
   int i = 1;
   while (HydVarWords[i] != NULL)
   {
      if (MSXutils_strcomp(id, HydVarWords[i])) return ERR_RESERVED_NAME;
      i++;
   }
    
// --- check that id name not used before

    if ( MSXproj_findObject(SPECIES, id) > 0 ||
         MSXproj_findObject(TERM, id)   > 0 ||
         MSXproj_findObject(PARAMETER, id)  > 0 ||
         MSXproj_findObject(CONSTANT, id)  > 0
       ) return ERR_DUP_NAME;
    return 0;
}        

//=============================================================================

int parseLine(int sect, char *line)
/* 
**  Purpose:
**    parses the contents of a line of input data.
**
**  Input:
**    sect = index of current input data section
**    line = contents of current line of input data
**
**  Returns:
**    an error code (0 if no error)
*/
{
    switch(sect)
    {
      case s_TITLE:
        strcpy(MSX.Title, line);
        break;

      case s_OPTION:
        return parseOption();

      case s_SPECIES:
        return parseSpecies();

      case s_COEFF:
        return parseCoeff();

      case s_TERM:
        return parseTerm();
      
      case s_PIPE:
        return parseExpression(LINK);

      case s_TANK:
        return parseExpression(TANK);

      case s_SOURCE:
        return parseSource();

      case s_QUALITY:
        return parseQuality();

      case s_PARAMETER:
        return parseParameter();

      case s_PATTERN:
        return parsePattern();

      case s_REPORT:
        return parseReport();

      case s_Diffu:
          return parseDiffu();
    }
    return 0;
}

//=============================================================================

int parseOption()
/*
**  Purpose:
**    parses an input line containing a project option.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int k;
    double v;

// --- determine which option is being read

    if ( Ntokens < 2 ) return 0;
    k = MSXutils_findmatch(Tok[0], OptionTypeWords);
    if ( k < 0 ) return ERR_KEYWORD;

// --- parse the value for the given option

    switch ( k )
    {
      case AREA_UNITS_OPTION:
          k = MSXutils_findmatch(Tok[1], AreaUnitsWords);
          if ( k < 0 ) return ERR_KEYWORD;
          MSX.AreaUnits = k;
          break;

      case RATE_UNITS_OPTION:
          k = MSXutils_findmatch(Tok[1], TimeUnitsWords);
          if ( k < 0 ) return ERR_KEYWORD;
          MSX.RateUnits = k;
          break;

      case SOLVER_OPTION:
          k = MSXutils_findmatch(Tok[1], SolverTypeWords);
          if ( k < 0 ) return ERR_KEYWORD;
          MSX.Solver = k;
          break;

      case COUPLING_OPTION:
          k = MSXutils_findmatch(Tok[1], CouplingWords);
          if ( k < 0 ) return ERR_KEYWORD;
          MSX.Coupling = k;
          break;

      case TIMESTEP_OPTION:

          // Read time step as a floating point value in seconds
          if ( !MSXutils_getDouble(Tok[1], &v) ) return ERR_NUMBER;
          if ( v < 0.001 ) return ERR_NUMBER;

          // Convert time step to integer milliseconds
          v = round(v * 1000.);
          MSX.Qstep = (int64_t)v;
          break;

      case RTOL_OPTION:
          if ( !MSXutils_getDouble(Tok[1], &MSX.DefRtol) ) return ERR_NUMBER;
          break;

      case ATOL_OPTION:
          if ( !MSXutils_getDouble(Tok[1], &MSX.DefAtol) ) return ERR_NUMBER;
          break;

      case COMPILER_OPTION:                                                    
          k = MSXutils_findmatch(Tok[1], CompilerWords);
          if ( k < 0 ) return ERR_KEYWORD;
    	  MSX.Compiler = k;
          break;

      case PECLETNUMER_OPTION:
          v = atof(Tok[1]);
          if (v <= 0.0)return ERR_NUMBER;
          MSX.Dispersion.PecletLimit = MAX(v, 1.0);
          break;

      case MAXSEGMENT_OPTION:
          k = atoi(Tok[1]);
          if (k <= 0) return ERR_NUMBER;
          MSX.MaxSegments = MAX(k, 50);  //at least 50 segments

    }
    return 0;
}

//=============================================================================

int parseSpecies()
/*
**  Purpose:
**    parses an input line containing a species variable.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int i;

// --- get Species index

    if ( Ntokens < 3 ) return ERR_ITEMS;
    i = MSXproj_findObject(SPECIES, Tok[1]);
    if ( i <= 0 ) return ERR_NAME;

// --- get pointer to Species name

    MSX.Species[i].id = MSXproj_findID(SPECIES, Tok[1]);

// --- get Species type

    if      ( MSXutils_match(Tok[0], "BULK") ) MSX.Species[i].type = BULK;
    else if ( MSXutils_match(Tok[0], "WALL") ) MSX.Species[i].type = WALL;
    else return ERR_KEYWORD;

// --- get Species units

    strncpy(MSX.Species[i].units, Tok[2], MAXUNITS);

// --- get Species error tolerance

    MSX.Species[i].aTol = 0.0;
    MSX.Species[i].rTol = 0.0;
    if ( Ntokens >= 4)
    {
        if ( !MSXutils_getDouble(Tok[3], &MSX.Species[i].aTol) )
            return ERR_NUMBER;
    }
    if ( Ntokens >= 5)
    {
        if ( !MSXutils_getDouble(Tok[4], &MSX.Species[i].rTol) )
            return ERR_NUMBER;
    }
    return 0;
}

//=============================================================================

int parseCoeff()
/*
**  Purpose:
**    parses an input line containing a coefficient definition.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int i, j;
    double x;

// --- check if variable is a Parameter

    if ( Ntokens < 2 ) return 0;
    if ( MSXutils_match(Tok[0], "PARAM") )
    {
    // --- get Parameter's index

        i = MSXproj_findObject(PARAMETER, Tok[1]);
        if ( i <= 0 ) return ERR_NAME;

    // --- get Parameter's value

        MSX.Param[i].id = MSXproj_findID(PARAMETER, Tok[1]); 
        if ( Ntokens >= 3 )
        {
            if ( !MSXutils_getDouble(Tok[2], &x) ) return ERR_NUMBER;
			MSX.Param[i].value = x;
            for (j=1; j<=MSX.Nobjects[LINK]; j++) MSX.Link[j].param[i] = x;
            for (j=1; j<=MSX.Nobjects[TANK]; j++) MSX.Tank[j].param[i] = x;
        }
        return 0;
    }

// --- check if variable is a Constant

    else if ( MSXutils_match(Tok[0], "CONST") )
    {
    // --- get Constant's index

        i = MSXproj_findObject(CONSTANT, Tok[1]);
        if ( i <= 0 ) return ERR_NAME;

    // --- get Constant's value

        MSX.Const[i].id = MSXproj_findID(CONSTANT, Tok[1]); 
        MSX.Const[i].value = 0.0;
        if ( Ntokens >= 3 )
        {
            if ( !MSXutils_getDouble(Tok[2], &MSX.Const[i].value) )
                return ERR_NUMBER;
        }
        return 0;
    }
    else return  ERR_KEYWORD;
}

//=============================================================================

int parseTerm()
/*
**  Purpose:
**    parses an input line containing an intermediate expression term .
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int i, j;
	int k;                                                                   
    char s[MAXLINE+1] = "";
    MathExpr *expr;

// --- get term's name

    if ( Ntokens < 2 ) return 0;
    i = MSXproj_findObject(TERM, Tok[0]);
    MSX.Term[i].id = MSXproj_findID(TERM, Tok[0]);                             

// --- reconstruct the expression string from its tokens

    for (j=1; j<Ntokens; j++)
	{                                                                          
		strcat(s, Tok[j]);                     
		k = MSXproj_findObject(TERM, Tok[j]);                                  
		if ( k > 0 ) TermArray[i][k] = 1.0;                                  
	}                                                                          
    
// --- convert expression into a postfix stack of op codes

    expr = mathexpr_create(s, getVariableCode);
    if ( expr == NULL ) return ERR_MATH_EXPR;

// --- assign the expression to a Term object

    MSX.Term[i].expr = expr;
    return 0;
}

//=============================================================================

int parseExpression(int classType)
/*
**  Purpose:
**    parses an input line containing a math expression.
**
**  Input:
**    classType = either LINK or TANK
**
**  Returns:
**    an error code (0 if  no error)
*/
{
    int i, j, k;
    char s[MAXLINE+1] = "";
    MathExpr *expr;

// --- determine expression type 

    if ( Ntokens < 3 ) return ERR_ITEMS;
    k = MSXutils_findmatch(Tok[0], ExprTypeWords);
    if ( k < 0 ) return ERR_KEYWORD;

// --- determine species associated with expression

    i = MSXproj_findObject(SPECIES, Tok[1]);
    if ( i < 1 ) return ERR_NAME;

// --- check that species does not already have an expression

    if ( classType == LINK )
    {
        if ( MSX.Species[i].pipeExprType != NO_EXPR ) return ERR_DUP_EXPR;
    }
    if ( classType == TANK )
    {
        if ( MSX.Species[i].tankExprType != NO_EXPR ) return ERR_DUP_EXPR;
    }

// --- reconstruct the expression string from its tokens

    for (j=2; j<Ntokens; j++) strcat(s, Tok[j]);
    
// --- convert expression into a postfix stack of op codes

    expr = mathexpr_create(s, getVariableCode);
    if ( expr == NULL ) return ERR_MATH_EXPR;

// --- assign the expression to the species

    switch (classType)
    {
    case LINK:
        MSX.Species[i].pipeExpr = expr;
        MSX.Species[i].pipeExprType = k;
        break;
    case TANK:
        MSX.Species[i].tankExpr = expr;
        MSX.Species[i].tankExprType = k;
        break;
    }
    return 0;    
}

//=============================================================================

int parseQuality()
/*
**  Purpose:
**    parses an input line containing initial species concentrations.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int err, i, j, k, m;
    double x;

// --- determine if quality value is global or object-specific

    if ( Ntokens < 3 ) return ERR_ITEMS;
    if      ( MSXutils_match(Tok[0], "GLOBAL") ) i = 1;
    else if ( MSXutils_match(Tok[0], "NODE") )   i = 2;
    else if ( MSXutils_match(Tok[0], "LINK") )   i = 3;
    else return ERR_KEYWORD;

// --- find species index

    k = 1;
    if ( i >= 2 ) k = 2;
    m = MSXproj_findObject(SPECIES, Tok[k]);
    if ( m <= 0 ) return ERR_NAME;

// --- get quality value

    if ( i >= 2  && Ntokens < 4 ) return ERR_ITEMS;
    k = 2;
    if ( i >= 2 ) k = 3;
    if ( !MSXutils_getDouble(Tok[k], &x) ) return ERR_NUMBER;

// --- for global specification, set initial quality either for
//     all nodes or links depending on type of species

    if ( i == 1)
    {
        MSX.C0[m] = x;
        if ( MSX.Species[m].type == BULK )
        {
            for (j=1; j<=MSX.Nobjects[NODE]; j++) MSX.Node[j].c0[m] = x;
        }
        for (j=1; j<=MSX.Nobjects[LINK]; j++) MSX.Link[j].c0[m] = x;
    }

// --- for a specific node, get its index & set its initial quality

    else if ( i == 2 )
    {
        err = ENgetnodeindex(Tok[1], &j);
        if ( err ) return ERR_NAME;
        if ( MSX.Species[m].type == BULK ) MSX.Node[j].c0[m] = x;
    }

// --- for a specific link, get its index & set its initial quality

    else if ( i == 3 )
    {
        err = ENgetlinkindex(Tok[1], &j);
        if ( err ) return ERR_NAME;
        MSX.Link[j].c0[m] = x;
    }
    return 0;
}

//=============================================================================

int parseParameter()
/*
**  Purpose:
**    parses an input line containing a parameter data.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int err, i, j;
    double x;

// --- get parameter name

    if ( Ntokens < 4 ) return 0;
    i = MSXproj_findObject(PARAMETER, Tok[2]);

// --- get parameter value

    if ( !MSXutils_getDouble(Tok[3], &x) ) return ERR_NUMBER;

// --- for pipe parameter, get pipe index and update parameter's value

    if ( MSXutils_match(Tok[0], "PIPE") )
    {
        err = ENgetlinkindex(Tok[1], &j);
        if ( err ) return ERR_NAME;
        MSX.Link[j].param[i] = x;
    }

// --- for tank parameter, get tank index and update parameter's value

    else if ( MSXutils_match(Tok[0], "TANK") )
    {
        err = ENgetnodeindex(Tok[1], &j);
        if ( err ) return ERR_NAME;
        j = MSX.Node[j].tank;
        if ( j > 0 ) MSX.Tank[j].param[i] = x;
    }
    else return ERR_KEYWORD;
    return 0;
}

//=============================================================================

int parseSource()
/*
**  Purpose:
**    parses an input line containing a source input data.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int err, i, j, k, m;
    double  x;
    Psource source;

// --- get source type

    if ( Ntokens < 4 ) return ERR_ITEMS;
    k = MSXutils_findmatch(Tok[0], SourceTypeWords);
    if ( k < 0 ) return ERR_KEYWORD;

// --- get node index

    err = ENgetnodeindex(Tok[1], &j);
    if ( err ) return ERR_NAME;

//  --- get species index

    m = MSXproj_findObject(SPECIES, Tok[2]);
    if ( m <= 0 ) return ERR_NAME;

// --- check that species is a BULK species

    if ( MSX.Species[m].type != BULK ) return 0;

// --- get base strength

    if ( !MSXutils_getDouble(Tok[3], &x) ) return ERR_NUMBER;

// --- get time pattern if present

    i = 0;
    if ( Ntokens >= 5 )
    {
        i = MSXproj_findObject(PATTERN, Tok[4]);
        if ( i <= 0 ) return ERR_NAME;
    }

// --- check if a source for this species already exists

    source = MSX.Node[j].sources;
    while ( source )
    {
        if ( source->species == m ) break;
        source = source->next;
    }

// --- otherwise create a new source object

    if ( source == NULL )
    {
        source = (struct Ssource *) malloc(sizeof(struct Ssource));
        if ( source == NULL ) return 101;
        source->next = MSX.Node[j].sources;
        MSX.Node[j].sources = source;
    }

// --- save source's properties

    source->type    = (char)k;
    source->species = m;
    source->c0      = x;
    source->pat     = i;
    return 0;
}    

//=============================================================================

int parsePattern()
/*
**  Purpose:
**    parses an input line containing a time pattern data.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int i, k;
    double x;
    SnumList *listItem;

// --- get time pattern index

    if ( Ntokens < 2 ) return ERR_ITEMS;
    i = MSXproj_findObject(PATTERN, Tok[0]);
    if ( i <= 0 ) return ERR_NAME;
    MSX.Pattern[i].id = MSXproj_findID(PATTERN, Tok[0]);

// --- begin reading pattern multipliers

    k = 1;
    while ( k < Ntokens )
    {
        if ( !MSXutils_getDouble(Tok[k], &x) ) return ERR_NUMBER;
        listItem = (SnumList *) malloc(sizeof(SnumList));
        if ( listItem == NULL ) return 101;
        listItem->value = x;
        listItem->next = NULL;
        if ( MSX.Pattern[i].first == NULL )
        {
            MSX.Pattern[i].current = listItem;
            MSX.Pattern[i].first = listItem;
        }
        else
        {
            MSX.Pattern[i].current->next = listItem;
            MSX.Pattern[i].current = listItem;
        }
        MSX.Pattern[i].length++;
        k++;
    }
    return 0;
}

//=============================================================================

int parseReport()
{
    int  i, j, k, err;

// --- get keyword

    if ( Ntokens < 2 ) return 0;
    k = MSXutils_findmatch(Tok[0], ReportWords);
    if ( k < 0 ) return ERR_KEYWORD;
    switch(k)
    {

    // --- keyword is NODE; parse ID names of reported nodes
    
        case 0:
        if ( MSXutils_strcomp(Tok[1], ALL) )
        {
            for (j=1; j<=MSX.Nobjects[NODE]; j++) MSX.Node[j].rpt = 1;
        }
        else if ( MSXutils_strcomp(Tok[1], NONE) )
        {
            for (j=1; j<=MSX.Nobjects[NODE]; j++) MSX.Node[j].rpt = 0;
        }
        else for (i=1; i<Ntokens; i++)
        {
            err = ENgetnodeindex(Tok[i], &j);
            if ( err ) return ERR_NAME;
            MSX.Node[j].rpt = 1;
        }
        break;

    // --- keyword is LINK: parse ID names of reported links
        case 1:
        if ( MSXutils_strcomp(Tok[1], ALL) )
        {
            for (j=1; j<=MSX.Nobjects[LINK]; j++) MSX.Link[j].rpt = 1;
        }
        else if ( MSXutils_strcomp(Tok[1], NONE) )
        {
            for (j=1; j<=MSX.Nobjects[LINK]; j++) MSX.Link[j].rpt = 0;
        }
        else for (i=1; i<Ntokens; i++)
        {
            err = ENgetlinkindex(Tok[i], &j);
            if ( err ) return ERR_NAME;
            MSX.Link[j].rpt = 1;
        }
        break;

    // --- keyword is SPECIES; get YES/NO & precision

        case 2:
        j = MSXproj_findObject(SPECIES, Tok[1]);
        if ( j <= 0 ) return ERR_NAME;
        if ( Ntokens >= 3 )
        {
            if ( MSXutils_strcomp(Tok[2], YES) ) MSX.Species[j].rpt = 1;
            else if ( MSXutils_strcomp(Tok[2], NO)  ) MSX.Species[j].rpt = 0;
            else return ERR_KEYWORD;
        }
        if ( Ntokens >= 4 )
        {
            if ( !MSXutils_getInt(Tok[3], &MSX.Species[j].precision) )
                return ERR_NUMBER;
        }
        break;

    // --- keyword is FILE: get name of report file

        case 3:
        strcpy(MSX.RptFile.name, Tok[1]);
        break;

    // --- keyword is PAGESIZE;

        case 4:
        if ( !MSXutils_getInt(Tok[1], &MSX.PageSize) ) return ERR_NUMBER;
        break;
    }
    return 0;
}

int parseDiffu()
/*
**  Purpose:
**    parses an input line containing molecular diffusivity data.
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error)
*/
{
    int m;
    double  x;

    // --- get source type
    if (Ntokens < 2) return ERR_ITEMS;

    //  --- get species index
    m = MSXproj_findObject(SPECIES, Tok[0]);
    if (m <= 0) return ERR_NAME;

    // --- check that species is a BULK species
    if (MSX.Species[m].type != BULK) return 0;

    // --- get base strength
    if (!MSXutils_getDouble(Tok[1], &x)) return ERR_NUMBER;
    if (x < 0) return ERR_NUMBER;

    if (Ntokens > 2 && MSXutils_match(Tok[2], "FIXED"))
    {
        x = x * MSX.Dispersion.DIFFUS;
        MSX.Dispersion.ld[m] = x;     
    }
    else
    {
        x = x * MSX.Dispersion.DIFFUS;
        MSX.Dispersion.md[m] = x;
    }
    MSX.DispersionFlag = 1;
    return 0;
}

//=============================================================================

int getVariableCode(char *id)
/*
**  Purpose:
**    finds the index assigned to a species, intermediate term,
**    parameter, or constant that appears in a math expression.
**
**  Input:
**    id = ID name being sought
**
**  Returns:
**    index of the symbolic variable or term named id.
**
**  Note:
**    Variables are assigned consecutive code numbers starting from 1 
**    and proceeding through each Species, Term, Parameter and Constant.
*/
{
    int j = MSXproj_findObject(SPECIES, id);
    if ( j >= 1 ) return j;
    j = MSXproj_findObject(TERM, id);
    if ( j >= 1 ) return MSX.Nobjects[SPECIES] + j;
    j = MSXproj_findObject(PARAMETER, id);
    if ( j >= 1 ) return MSX.Nobjects[SPECIES] + MSX.Nobjects[TERM] + j;
    j = MSXproj_findObject(CONSTANT, id);
    if ( j >= 1 ) return MSX.Nobjects[SPECIES] + MSX.Nobjects[TERM] + 
                         MSX.Nobjects[PARAMETER] + j;
    j = MSXutils_findmatch(id, HydVarWords);
    if ( j >= 1 ) return MSX.Nobjects[SPECIES] + MSX.Nobjects[TERM] + 
                         MSX.Nobjects[PARAMETER] + MSX.Nobjects[CONSTANT] + j;
    return -1;
}

//=============================================================================

int  getTokens(char *s)
/*
**  Purpose:
**    scans a string for tokens, saving pointers to them
**    in shared variable Tok[].
**
**  Input:
**    s = a character string
**
**  Returns:
**    number of tokens found in s
**
**  Notes:
**    Tokens can be separated by the characters listed in SEPSTR
**    (spaces, tabs, newline, carriage return) which is defined in
**    MSXGLOBALS.H. Text between quotes is treated as a single token.
*/
{
    int  len, m, n;
    char *c;

    // --- begin with no tokens

    for (n = 0; n < MAXTOKS; n++) Tok[n] = NULL;
    n = 0;

    // --- truncate s at start of comment 

    c = strchr(s,';');
    if (c) *c = '\0';
    len = (int)strlen(s);

    // --- scan s for tokens until nothing left

    while (len > 0 && n < MAXTOKS)
    {
        m = (int)strcspn(s,SEPSTR);              // find token length 
        if (m == 0) s++;                    // no token found
        else
        {
            if (*s == '"')                  // token begins with quote
            {
                s++;                        // start token after quote
                len--;                      // reduce length of s
                m = (int)strcspn(s,"\"\n"); // find end quote or new line
            }
            s[m] = '\0';                    // null-terminate the token
            Tok[n] = s;                     // save pointer to token 
            n++;                            // update token count
            s += m+1;                       // begin next token
        }
        len -= m+1;                         // update length of s
    }
    return(n);
}

//=============================================================================

void writeInpErrMsg(int errcode, char *sect, char *line, int lineCount)
{
    char msg[MAXMSG+1];
    if ( errcode >= INP_ERR_LAST  || errcode <= INP_ERR_FIRST )
    {
        sprintf(msg, "Error Code = %d", errcode);
    }
    else
    {
        sprintf(msg, "%s at line %d of %s] section:",
             InpErrorTxt[errcode-INP_ERR_FIRST], lineCount, sect);
    }
    ENwriteline("");
    ENwriteline(msg);
    ENwriteline(line);
}

//=============================================================================

int checkCyclicTerms()                                                         
/*
**  Purpose:
**    checks for cyclic references in Term expressions (e.g., T1 = T2 + T3
**    and T3 = T2/T1)
**
**  Input:
**    none
**
**  Returns:
**    1 if cyclic reference found or 0 if none found.
*/
{
    int i, j, n;
    char msg[MAXMSG+1];

    n = MSX.Nobjects[TERM];
    for (i=1; i<n; i++)
    {
        for (j=1; j<=n; j++) TermArray[0][j] = 0.0;
        if ( traceTermPath(i, i, n) )
	{
            sprintf(msg, "Error 410 - term %s contains a cyclic reference.",
                MSX.Term[i].id);
            ENwriteline(msg);
            return 1;
        }
    }
    return 0;
}

//=============================================================================

int traceTermPath(int i, int istar, int n)                                    
/*
**  Purpose:
**    checks if Term[istar] is in the path of terms that appear when evaluating
**    Term[i]
**
**  Input:
**    i = index of term whose expressions are to be traced
**    istar = index of term being searched for
**    n = total number of terms
**
**  Returns:
**    1 if term istar found; 0 if not found.
*/
{
    int j;
    if ( TermArray[0][i] == 1.0 ) return 0;
    TermArray[0][i] = 1.0;
    for (j=1; j<=n; j++)
    {
        if ( TermArray[i][j] == 0.0 ) continue;
        if ( j == istar ) return 1;
        else if ( traceTermPath(j, istar, n) ) return 1;
    }
    return 0;
}
