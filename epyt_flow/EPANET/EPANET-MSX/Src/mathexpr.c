/******************************************************************************
**  MODULE:        MATHEXPR.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Evaluates symbolic mathematical expression consisting
**                 of numbers, variable names, math functions & arithmetic
**                 operators.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   09/02/2022
******************************************************************************/
/*
**   Operand codes:
** 	1 = (
** 	2 = )
** 	3 = +
** 	4 = - (subtraction)
** 	5 = *
** 	6 = /
** 	7 = number
** 	8 = user-defined variable
** 	9 = - (negative)
**	10 = cos
**	11 = sin
**	12 = tan
**	13 = cot
**	14 = abs
**	15 = sgn
**	16 = sqrt
**	17 = log
**	18 = exp
**	19 = asin
**	20 = acos
**	21 = atan
**      22 = acot
**	23 = sinh
**	24 = cosh
**	25 = tanh
**	26 = coth
**	27 = log10
**  28 = step (x<=0 ? 0 : 1)
**	31 = ^
******************************************************************************/
#define _CRT_SECURE_NO_WARNINGS

#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "mathexpr.h"

#define MAX_STACK_SIZE  1024

//***************************************************                         
#define MAX_TERM_SIZE  1024
struct MathTerm
{
    char s[MAX_TERM_SIZE];
};
typedef struct MathTerm Term;
//***************************************************


//  Local declarations
//--------------------
//  Structure for binary tree representation of math expression
struct TreeNode
{
    int    opcode;                // operator code
    int    ivar;                  // variable index
    double fvalue;                // numerical value
    struct TreeNode* left;        // left sub-tree of tokenized formula
    struct TreeNode* right;       // right sub-tree of tokenized formula
};
typedef struct TreeNode ExprTree;

// Local variables
//----------------
static int    Err;
static int    Bc;
static int    PrevLex, CurLex;
static int    Len, Pos;
static char* S;
static char   Token[255];
static int    Ivar;
static double Fvalue;

// math function names
char* MathFunc[] = { "COS", "SIN", "TAN", "COT", "ABS", "SGN",
                     "SQRT", "LOG", "EXP", "ASIN", "ACOS", "ATAN",
                     "ACOT", "SINH", "COSH", "TANH", "COTH", "LOG10",
                     "STEP", NULL };

// Local functions
//----------------
static int        sametext(char*, char*);
static int        isDigit(char);
static int        isLetter(char);
static void       getToken(void);
static int        getMathFunc(void);
static int        getVariable(void);
static int        getOperand(void);
static int        getLex(void);
static double     getNumber(void);
static ExprTree* newNode(void);
static ExprTree* getSingleOp(int*);
static ExprTree* getOp(int*);
static ExprTree* getTree(void);
static void       traverseTree(ExprTree*, MathExpr**);
static void       deleteTree(ExprTree*);

// Callback functions
static int    (*getVariableIndex) (char*); // return index of named variable
static double (*getVariableValue) (int);    // return value of indexed variable

//=============================================================================

int  sametext(char* s1, char* s2)
/*
**  Purpose:
**    performs case insensitive comparison of two strings.
**
**  Input:
**    s1 = character string
**    s2 = character string.
**
**  Returns:
**    1 if strings are the same, 0 otherwise.
*/
{
    int i;
    for (i = 0; toupper(s1[i]) == toupper(s2[i]); i++)
        if (!s1[i + 1] && !s2[i + 1]) return(1);
    return(0);
}

//=============================================================================

int isDigit(char c)
{
    if (c >= '1' && c <= '9') return 1;
    if (c == '0') return 1;
    return 0;
}

//=============================================================================

int isLetter(char c)
{
    if (c >= 'a' && c <= 'z') return 1;
    if (c >= 'A' && c <= 'Z') return 1;
    if (c == '_') return 1;
    return 0;
}

//=============================================================================

void getToken()
{
    char c[] = " ";
    Token[0] = '\0';
    while (Pos <= Len &&
        (isLetter(S[Pos]) || isDigit(S[Pos])))
    {
        c[0] = S[Pos];
        strcat(Token, c);
        Pos++;
    }
    Pos--;
}

