
class DUT(object):
    '''
    '''
    testSuites = []
    def addTestSuite(self, testSuite):
        '''
        add test suite to DUT
        '''
    
    def deleteTestSuite(self, testSuite):
        '''
        delete test suite from DUT
        1. delete all queue task from this test suite
        2. delete test suite from DUT list
        '''
    
    def runTestSuite(self, testSuite):
        '''
        '''
        
    def runTestCase(self, testCase):
        '''
        '''
        
    def pauseTestSuite(self, testSuite):
        '''
        '''
    
    def queueTask(self, task, priority, type_):
        '''
        Add task to DUT queue
        '''

    def peekTask(self, task=None, type_=None):
        '''
        check task info in DUT queue
        '''
    
    def deleteTask(self, task=None, type_=None):
        '''
        delete task from DUT queue
        '''
    

class Server(object):
    '''
    '''
    DUTs = []
    def addDUT(self, DUT):
        '''
        add DUT to server

        1. add DUT to DUT list
        2. check if DUT reachable
        3. change trust level to 3 for DUT, to allow DUT queue message back
        
        '''
        
    def deleteDUT(self, DUT):
        '''
        delete DUT from server
        1. clear all queue task in DUT from this server
        2. remove DUT from DUT list
        3. delete trust level of DUT
        
        '''
        

