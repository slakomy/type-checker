#!/usr/bin/python

from scanner import Scanner
#import AST
from AST import *
from TypeChecker import *
from SymbolTable import *
from TreePrinter import *

class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens
    
    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )
    

    error_encountered = False
    


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input')

    
    
    def p_program(self, p):
        """program : declarations fundefs instructions"""
        
        p[0] = Program(p[1], p[2], p[3])
        #if self.error_encountered == False:
        #    p[0].accept(TypeChecker(), SymbolTable(None))
        p[0].error_encountered = self.error_encountered
    
    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if (len(p) == 3):
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = list()
    
    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """
        if len(p) == 4:
            p[0] = Declaration(p[1], p[2])
        else:
            print "Bad declaration at line", p.lineno(1)
            self.error_encountered = True
            

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        else:
            p[0] = list()
            p[0].append(p[1])


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = Init(p[1], p[3], p.lineno(1))

    
    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = list()
            p[0].append(p[1])
    
    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""
        p[0] = p[1]
    
    
    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """
        if isinstance(p[2], Node):
            p[0] = PrintInstr(p[2])
        else:
            print "Bad expression in print instruction at line", p.lineno(1)
            self.error_encountered = True
    
    
    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = p[3]
        
    
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = Assignment(p[1], p[3], p.lineno(1))
    
    
    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        if isinstance(p[3], Node) == False:
            print "Bad condition in choice instruction at line", p.lineno(1)
            self.error_encountered = True  
        elif len(p) == 6:
            p[0] = ChoiceInstr(p[3], p[5])
        else:
            p[0] = ChoiceInstr(p[3], p[5], p[7])
    
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        if isinstance(p[3], Node) == False:
            print "Bad condition in while instruction at line", p.lineno(1)
            self.error_encountered = True
        else:  
            p[0] = WhileInstr(p[3], p[5])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = RepeatInstr(p[2], p[4])
    
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = RetInstr(p[2])
    
    
    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = ContinueInstr()
    
    
    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = BreakInstr()
    
    
    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """
        p[0] = CompoundInstr(p[2], p[3])

    
    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]


    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        try:
            p[0] = Integer(int(p[1]), p.lineno(1))
        except ValueError:
            try:
                p[0] = Float(float(p[1]), p.lineno(1))
            except ValueError:
                p[0] = String(p[1], p.lineno(1))
        '''
        if isinstance(p[1], int):
            p[0] = Integer(p[1], p.lineno(1))
        elif isinstance(p[1], float):
            p[0] = Float(p[1], p.lineno(1))
        else:
            p[0] = String(p[1], p.lineno(1))
        '''
    
    
    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        
        if len(p) == 5:
            if isinstance(p[3], list):
                p[0] = FunCall(p[1], p[3], p.lineno(1))
            else:
                print "Bad function call at line", p.lineno(1)
                self.error_encountered = True
        elif len(p) == 4 and p[1] == '(':
            if isinstance(p[2], Node) == False:
                print "Bad expression at line", p.lineno(1)
                self.error_encountered = True
            else:  
                p[0] = p[2]
        elif len(p) == 2:
            if type(p[1]) is str:
                p[0] = Variable(p[1], p.lineno(1))
            else:
                p[0] = p[1]
        else:
            p[0] = BinExpr(p[1], p[2], p[3], p.lineno(2))
    
    
    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = list()    
    
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        else:
            p[0] = list()
            p[0].append(p[1])
    
    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """
        if len(p) == 3:
            p[2].append(p[1])
            p[0] = p[2]
        else:
            p[0] = list()        

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = FunDef(p[1], p[2], p[4], p[6], p.lineno(1))
    
    
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 2:
            p[0] = p[1]     #at least one element in list
        else:
            p[0] = list()   #empty list        
    
    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
        if len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        else:
            p[0] = list()
            p[0].append(p[1])
    
    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = Arg(p[1], p[2], p.lineno(1))


    

