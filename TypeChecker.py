#!/usr/bin/python

from SymbolTable import *
from AST import CompoundInstr


class NodeVisitor(object):

    def visit(self, node, sym_table):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, sym_table)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.ttype = self.init_ttype()


    def init_ttype(self):
        res = {}
        for op in ['+', '-', '*', '/']:  
            res[op] = {}
            res[op]['int'] = {}
            res[op]['int']['int'] = 'int'
            res[op]['int']['float'] = 'float'
            res[op]['float'] = {}
            res[op]['float']['int'] = 'float'
            res[op]['float']['float'] = 'float'
    
        res['+']['string'] = {}
        res['*']['string'] = {}
        res['+']['string']['string'] = 'string'
        res['*']['string']['int'] = 'string'
        
        for op in ['>', '>=', '<=', '==', '!=', '<']:
            res[op] = {}
            res[op]['int'] = {}
            res[op]['string'] = {}
            res[op]['string']['string'] = 'int'
            res[op]['int']['int'] = 'int'
        
        res['='] = {}
        res['=']['int'] = {}
        res['=']['float'] = {}
        res['=']['int']['int'] = 'int'
        res['=']['float']['int'] = 'float'
        res['=']['float']['float'] = 'float'
        
        return res


    def get_ttype(self, op, l_operand, r_operand):
        if op not in self.ttype:
            return None
        elif l_operand not in self.ttype[op]:
            return None
        elif r_operand not in self.ttype[op][l_operand]:
            return None
        else:
            return self.ttype[op][l_operand][r_operand]
            

    def visit_Integer(self, node, sym_table):
        return 'int'
        
    def visit_String(self, node, sym_table):
        return 'string'
        
    def visit_Float(self, node, sym_table):
        return 'float'
        
    def visit_Variable(self, node, sym_table):
        var_symbol = sym_table.get(node.value)
        if var_symbol is None:
            print "Line: %d. Variable %s not declared!" % (node.lineno, node.value)
            return None
        return var_symbol.type
        
        
    def visit_PrintInstr(self, node, sym_table):
        node.expr.accept(self, sym_table)
        
    def visit_RetInstr(self, node, sym_table):
        node.expr.accept(self, sym_table)
        
    def visit_BreakInstr(self, node, sym_table):
        pass
        
    def visit_ContinueInstr(self, node, sym_table):
        pass
        
    def visit_RepeatInstr(self, node, sym_table):
        for instr in node.instrs:
            if isinstance(instr, CompoundInstr):
                instr.accept(self, SymbolTable(sym_table)) #CompoundInstr creates new scope
            else:
                instr.accept(self, sym_table)
        node.cond.accept(self, sym_table)
        
    def visit_WhileInstr(self, node, sym_table):
        if isinstance(node.instr, CompoundInstr):
            node.instr.accept(self, SymbolTable(sym_table)) #CompoundInstr creates new scope
        else:
            node.instr.accept(self, sym_table)
        node.cond.accept(self, sym_table)
       
    def visit_ChoiceInstr(self, node, sym_table):
        node.cond.accept(self, sym_table)
        if isinstance(node.if_instr, CompoundInstr):
            node.if_instr.accept(self, SymbolTable(sym_table)) #CompoundInstr creates new scope
        else:
            node.if_instr.accept(self, sym_table)
        if node.else_instr is not None: 
            if isinstance(node.else_instr, CompoundInstr):
                node.else_instr.accept(self, SymbolTable(sym_table)) #CompoundInstr creates new scope
            else:
                node.else_instr.accept(self, sym_table)

    
    def visit_CompoundInstr(self, node, sym_table):
        for decl in node.decls:
            decl.accept(self, sym_table)
        for instr in node.instrs:
            if isinstance(instr, CompoundInstr):
                instr.accept(self, SymbolTable(sym_table)) #CompoundInstr creates new scope
            else:
                instr.accept(self, sym_table)       
    
    
    def visit_FunCall(self, node, sym_table):
        fun_symbol = sym_table.get(node.fun_name)
        if fun_symbol is None:
            print "Line: %d. Function %s is not defined!" % (node.lineno, node.fun_name)
            return None
        if len(node.expr_list) != len(fun_symbol.arg_types):
            print "Line: %d. Function: %s - number of arguments passed inconsistent with declaration!" % (node.lineno, node.fun_name)
            return None
        arg_no = 0
        for expr in node.expr_list:
            arg_no += 1
            type1 = expr.accept(self, sym_table)
            if type1 == 'int' and fun_symbol.arg_types[arg_no - 1] == 'float':  #cast from int to float is allowed
                pass
            elif type1 != fun_symbol.arg_types[arg_no - 1]:
                print "Line: %d. Inconsistent type of %d. argument in %s function call." % (node.lineno, arg_no, node.fun_name)
                print "Found: %s. Required: %s." % (type1, fun_symbol.arg_types[arg_no - 1])
        return fun_symbol.type
                

    def visit_BinExpr(self, node, sym_table):
        type1 = node.left_operand.accept(self, sym_table)
        type2 = node.right_operand.accept(self, sym_table)
        op    = node.operator;
        result_type = self.get_ttype(op, type1, type2)
        if result_type is None:
            print "Line: %d. Binary expression %s %s %s forbidden!" % (node.lineno, type1, op, type2)
        return result_type
        
    def visit_Init(self, node, sym_table):
        type1 = node.expr.accept(self, sym_table)
        if sym_table.get(node.var_name, False) is not None:
            print "Line: %d. Variable name %s already in use in this scope!" % (node.lineno, node.var_name)
            return None
        
        return type1
        
    def visit_Assignment(self, node, sym_table):
        type1 = node.expr.accept(self, sym_table)
        symbol = sym_table.get(node.var_name)
        if symbol is None:
            print "Line: %d. Assignment to nonexisting variable - %s!" % (node.lineno, node.var_name)
            return None
        elif symbol.type != type1:
            print "Line: %d. Types inconsistency. Trying to assign type %s to variable %s defined as %s." % (node.lineno, type1, node.var_name, symbol.type)
            return None
        else:
            return symbol.type
            
 
    def visit_Declaration(self, node, sym_table):
        decl_type = node.decl_type
        for assignment in node.inits:
            type1 = assignment.accept(self, sym_table)
            if type1 != None and type1 != decl_type:
                print "Line: %d. Value assigned to variable %s is inconsistent with declared type" % (assignment.lineno, assignment.var_name)
                print "Przypisano: %s. Wymagano: %s." % (type1, decl_type)
            if type1 != None:
                sym_table.put(assignment.var_name, VariableSymbol(assignment.var_name, decl_type))

                
    
    
    def visit_Arg(self, node, sym_table):
        if sym_table.get(node.arg_name, False) is not None:
            print "Line: %d. Repetition of a variable name %s in function signature!" % (node.lineno, node.arg_name)
        else:
            sym_table.put(node.arg_name, VariableSymbol(node.arg_name, node.arg_type))
        return node.arg_type        
                
    def visit_FunDef(self, node, sym_table):
        local_sym_table = SymbolTable(sym_table)
        arg_types = list()
        for arg in node.args_list:
            arg_types.append(arg.accept(self, local_sym_table))
        if sym_table.get(node.fun_name) is not None:
            print "Line: %d. Already exists symbol with the same name as the one assigned to a function!" % (node.lineno)
        else:
            sym_table.put(node.fun_name, FunctionSymbol(node.fun_name, node.fun_type, arg_types))
        node.compound_instr.accept(self, local_sym_table)
                 
    
    def visit_Program(self, node, sym_table):
        for decl in node.decls:
            decl.accept(self, sym_table)
        for fundef in node.fundefs:
            fundef.accept(self, sym_table)
        for instr in node.instrs:
            instr.accept(self, sym_table)        