//=============================================================================

int getMathFunc()
{
    int i = 0;
    while (MathFunc[i] != NULL)
    {
        if (sametext(MathFunc[i], Token)) return i + 10;
        i++;
    }
    return(0);
}

//=============================================================================

int getVariable()
{
    if (!getVariableIndex) return 0;
    Ivar = getVariableIndex(Token);
    if (Ivar >= 0) return 8;
    return 0;
}

//=============================================================================

double getNumber()
{
    char c[] = " ";
    char sNumber[255];
    int  errflag = 0;
    int  decimalCount = 0;

    /* --- get whole number portion of number */
    sNumber[0] = '\0';
    while (Pos < Len && isDigit(S[Pos]))
    {
        c[0] = S[Pos];
        strcat(sNumber, c);
        Pos++;
    }

    /* --- get fractional portion of number */
    if (Pos < Len)
    {
        if (S[Pos] == '.')
        {
            decimalCount++;
            if (decimalCount > 1) Err = 1;
            strcat(sNumber, ".");
            Pos++;
            while (Pos < Len && isDigit(S[Pos]))
            {
                c[0] = S[Pos];
                strcat(sNumber, c);
                Pos++;
            }
        }

        /* --- get exponent */
        if (Pos < Len && (S[Pos] == 'e' || S[Pos] == 'E'))
        {
            strcat(sNumber, "E");
            Pos++;
            if (Pos >= Len) errflag = 1;
            else
            {
                if (S[Pos] == '-' || S[Pos] == '+')
                {
                    c[0] = S[Pos];
                    strcat(sNumber, c);
                    Pos++;
                }
                if (Pos >= Len || !isDigit(S[Pos])) errflag = 1;
                else while (Pos < Len && isDigit(S[Pos]))
                {
                    c[0] = S[Pos];
                    strcat(sNumber, c);
                    Pos++;
                }
            }
        }
    }
    Pos--;
    if (errflag) return 0;
    else return atof(sNumber);
}

//=============================================================================

int getOperand()
{
    int code;
    switch (S[Pos])
    {
    case '(': code = 1;  break;
    case ')': code = 2;  break;
    case '+': code = 3;  break;
    case '-': code = 4;
        if (Pos < Len - 1 &&
            isDigit(S[Pos + 1]) &&
            (CurLex <= 6 || CurLex == 31))
        {
            Pos++;
            Fvalue = -getNumber();
            code = 7;
        }
        break;
    case '*': code = 5;  break;
    case '/': code = 6;  break;
    case '^': code = 31; break;
    default:  code = 0;
    }
    return code;
}

//=============================================================================

int getLex()
{
    int n;

    /* --- skip spaces */
    while (Pos < Len && S[Pos] == ' ') Pos++;
    if (Pos >= Len) return 0;

    /* --- check for operand */
    n = getOperand();

    /* --- check for function/variable/number */
    if (n == 0)
    {
        if (isLetter(S[Pos]))
        {
            getToken();
            n = getMathFunc();
            if (n == 0) n = getVariable();
        }
        else if (S[Pos] == '.' || isDigit(S[Pos]))
        {
            n = 7;
            Fvalue = getNumber();
        }
    }
    Pos++;
    PrevLex = CurLex;
    CurLex = n;
    return n;
}

//=============================================================================

ExprTree* newNode()
{
    ExprTree* node;
    node = (ExprTree*)malloc(sizeof(ExprTree));
    if (!node) Err = 2;
    else
    {
        node->opcode = 0;
        node->ivar = -1;
        node->fvalue = 0.;
        node->left = NULL;
        node->right = NULL;
    }
    return node;
}

//=============================================================================

