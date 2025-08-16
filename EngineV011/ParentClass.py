'''
class ParentClass():
    def __init__(self):
        self.stringvalue = child.returnChild()
    def printChildClass(self):
        print(self.stringvalue)
        
ParentClass.child.printChildClass()
'''




class ChildClass:
    def __init__(self):
        self.helloworld = "Hello world"  # Make the variable an instance variable
    def returnChild(self):
        return self.helloworld  # Use self to access the instance variable

child = ChildClass()



class ParentClass:
    def __init__(self):
        self.stringvalue = child.returnChild()  # Call the method to get the value
    def printChildClass(self):
        print(self.stringvalue)



parent = ParentClass()

# Call the method to print the value
parent.printChildClass()