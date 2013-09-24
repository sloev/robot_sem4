

class TMCStatus:

    def __init__(self, byte):
        self.slaveAdd = byte[0]
        self.add = byte[1]
        self.current = byte[2]
        self.voltage = byte[3]
        self.stat1 = byte[4]
        self.stat2 = byte[5]
        self.stat3 = byte[6]
        self.NA1 = byte[7]
        self.NA2 = byte[8]
        
    def checkSingleBit(self, byte, pos):
        return str((1 << pos) & byte)
    
    def checkTwoBits(self, byte, pos1, pos2):
        bit1 = (1 << pos1) & byte
        bit2 = (1 << pos2) & byte
        return str(bit1+""+bit2)
        
    def checkThreeBits(self, byte, pos1, pos2, pos3):
        bit1 = (1 << pos1) & byte 
        bit2 = (1 << pos2) & byte
        bit3 = (1 << pos3) & byte
        return str(bit1-""+bit2+""+bit3)
        
    def getSlaveAdd(self):
        temp = hex(self.slaveAdd)
        return temp
    
    def getAdd(self):
        temp = hex(self.add)
        return temp    
    
    def getCurrent(self):
        temp = bin(self.current)
        return temp
        
    def getVoltage(self):
        temp = bin(self.voltage)
        return temp
        
    def getStat1(self):
        temp = bin(self.stat1)
        return temp
    
    def getStat2(self):
        temp = bin (self.stat2)
        return temp
    
    def getStat3(self):
        temp = bin(self.stat3)
        return temp
    
    def toString(self):
        print self.getSlaveAdd()
        print self.getAdd()
        print self.getCurrent()
        print self.getVoltage()
        print self.getStat1()    
        print self.getStat2()
        print self.getStat3()
        
    def printStatus(self):
        pass
        
        
def main():
    test = TMCStatus([0xF1, 0x11, 0xAB, 0xFF, 0x56, 0x23, 0xBB, 0x21, 0xC9])
    test.toString()

if __name__ == "__main__":
    main()    
    
    