ExprTree* getSingleOp(int* lex)
{
    int opcode;
    ExprTree* left;
    ExprTree* node;

    /* --- open parenthesis, so continue to grow the tree */
    if (*lex == 1)
    {
        Bc++;
        left = getTree();
    }

    else
    {
        /* --- Error if not a singleton operand */
        if (*lex < 7 || *lex == 9 || *lex > 30)
        {
            Err = 1;
            return NULL;
        }

        opcode = *lex;

        /* --- simple number or variable name */
        if (*lex == 7 || *lex == 8)
        {
            left = newNode();
            left->opcode = opcode;
            if (*lex == 7) left->fvalue = Fvalue;
            if (*lex == 8) left->ivar = Ivar;
        }

        /* --- function which must have a '(' after it */
        else
        {
            *lex = getLex();
            if (*lex != 1)
            {
                Err = 1;
                return NULL;
            }
            Bc++;
            left = newNode();
            left->left = getTree();
            left->opcode = opcode;
        }
    }
    *lex = getLex();

    /* --- exponentiation */
    if (*lex == 31)
    {
        node = newNode();
        node->left = left;
        node->opcode = *lex;
        *lex = getLex();
        node->right = getSingleOp(lex);
        left = node;
    }
    return left;
}

//=============================================================================

ExprTree* getOp(int* lex)
{
    int opcode;
    ExprTree* left;
    ExprTree* right;
    ExprTree* node;
    int neg = 0;

    *lex = getLex();
    if (PrevLex == 0 || PrevLex == 1)
    {
        if (*lex == 4)
        {
            neg = 1;
            *lex = getLex();
        }
        else if (*lex == 3) *lex = getLex();
    }
    left = getSingleOp(lex);
    while (*lex == 5 || *lex == 6)
    {
        opcode = *lex;
        *lex = getLex();
        right = getSingleOp(lex);
        node = newNode();
        if (Err) return NULL;
        node->left = left;
        node->right = right;
        node->opcode = opcode;
        left = node;
    }
    if (neg)
    {
        node = newNode();
        if (Err) return NULL;
        node->left = left;
        node->right = NULL;
        node->opcode = 9;
        left = node;
    }
    return left;
}

//=============================================================================

ExprTree* getTree()
{
    int      lex;
    int      opcode;
    ExprTree* left;
    ExprTree* right;
    ExprTree* node;

    left = getOp(&lex);
    for (;;)
    {
        if (lex == 0 || lex == 2)
        {
            if (lex == 2) Bc--;
            break;
        }

        if (lex != 3 && lex != 4)
        {
            Err = 1;
            break;
        }

        opcode = lex;
        right = getOp(&lex);
        node = newNode();
        if (Err) break;
        node->left = left;
        node->right = right;
        node->opcode = opcode;
        left = node;
    }
    return left;
}

//=============================================================================

void traverseTree(ExprTree* tree, MathExpr** expr)
// Converts binary tree to linked list (postfix format)
{
    MathExpr* node;
    if (tree == NULL) return;
    traverseTree(tree->left, expr);
    traverseTree(tree->right, expr);
    node = (MathExpr*)malloc(sizeof(MathExpr));
    if (node)
    {
        node->fvalue = tree->fvalue;
        node->opcode = tree->opcode;
        node->ivar = tree->ivar;
        node->next = NULL;
        node->prev = (*expr);
    }
    if (*expr) (*expr)->next = node;
    (*expr) = node;
}

//=============================================================================

void deleteTree(ExprTree* tree)
{
    if (tree)
    {
        if (tree->left)  deleteTree(tree->left);
        if (tree->right) deleteTree(tree->right);
        free(tree);
    }
}

//=============================================================================

// Turn on "precise" floating point option
#pragma float_control(precise, on, push)

double mathexpr_eval(MathExpr* expr, double (*getVariableValue) (int))
//  Mathematica expression evaluation using a stack
{

    // --- Note: the exprStack array must be declared locally and not globally
    //     since this function can be called recursively.

    double exprStack[MAX_STACK_SIZE];
    MathExpr* node = expr;
    double r1, r2;
    int stackindex = 0;

    exprStack[0] = 0.0;
    while (node != NULL)
    {
        switch (node->opcode)
        {
        case 3:
            r1 = exprStack[stackindex];
            stackindex--;
            r2 = exprStack[stackindex];
            exprStack[stackindex] = r2 + r1;
            break;

        case 4:
            r1 = exprStack[stackindex];
            stackindex--;
            r2 = exprStack[stackindex];
            exprStack[stackindex] = r2 - r1;
            break;

        case 5:
            r1 = exprStack[stackindex];
            stackindex--;
            r2 = exprStack[stackindex];
            exprStack[stackindex] = r2 * r1;
            break;

        case 6:
            r1 = exprStack[stackindex];
            stackindex--;
            r2 = exprStack[stackindex];
            exprStack[stackindex] = r2 / r1;
            break;

        case 7:
            stackindex++;
            exprStack[stackindex] = node->fvalue;
            break;

        case 8:
            if (getVariableValue != NULL)
                r1 = getVariableValue(node->ivar);
            else r1 = 0.0;
            stackindex++;
            exprStack[stackindex] = r1;
            break;

        case 9:
            exprStack[stackindex] = -exprStack[stackindex];
            break;

        case 10:
            r1 = exprStack[stackindex];
            r2 = cos(r1);
            exprStack[stackindex] = r2;
            break;

        case 11:
            r1 = exprStack[stackindex];
            r2 = sin(r1);
            exprStack[stackindex] = r2;
            break;

        case 12:
            r1 = exprStack[stackindex];
            r2 = tan(r1);
            exprStack[stackindex] = r2;
            break;

        case 13:
            r1 = exprStack[stackindex];
            r2 = 1.0 / tan(r1);
            exprStack[stackindex] = r2;
            break;

        case 14:
            r1 = exprStack[stackindex];
            r2 = fabs(r1);
            exprStack[stackindex] = r2;
            break;

        case 15:
            r1 = exprStack[stackindex];
            if (r1 < 0.0) r2 = -1.0;
            else if (r1 > 0.0) r2 = 1.0;
            else r2 = 0.0;
            exprStack[stackindex] = r2;
            break;

        case 16:
            r1 = exprStack[stackindex];
            r2 = sqrt(r1);
            exprStack[stackindex] = r2;
            break;

        case 17:
            r1 = exprStack[stackindex];
            r2 = log(r1);
            exprStack[stackindex] = r2;
            break;

        case 18:
            r1 = exprStack[stackindex];
            r2 = exp(r1);
            exprStack[stackindex] = r2;
            break;

        case 19:
            r1 = exprStack[stackindex];
            r2 = asin(r1);
            exprStack[stackindex] = r2;
            break;

        case 20:
            r1 = exprStack[stackindex];
            r2 = acos(r1);
            exprStack[stackindex] = r2;
            break;

        case 21:
            r1 = exprStack[stackindex];
            r2 = atan(r1);
            exprStack[stackindex] = r2;
            break;

        case 22:
            r1 = exprStack[stackindex];
            r2 = 1.57079632679489661923 - atan(r1);
            exprStack[stackindex] = r2;
            break;

        case 23:
            r1 = exprStack[stackindex];
            r2 = (exp(r1) - exp(-r1)) / 2.0;
            exprStack[stackindex] = r2;
            break;

        case 24:
            r1 = exprStack[stackindex];
            r2 = (exp(r1) + exp(-r1)) / 2.0;
            exprStack[stackindex] = r2;
            break;

        case 25:
            r1 = exprStack[stackindex];
            r2 = (exp(r1) - exp(-r1)) / (exp(r1) + exp(-r1));
            exprStack[stackindex] = r2;
            break;

        case 26:
            r1 = exprStack[stackindex];
            r2 = (exp(r1) + exp(-r1)) / (exp(r1) - exp(-r1));
            exprStack[stackindex] = r2;
            break;

        case 27:
            r1 = exprStack[stackindex];
            r2 = log10(r1);
            exprStack[stackindex] = r2;
            break;

        case 28:
            r1 = exprStack[stackindex];
            if (r1 <= 0.0) r2 = 0.0;
            else           r2 = 1.0;
            exprStack[stackindex] = r2;
            break;

        case 31:
            r1 = exprStack[stackindex];
            stackindex--;
            if (stackindex < 0) break;
            r2 = exprStack[stackindex];
            if (r2 <= 0.0) r2 = 0.0;
            else r2 = pow(r2, r1);
            exprStack[stackindex] = r2;
            break;
        }
        node = node->next;
    }
    if (stackindex >= 0)
        r1 = exprStack[stackindex];
    else
        r1 = 0.0;

    // Set result to 0 if it is NaN due to an illegal math op
    if (r1 != r1) r1 = 0.0;

    return r1;
}

