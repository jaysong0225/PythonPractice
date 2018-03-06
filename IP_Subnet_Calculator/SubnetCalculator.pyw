import sys, math

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

# ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import SubnetCalculator_Lib

# CHANGE THE SECOND PARAMETER HERE TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, SubnetCalculator_Lib.Ui_MainWindow):

    # declare global variables here
    networkClass = ""

    # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
        # END DO NOT MODIFY

        # ADD SLOTS HERE
        self.pushButton_Calculate.clicked.connect(self.start_calculation)
        self.actionOpen.triggered.connect(self.openFileNameDialog)
        self.actionSave_As.triggered.connect(self.saveFileNameDialog)
        self.actionExit.triggered.connect(self.exitDialog)
        self.actionClear.triggered.connect(self.clearAllData)
        self.actionCalculate.triggered.connect(self.start_calculation)

        # setup form by automatically loading data from file and filling UI list

    # ADD SLOT FUNCTIONS HERE
    def validate_input_value(self, ipAddress, numberOfHostsPerSubnet):
        ipAddrList = ipAddress.split(".")
        error = 0
        if len(ipAddrList) != 4:
            error = 1
        else:
            for bitBlock in ipAddrList:
                if not bitBlock.isdigit():
                    error = 1
                else:
                    if int(bitBlock) > 255:
                        error = 1
        if not numberOfHostsPerSubnet.isdigit():
            error = 2
        return error

    def start_calculation(self):
        # Get user inputs (network address, number of needed usable hosts)
        networkAddress = self.lineEdit_NetworkAddress.text()
        numOfHostPerSubnet = self.lineEdit_HostsPerSubnet.text()

        # Validate the network IP Address, number of hosts
        error = self.validate_input_value(networkAddress, numOfHostPerSubnet)

        # If the previous validation process found an error, display popup message
        if error == 1:
            # Not a valid address
            QMessageBox.critical(self, 'Invalid Data', 'Network Address must be a valid IPv4 address', QMessageBox.Ok)
        elif error == 2:
            # Not a valid input host numbers
            QMessageBox.critical(self, 'Invalid Data', 'Number of hosts must be a valid number', QMessageBox.Ok)
        else:
            # If no error detected, proceed subnet calculation
            # Call sub-functions for the subnet calculation
            subnetSize = self.CalculateSubnetSize(numOfHostPerSubnet)
            decimalOctects = self.CalculateDecimalOctects(networkAddress)
            decimalAddress = self.CalculateDecimalAddress(networkAddress)
            binaryAddress = self.CalculateBinaryAddress(networkAddress)
            hexAddress = self.CalculateHexAddress(networkAddress)
            self.networkClass = self.CalculateNetworkClass(networkAddress)
            numOfIpAddresses = self.CalculateNumberOfIPAddresses(networkAddress)
            subnetMask = self.CalculateSubnetMask(subnetSize)
            binarySubnetMask = self.CalculateBinaryMask(subnetSize)
            numOfSubnet = self.CalculateNumberOfSubnets(subnetSize)
            # Check the input IP address and numOfHost are valid
            if self.networkClass == '-1':
                # Not a valid address
                QMessageBox.critical(self, 'Invalid Data', 'Network Address must be a valid address', QMessageBox.Ok)
            elif numOfSubnet == 0:
                QMessageBox.critical(self, 'Invalid Data',
                                     'Number of hosts required is too big for the Network Class of IP Address',
                                     QMessageBox.Ok)
            else:
                self.listWidgetIpRanges.clear()
                usableIpList = self.CalculateSubnetList(networkAddress, numOfSubnet)
                # Check the range of the number of subnet
                self.lineEdit_CalculatedSubnetSize.setText(str(subnetSize))
                self.lineEdit_DecimalOctets.setText(decimalOctects)
                self.lineEdit_DecimalAddress.setText(str(decimalAddress))
                self.lineEdit_BinaryOctets.setText(binaryAddress)
                self.lineEdit_HexOctects.setText(hexAddress)
                self.lineEdit_NetworkClass.setText(self.networkClass)
                self.lineEdit_NumIP_Addresses.setText(str(numOfIpAddresses))
                self.lineEdit_SubnetMask.setText(subnetMask)
                self.lineEdit_BinaryMask.setText(binarySubnetMask)
                self.lineEdit_NumOfSubnets.setText(str(numOfSubnet))
                for index in range(numOfSubnet):
                    self.listWidgetIpRanges.addItem(usableIpList[index])

    def openFileNameDialog(self):
        # Get the file full path
        fileName = QFileDialog.getOpenFileName(self, "Open", "./SubnetCalculator_Demo", "Text Files (*.txt)")
        tempList = []
        # Get the data
        with open(fileName[0], "r") as myFile:
            for line in myFile:
                tempList.append(line[:-1])
        myFile.close()
        # Update with the data
        index = 0
        for data in tempList:
            if index == 0:
                self.lineEdit_NetworkAddress.setText(data)
            elif index == 1:
                self.lineEdit_HostsPerSubnet.setText(data)
            elif index == 2:
                self.lineEdit_CalculatedSubnetSize.setText(data)
            elif index == 3:
                self.lineEdit_DecimalOctets.setText(data)
            elif index == 4:
                self.lineEdit_DecimalAddress.setText(data)
            elif index == 5:
                self.lineEdit_BinaryOctets.setText(data)
            elif index == 6:
                self.lineEdit_HexOctects.setText(data)
            elif index == 7:
                self.lineEdit_NetworkClass.setText(data)
            elif index == 8:
                self.lineEdit_NumIP_Addresses.setText(data)
            elif index == 9:
                self.lineEdit_SubnetMask.setText(data)
            elif index == 10:
                self.lineEdit_BinaryMask.setText(data)
            elif index == 11:
                self.lineEdit_NumOfSubnets.setText(data)
            else:
                self.listWidgetIpRanges.addItem(data)
            index += 1

    def saveFileNameDialog(self):
        # Get the target file full path
        fileName = QFileDialog.getSaveFileName(self, "Save As", "./SubnetCalculator_Demo", "*.txt")
        list = []
        with open(fileName[0], "w") as myFile:
            myFile.write(self.lineEdit_NetworkAddress.text() + "\n")
            myFile.write(self.lineEdit_HostsPerSubnet.text() + "\n")
            myFile.write(self.lineEdit_CalculatedSubnetSize.text() + "\n")
            myFile.write(self.lineEdit_DecimalOctets.text() + "\n")
            myFile.write(self.lineEdit_DecimalAddress.text() + "\n")
            myFile.write(self.lineEdit_BinaryOctets.text() + "\n")
            myFile.write(self.lineEdit_HexOctects.text() + "\n")
            myFile.write(self.lineEdit_NetworkClass.text() + "\n")
            myFile.write(self.lineEdit_NumIP_Addresses.text() + "\n")
            myFile.write(self.lineEdit_SubnetMask.text() + "\n")
            myFile.write(self.lineEdit_BinaryMask.text() + "\n")
            myFile.write(self.lineEdit_NumOfSubnets.text() + "\n")
            for index in range(self.listWidgetIpRanges.count()):
                myFile.write(self.listWidgetIpRanges.item(index).text() + "\n")
        myFile.close()

    def exitDialog(self):
        quit_msg = "Exit Program?"
        reply = QMessageBox.question(self, 'Exit',
                                     quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.closeAllWindows()

    def clearAllData(self):
        self.lineEdit_NetworkAddress.clear()
        self.lineEdit_HostsPerSubnet.clear()
        self.lineEdit_CalculatedSubnetSize.clear()
        self.lineEdit_DecimalOctets.clear()
        self.lineEdit_DecimalAddress.clear()
        self.lineEdit_BinaryOctets.clear()
        self.lineEdit_HexOctects.clear()
        self.lineEdit_NetworkClass.clear()
        self.lineEdit_NumIP_Addresses.clear()
        self.lineEdit_SubnetMask.clear()
        self.lineEdit_BinaryMask.clear()
        self.lineEdit_NumOfSubnets.clear()
        self.listWidgetIpRanges.clear()

    # ADD HELPER FUNCTIONS HERE
    def CalculateSubnetSize(self, numberOfHostsPerSubnet):
        index = 1
        while True:
            num_of_usable_addresses = pow(2, index) - 2
            if num_of_usable_addresses >= int(numberOfHostsPerSubnet):
                break
            else:
                index += 1
        total_num_of_host_addresses = num_of_usable_addresses + 2
        return total_num_of_host_addresses

    def CalculateDecimalOctects(self, ipAddress):
        return ipAddress

    def CalculateDecimalAddress(self, ipAddress):
        ipAddrList = ipAddress.split(".")
        decimalAddr = (int(ipAddrList[0]) * pow(256, 3)) + (int(ipAddrList[1]) * pow(256, 2)) + \
                      (int(ipAddrList[2]) * pow(256, 1)) + (int(ipAddrList[3]) * pow(256, 0))
        return decimalAddr

    def CalculateBinaryAddress(self, ipAddress):
        ipAddrList = ipAddress.split(".")
        ipAddrBinaryList = []
        for data in ipAddrList:
            binaryValue = bin(int(data))[2:].zfill(8)
            ipAddrBinaryList.append(binaryValue)
        return ".".join(ipAddrBinaryList)

    def CalculateHexAddress(self, ipAddress):
        ipAddrList = ipAddress.split(".")
        ipAddrHexList = []
        for data in ipAddrList:
            hexValue = hex(int(data))[2:].zfill(2)
            ipAddrHexList.append(hexValue.upper())
        return ".".join(ipAddrHexList)

    def CalculateNetworkClass(self, ipAddress):
        ipAddrList = ipAddress.split(".")
        binaryValue = bin(int(ipAddrList[0]))[2:].zfill(8)
        zeroIndex = binaryValue.find("0")
        if zeroIndex == 0:
            if ipAddrList[1] == '0' and ipAddrList[2] == '0' and ipAddrList[3] == '0':
                return "A"
            else:
                return "-1"
        elif zeroIndex == 1:
            if ipAddrList[2] == '0' and ipAddrList[3] == '0':
                return "B"
            else:
                return "-1"
        elif zeroIndex == 2:
            if ipAddrList[3] == '0':
                return "C"
            else:
                return "-1"
        else:
            return "-1"   # Error Occurred

    def CalculateNumberOfIPAddresses(self, networkIPAddress):
        net_Class = self.CalculateNetworkClass(networkIPAddress)

        if net_Class == "A":
            return pow(2, 24)
        elif net_Class == "B":
            return pow(2, 16)
        elif net_Class == "C":
            return pow(2, 8)
        else:
            return -1

    def CalculateSubnetMask(self, numberOfHostsPerSubnet):
        subnetMask = ""
        subnetMaskList = []
        bitLength = len(bin(numberOfHostsPerSubnet)[2:]) - 1
        for index in range(32 - bitLength):
            subnetMask += '1'
        for index in range(bitLength):
            subnetMask += '0'
        a = len(subnetMask)
        for index in range(4):
            num = int(('0b' + subnetMask[index*8:(index*8)+8]), 2)
            subnetMaskList.append(str(num))

        subnetMask = ".".join(subnetMaskList) + " /" + str(32 - bitLength)
        return subnetMask

    def CalculateBinaryMask(self, numberOfHostsPerSubnet):
        bitLength = len(bin(numberOfHostsPerSubnet)[2:]) - 1
        binarySubnetMask = ""
        for index in range(31, -1, -1):
            if index > (bitLength-1):
                binarySubnetMask += "1"
            else:
                binarySubnetMask += "0"
            if (index % 8) == 0 and index != 0:
                binarySubnetMask += "."
        return binarySubnetMask

    def CalculateNumberOfSubnets(self, calculatedSubnetSize):
        # example)             |/DSM   |/CSM
        #           192.168.0. | x x x |x x x x x
        IPv4_bit_size = 32      # 4 bytes * 4
        hostBitLength = len(bin(calculatedSubnetSize)[2:]) - 1

        if self.networkClass == 'A':
            subnetBitLength = IPv4_bit_size - 8 - hostBitLength
        elif self.networkClass == 'B':
            subnetBitLength = IPv4_bit_size - 16 - hostBitLength
        else:
            subnetBitLength = IPv4_bit_size - 24 - hostBitLength

        if subnetBitLength > 0:
            num_subnet = pow(2, subnetBitLength)
        else:
            num_subnet = 0
        return num_subnet

    def CalculateSubnetList(self, ipAddress, numOfSubnet):
        # example)             |/DSM   |/CSM
        #           192.168.0. | x x x |x x x x x
        #                      | 0 0 0 |0 0 0 0 0
        #                      | 0 0 1 |1 1 1 1 1
        #                      | 0 1 0 |
        usableAddrList = []
        networkAddress = ipAddress.split(".")
        subnetBitLength = len(bin(numOfSubnet)[2:]) - 1
        error = 0
        # define bypass, range value
        if self.networkClass == 'A':
            bypass = 1
            bitRange = 24
        elif self.networkClass == 'B':
            bypass = 2
            bitRange = 16
        else:
            bypass = 3
            bitRange = 8

        # Calculate usable address list (binary)
        for subnet in range(numOfSubnet):
            # Initialize the usable address
            firstUsableAddress = []
            lastUsableAddress = []
            # Add bypass bit Blocks depending the network Class
            for index in range(bypass):
                firstUsableAddress.append(networkAddress[index])
                lastUsableAddress.append(networkAddress[index])
            # Calculate non-bypass bit Blocks
            firstBitBlock = str(bin(subnet)[2:])
            lastBitBlock = str(bin(subnet)[2:])
            firstBitBlock = firstBitBlock.zfill(subnetBitLength)
            lastBitBlock = lastBitBlock.zfill(subnetBitLength)
            for host in range(bitRange - subnetBitLength):
                firstBitBlock += '0'
                lastBitBlock += '1'
            # Binary to Decimal conversion
            for index in range(4 - bypass):
                firstBit = index * 8
                lastBit = firstBit + 8
                tempFirstByte = int(("0b" + firstBitBlock[firstBit:lastBit]), 2)
                tempLastByte = int(("0b" + lastBitBlock[firstBit:lastBit]), 2)
                firstUsableAddress.append(str(tempFirstByte))
                lastUsableAddress.append(str(tempLastByte))
            usableAddrList.append(".".join(firstUsableAddress) + " - " + ".".join(lastUsableAddress))

        return usableAddrList

# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY
