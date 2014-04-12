import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

level = 0
    
def printLevel():
    global level
    for num in range(0, level):
        print '|',

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self):
        global level
        printLevel(),
        print self.operator
        level = level + 1
        self.left_operand.printTree()
        self.right_operand.printTree()
        level = level - 1


    @addToClass(AST.Assignment)
    @addToClass(AST.Init)
    def printTree(self):
        global level
        printLevel(), 
        print '='
        level = level + 1
        printLevel(),
        print self.var_name
        self.expr.printTree()
        level = level - 1
        
    @addToClass(AST.Declaration)
    def printTree(self):
        global level
        printLevel(),
        print "DECL"
        level = level + 1
        for init in self.inits:
        	init.printTree()
        level = level - 1
       
    @addToClass(AST.FunDef)    
    def printTree(self):
        global level
        printLevel(),
        print "FUNDEF"
        
        level = level + 1
        printLevel(),
        print self.fun_name
        
        printLevel(),
        print "RET", 
        print self.fun_type
        
        for arg in self.args_list:
            arg.printTree()
        self.compound_instr.printTree()
        level = level - 1
        
    @addToClass(AST.Arg)
    def printTree(self):
        printLevel(),
        print "ARG",
        print self.arg_name        
        
    
    @addToClass(AST.CompoundInstr)
    def printTree(self):
        for decl in self.decls:
            decl.printTree()
        for instr in self.instrs:
            instr.printTree()
            
            
    @addToClass(AST.PrintInstr)
    def printTree(self):
        global level
        printLevel(),
        print "PRINT"
        level = level + 1
        self.expr.printTree()
        level = level - 1
    
    
    @addToClass(AST.RetInstr)
    def printTree(self):
        global level
        printLevel(),
        print "RETURN"
        level = level + 1
        self.expr.printTree()
        level = level - 1
        
        
    @addToClass(AST.Program)
    def printTree(self):
        for decl in self.decls:
            decl.printTree()
        for fundef in self.fundefs:
            fundef.printTree()
        for instr in self.instrs:
            instr.printTree()
        
        
    @addToClass(AST.Variable)
    def printTree(self):
        printLevel(),
        print self.value
        
    
    @addToClass(AST.Const)
    def printTree(self):
        printLevel(),
        print self.value
    
    
    @addToClass(AST.BreakInstr)
    def printTree(self):
        printLevel(),
        print "BREAK"
        
        
    @addToClass(AST.ContinueInstr)
    def printTree(self):
        printLevel(),
        print "CONTINUE"
        
    @addToClass(AST.RepeatInstr)
    def printTree(self):
        global level
        printLevel(),
        print "REPEAT"
        level = level + 1
        for instr in self.instrs:
            instr.printTree()
        level = level - 1
        printLevel(),
        print "UNTIL"
        level = level + 1
        self.cond.printTree()
        level = level - 1
        
        
    @addToClass(AST.FunCall)
    def printTree(self):
        global level
        printLevel(),
        print "FUNCALL"
        level = level + 1
        
        printLevel(),
        print self.fun_name
        for expr in self.expr_list:
            expr.printTree()
        level = level - 1
        
    @addToClass(AST.WhileInstr)
    def printTree(self):
        global level
        printLevel(),
        print "WHILE"
        level = level + 1
        self.cond.printTree()
        self.instr.printTree()
        level = level - 1
        
    @addToClass(AST.ChoiceInstr)
    def printTree(self):
        global level
        printLevel(),
        print "IF"
        level = level + 1
        self.cond.printTree()
        self.if_instr.printTree()
        level = level -1
        if (self.else_instr):
            printLevel(),
            print "ELSE"
            level = level + 1
            self.else_instr.printTree()
            level = level - 1
        
        