// Turn off "precise" floating point option
#pragma float_control(pop)

//=============================================================================

void mathexpr_delete(MathExpr* expr)
{
    if (expr) mathexpr_delete(expr->next);
    free(expr);
}

//=============================================================================

MathExpr* mathexpr_create(char* formula, int (*getVar) (char*))
{
    ExprTree* tree;
    MathExpr* expr = NULL;
    MathExpr* result = NULL;
    getVariableIndex = getVar;
    Err = 0;
    PrevLex = 0;
    CurLex = 0;
    S = formula;
    Len = (int)strlen(S);
    Pos = 0;
    Bc = 0;
    tree = getTree();
    if (Bc == 0 && Err == 0)
    {
        traverseTree(tree, &expr);
        while (expr)
        {
            result = expr;
            expr = expr->prev;
        }
    }
    deleteTree(tree);
    return result;
}


//=============================================================================

char* mathexpr_getStr(MathExpr* expr, char* exprStr,                         
    char* (*getVariableStr) (int, char*))
{
    Term TermStack[50];
    MathExpr* node = expr;
    char r1[MAX_TERM_SIZE], r2[MAX_TERM_SIZE];
    int stackindex = 0;

    strcpy(TermStack[0].s, "");
    while (node != NULL)
    {
        switch (node->opcode)
        {
        case 3:
            strcpy(r1, TermStack[stackindex].s);
            stackindex--;
            strcpy(r2, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "(%s) + (%s)", r2, r1);
            break;

        case 4:
            strcpy(r1, TermStack[stackindex].s);
            stackindex--;
            strcpy(r2, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "(%s) - (%s)", r2, r1);
            break;

        case 5:
            strcpy(r1, TermStack[stackindex].s);
            stackindex--;
            strcpy(r2, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "(%s) * (%s)", r2, r1);
            break;

        case 6:
            strcpy(r1, TermStack[stackindex].s);
            stackindex--;
            strcpy(r2, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "(%s) / (%s)", r2, r1);
            break;

        case 7:
            stackindex++;
            sprintf(TermStack[stackindex].s, "%.6g", node->fvalue);
            break;

        case 8:
            if (getVariableStr != NULL)strcpy(r1, getVariableStr(node->ivar, r2));
            else strcpy(r1, "");
            stackindex++;
            strcpy(TermStack[stackindex].s, r1);
            break;

        case 9:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "-(%s)", r1);
            break;

        case 10:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "cos(%s)", r1);
            break;

        case 11:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "sin(%s)", r1);
            break;

        case 12:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "tan(%s)", r1);
            break;

        case 13:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "cot(%s)", r1);
            break;

        case 14:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "abs(%s)", r1);
            break;

        case 15:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "sgn(%s)", r1);
            break;

        case 16:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "sqrt(%s)", r1);
            break;

        case 17:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "log(%s)", r1);
            break;

        case 18:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "exp(%s)", r1);
            break;

        case 19:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "asin(%s)", r1);
            break;

        case 20:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "acos(%s)", r1);
            break;

        case 21:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "atan(%s)", r1);
            break;

        case 22:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "acot(%s)", r1);
            break;

        case 23:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "sinh(%s)", r1);
            break;

        case 24:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "cosh(%s)", r1);
            break;

        case 25:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "tanh(%s)", r1);
            break;

        case 26:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "coth(%s)", r1);
            break;

        case 27:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "log10(%s)", r1);
            break;

        case 28:
            strcpy(r1, TermStack[stackindex].s);
            sprintf(TermStack[stackindex].s, "step(%s)", r1);
            break;

        case 31:
            strcpy(r1, TermStack[stackindex].s);
            strcpy(r2, TermStack[stackindex - 1].s);
            sprintf(TermStack[stackindex - 1].s, "pow(%s,%s)", r2, r1);
            stackindex--;
            break;
        }
        node = node->next;
    }
    strcpy(exprStr, TermStack[stackindex].s);
    return exprStr;
}
