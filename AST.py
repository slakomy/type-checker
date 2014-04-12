#classes defined in this file represent nodes in Abstract Syntax Trees

class Node(object):

    def __str__(self):
        return self.printTree()
    
    def accept(self, visitor, sym_table):
        return visitor.visit(self, sym_table)


class Const(Node):
    
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class Integer(Const):
    
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class Float(Const):

    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class String(Const):
    
    def __init__(self, value, lineno):
        self.value = value 	
        self.lineno = lineno


class Variable(Node):
    
    def __init__(self, value, lineno):
    	self.value = value
    	self.lineno = lineno
    	

class BinExpr(Node):

    
    def __init__(self, left_operand, operator, right_operand, lineno):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator
        self.lineno = lineno
    	

class FunCall(Node):
	
    def __init__(self, fun_name, expr_list, lineno):
        self.fun_name = fun_name
        self.expr_list = expr_list
        self.lineno = lineno
	
	
class PrintInstr(Node):
	
    def __init__(self, expr):
        self.expr = expr

class Program(Node):
	
    def __init__(self, decls, fundefs, instrs):
        self.decls = decls
        self.fundefs = fundefs
        self.instrs = instrs


class Declaration(Node):
	
    def __init__(self, decl_type, inits):
        self.decl_type = decl_type
        self.inits = inits  #assignments

class Init(Node):
    def __init__(self, var_name, expr, lineno):
        self.var_name = var_name
        self.expr = expr
        self.lineno = lineno
		

class Assignment(Node):     
	
    def __init__(self, var_name, expr, lineno):
        self.var_name = var_name
        self.expr = expr
        self.lineno = lineno
		
class FunDef(Node):
    
    def __init__(self, fun_type, fun_name, args_list, compound_instr, lineno):
        self.fun_type = fun_type
        self.fun_name = fun_name
        self.args_list = args_list
        self.compound_instr = compound_instr  
        self.lineno = lineno  

class Arg(Node):
    
    def __init__(self, arg_type, arg_name, lineno):
        self.arg_type = arg_type
        self.arg_name = arg_name
        self.lineno = lineno
        
class CompoundInstr(Node):
    
    def __init__(self, decls, instrs):
        self.decls = decls
        self.instrs = instrs
        
class PrintInstr(Node):
    
    def __init__(self, expr):
        self.expr = expr
        
class RetInstr(Node):
    
    def __init__(self, expr):
        self.expr = expr
        
class BreakInstr(Node):
    pass
    
class ContinueInstr(Node):
    pass
    
class RepeatInstr(Node):
    
    def __init__(self, instrs, cond):
        self.instrs = instrs
        self.cond = cond
        
class WhileInstr(Node):
    
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr
        

class ChoiceInstr(Node):
    
    def __init__(self, cond, if_instr, else_instr = None):
        self.cond = cond
        self.if_instr = if_instr
        self.else_instr = else_instr
		


