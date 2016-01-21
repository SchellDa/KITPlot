import numpy as np
import ROOT
import os, sys
import ConfigParser
import KITDataFile

class KITPlot(object):

    __kitGreen = []
    __kitBlue = []
    __kitMay = []
    __kitYellow = []
    __kitOrange = []
    __kitBrown = []
    __kitRed = []
    __kitPurple = []
    __kitCyan = []

    __init = False
    __color = 0
    
    def __init__(self, input=None):
        
        self.cfgFile=None
        self.fileInput = False
        
        # init colors and markers
        if self.__init == False:
            self.__initColor()
            self.markerSet = [22,21,20,26,25,24]
        else:
            pass
        
        # check if cfgFile exists
        self.cfg_exists = self.__check_cfg(None)
        
        # if cfg path is given, check if correct and write into self.cfgFile
        if len(sys.argv) > 2:
            self.cfg_path = sys.argv[2]
            self.cfg_exists = self.__check_cfg(self.cfg_path)
            if self.cfg_exists == False:
                print "No .cfg found! Need valid path!"

        # load cfg if present
        if self.cfgFile is not None:
            if os.path.isfile(self.cfgFile):
                self.__initCfg(self.cfgFile)
                print "Found cfg!"
        else:
            self.__initDefaultValues()
            print "Use default values!"

        self.__initStyle()
        self.__file = []
        self.__graphs = []
        
        # Load KITDataFile
        if isinstance(input, KITDataFile.KITDataFile):
            self.__file.append(input)
            self.addGraph(input.getX(),input.getY())

        # Load single PID
        elif isinstance(input, int):
            self.__file.append(KITDataFile.KITDataFile(input))
            self.addGraph(self.__file[0].getX(), self.__file[0].getY())
          
        elif isinstance(input, str):

            # Load single PID
            if input.isdigit():
                self.__file.append(KITDataFile.KITDataFile(input))
                self.addGraph(self.__file[0].getX(), self.__file[0].getY())
            
            # Load multiple data files in a folder
            elif os.path.isdir(input):
                print input
                self.fileInput = True
                for inputFile in os.listdir(input):
                    if (os.path.splitext(inputFile)[1] == ".txt"):
                        self.__file.append(KITDataFile.KITDataFile(input + inputFile))
                        self.addGraph(self.__file[-1].getX(),self.__file[-1].getY())
#
# If you open the file the data type changes from str to file 
#
#                        with open(input + file) as inputFile:
#                            self.__file.append(KITDataFile.KITDataFile(inputFile))
#                            self.addGraph(self.__file[-1].getX(),self.__file[-1].getY())
                        
                    else:
                        pass

            # Load file with multiple PIDs
            elif os.path.isfile(input):
                if self.__checkPID(input) == True:
                    with open(input) as inputFile:
                        for i, line in enumerate(inputFile):
                            entry = line.split()
                            if entry[0].isdigit():
                                self.__file.append(KITDataFile.KITDataFile(entry[0]))
                    for i, File in enumerate(self.__file):
                        self.arrangeFileList()
                        self.addGraph(self.__file[i].getX(),self.__file[i].getY())
                else:
                    self.__file.append(KITDataFile.KITDataFile(input))
                    self.addGraph(self.__file[-1].getX(),self.__file[-1].getY())
        
        # create cfg file if it doesnt exist
        if self.cfg_exists == False:
            self.__writeCfg(self.cfgFile)

        

######################
### Default values ###
######################
     
    def __initDefaultValues(self):
        
        # Title options 
        self.title = "auto"
        self.titleX0 = 0.5
        self.titleY0 = 0.97
        self.titleH = 0.05

        # XAxis
        self.titleX = "px"
        self.titleSizeX = 0.05
        self.titleOffsetX = 1.1
        self.labelSizeX = 0.04
        self.absX = True
        self.logX = False
        self.rangeX = "auto"

        # YAxis
        self.titleY = "py"
        self.titleSizeY = 0.05
        self.titleOffsetY = 1.1
        self.labelSizeY = 0.04
        self.absY = True
        self.logY = False
        self.rangeY = "auto"
        
        # Legend
        self.legendEntry = "name" # name / id
        self.TopRight = True
        self.TopLeft = False
        self.BottomRight = False
        
        # Misc
        self.padBottomMargin = 0.15
        self.padLeftMargin = 0.15
        self.markerSize = 1.5
        self.markerStyle = 22
        self.markerColor = 1100

        # More plot options
        self.GraphGroup = True
        self.FluenzGroup = False
        self.NameGroup = True
        
        
###################
### cfg methods ###
###################


    def __initCfg(self, fileName):
        
        cfgPrs = ConfigParser.ConfigParser()

        cfgPrs.read(fileName)
            
        self.title = cfgPrs.get('Title', 'title')
        self.titleX0 = cfgPrs.getfloat('Title', 'x0')
        self.titleY0 = cfgPrs.getfloat('Title', 'Y0')
        self.titleH = cfgPrs.getfloat('Title', 'height')

        self.titleX = cfgPrs.get('XAxis', 'title')
        self.titleSizeX = cfgPrs.getfloat('XAxis', 'titleSize')
        self.titleOffsetX = cfgPrs.getfloat('XAxis', 'titleOffset')
        self.labelSizeX = cfgPrs.getfloat('XAxis', 'labelsize')
        self.absX = cfgPrs.getboolean('XAxis', 'absolute')
        self.logX = cfgPrs.getboolean('XAxis', 'log')
        self.rangeX = cfgPrs.get('XAxis', 'xrange')

        self.titleY = cfgPrs.get('YAxis', 'title')
        self.titleSizeY = cfgPrs.getfloat('YAxis', 'titleSize')
        self.titleOffsetY = cfgPrs.getfloat('YAxis', 'titleOffset')
        self.labelSizeY = cfgPrs.getfloat('YAxis', 'labelsize')
        self.absY = cfgPrs.getboolean('YAxis', 'absolute')
        self.logY = cfgPrs.getboolean('YAxis', 'log')
        self.rangeY = cfgPrs.get('YAxis', 'yrange')

        self.legendEntry = cfgPrs.get('Legend', 'entry')
        self.TopRight = cfgPrs.getboolean('Legend', 'top right position')
        self.TopLeft = cfgPrs.getboolean('Legend', 'top left position')
        self.BottomRight = cfgPrs.getboolean('Legend', 'bottom right position')

        self.padBottomMargin = cfgPrs.getfloat('Misc', 'pad bottom margin')
        self.padLeftMargin = cfgPrs.getfloat('Misc', 'pad left margin')
        self.markerSize = cfgPrs.getfloat('Misc', 'marker size')
        self.markerStyle = cfgPrs.getint('Misc', 'marker style')
        self.markerColor = cfgPrs.getint('Misc', 'marker color')

        self.GraphGroup = cfgPrs.getboolean('More plot options', 'graph group')
        self.FluenzGroup = cfgPrs.getboolean('More plot options', 'fluenz group')
        self.NameGroup = cfgPrs.getboolean('More plot options', 'name group')

    def __writeCfg(self, fileName):
        
        cfgPrs = ConfigParser.ConfigParser()

        if not os.path.exists("cfg"):
            os.makedirs("cfg")
        
        if fileName is None:
            #if self.__file[0].getID() is not None:
                #fileName = ("cfg/%s.cfg" %(self.__file[0].getID()))
            #else:
            fileName = "cfg/plot.cfg"
        else:
            pass

        with open(fileName,'w') as self.cfgFile:
            cfgPrs.add_section('Global')

            cfgPrs.add_section('Title')
            cfgPrs.set('Title', 'Title', self.title)
            cfgPrs.set('Title', 'X0', self.titleX0)
            cfgPrs.set('Title', 'Y0', self.titleY0)
            cfgPrs.set('Title', 'Height', self.titleH)

            cfgPrs.add_section('XAxis')
            cfgPrs.set('XAxis', 'Title', self.titleX)
            cfgPrs.set('XAxis', 'TitleOffset', self.titleOffsetX)
            cfgPrs.set('XAxis', 'TitleSize', self.titleSizeX)
            cfgPrs.set('XAxis', 'Labelsize', self.labelSizeX)
            cfgPrs.set('XAxis', 'Absolute', self.absX)
            cfgPrs.set('XAxis', 'Log', self.logX)
            cfgPrs.set('XAxis', 'xRange', self.rangeX)

            cfgPrs.add_section('YAxis')
            cfgPrs.set('YAxis', 'Title', self.titleY)
            cfgPrs.set('YAxis', 'TitleOffset', self.titleOffsetY)
            cfgPrs.set('YAxis', 'TitleSize', self.titleSizeY)
            cfgPrs.set('YAxis', 'Labelsize', self.labelSizeY)
            cfgPrs.set('YAxis', 'Absolute', self.absY)
            cfgPrs.set('YAxis', 'Log', self.logY)
            cfgPrs.set('YAxis', 'yrange', self.rangeY)

            cfgPrs.add_section('Legend')
            cfgPrs.set('Legend', 'Entry', self.legendEntry)
            cfgPrs.set('Legend', 'top right position', self.TopRight)
            cfgPrs.set('Legend', 'top left position', self.TopLeft)
            cfgPrs.set('Legend', 'bottom right position', self.BottomRight)
       
            cfgPrs.add_section('Misc')
            cfgPrs.set('Misc', 'pad bottom margin', self.padBottomMargin)
            cfgPrs.set('Misc', 'pad left margin', self.padLeftMargin)
            cfgPrs.set('Misc', 'marker size', self.markerSize)
            cfgPrs.set('Misc', 'marker style', self.markerStyle)
            cfgPrs.set('Misc', 'marker color', self.markerColor)
            
            cfgPrs.add_section('More plot options')
            cfgPrs.set('More plot options', 'graph group', self.GraphGroup)
            cfgPrs.set('More plot options', 'fluenz group', self.FluenzGroup)
            cfgPrs.set('More plot options', 'name group', self.NameGroup)

            cfgPrs.write(self.cfgFile)

        print ("Wrote %s" %(fileName))
        

##############
### Checks ###
##############

    def MeasurementType(self):
    
        self.MT = self.__file[0].getParaY()
        if self.MT == "I_tot":
            self.autotitle = "Current Voltage characteristics" 
            self.autotitleY = "Current (A)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "Pinhole":
            self.autotitle = "Pinhole leakage" 
            self.autotitleY = "Current (A)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "I_leak_dc":
            self.autotitle = "Interstrip current leakage" 
            self.autotitleY = "Current (A)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "C_tot":
            self.autotitle = "Capacitance Voltage characteristics" 
            self.autotitleY = "Capacitance (F)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "C_int":
            self.autotitle = "Interstrip capacitance measurement" 
            self.autotitleY = "Capacitance (F)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "CC":
            self.autotitle = "Coupling capacitance measurement" 
            self.autotitleY = "Capacitance (F)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "R_int":
            self.autotitle = "Interstrip resistance measurement" 
            self.autotitleY = "Resistance (#Omega)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "R_poly":
            self.autotitle = "Strip resistance measurement" 
            self.autotitleY = "Resistance (#Omega)"
            self.autotitleX = "Voltage (V)"
            
        if len(self.__file) >= 2 and self.fileInput == False:
            if self.__file[0].getParaY() != self.__file[1].getParaY():
                sys.exit("Measurement types are not equal!")
        
        if self.fileInput == True:
            self.autotitle = "Title" 
            self.autotitleY = "Y Value"
            self.autotitleX = "X Value"

    def __checkPID(self, input):
        
        if os.path.isfile(input):
            with open(input) as inputFile:
                if len(inputFile.readline().split()) == 1:
                    return True
                else:
                    return False
                    
    #def __checkFiles(self, arg):
                
    #    if os.path.isdir(input):
    #        return True
    #    else:
    #        return False
                
    
    def __check_cfg(self, arg):
        
        if arg == None:
            file_path = os.getcwd() + "/cfg"
            if os.path.exists(file_path) == False:
                return False
            else:
                if os.listdir(file_path) != [] and os.path.splitext(os.listdir(file_path)[0])[1] == ".cfg":
                    self.cfgFile = "cfg/" + os.listdir(file_path)[0]
                    return True
                if os.listdir(file_path) == [] or os.path.splitext(os.listdir(file_path)[0])[1] != ".cfg":
                    return False
            
        if arg != None:
            if os.path.exists(arg) == False:
                return False
            else:
                self.cfgFile = arg
                return True




#####################
### Graph methods ###
#####################

    
    def __initStyle(self):

        # Title options
        ROOT.gStyle.SetTitleX(self.titleX0)
        ROOT.gStyle.SetTitleY(self.titleY0)
        ROOT.gStyle.SetTitleH(self.titleH)

        # Axis Options
        ROOT.gStyle.SetTitleSize(self.titleSizeX,"X")
        ROOT.gStyle.SetTitleSize(self.titleSizeY,"Y")
        ROOT.gStyle.SetTitleOffset(self.titleOffsetX,"X")
        ROOT.gStyle.SetTitleOffset(self.titleOffsetY,"Y")
        
        ROOT.gStyle.SetLabelSize(self.labelSizeX,"X")
        ROOT.gStyle.SetLabelSize(self.labelSizeY,"Y")
        
        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(self.padBottomMargin)
        ROOT.gStyle.SetPadLeftMargin(self.padLeftMargin)
        
        # Marker Options
        ROOT.gStyle.SetMarkerSize(self.markerSize)
        ROOT.gStyle.SetMarkerStyle(self.markerStyle)
        ROOT.gStyle.SetMarkerColor(self.markerColor)

        # Pad Options
        ROOT.gStyle.SetPadGridX(True)
        ROOT.gStyle.SetPadGridY(True)

        KITPlot.__init = True
        return True


    def addGraph(self, *args):
        
        # args: x, y or KITDataFile

        if isinstance(args[0], KITDataFile.KITDataFile):

            self.__file.append(args[0])
            
            if self.absX:
                x = np.absolute(args[0].getX())
            else:
                x = args[0].getX()
            
            if self.absY:
                if str(args[1]) == "y":
                    y = np.absolute(args[0].getY())
                elif str(args[1]) == "z":
                    y = np.absolute(args[0].getZ())
            else:
                if args[1] == "y":
                    y = args[0].getY()
                elif args[1] == "z":
                    y = args[0].getZ()
                
        elif len(args) == 2 and not isinstance(args[0], KITDataFile.KITDataFile):
            
            if self.absX:
                x = np.absolute(args[0])
            else:
                x = args[0]
            
            if self.absY:
                y = np.absolute(args[1])
            else:
                y = args[1]
        else:
            sys.exit("Cant add graph")
        
        self.__graphs.append(ROOT.TGraph(len(x),np.asarray(x),np.asarray(y)))

        return True
            
                        
    def Draw(self, arg="AP"):

        self.canvas = ROOT.TCanvas("c1","c1",1280,768)
        self.canvas.cd()

        self.__autoScaling()
        self.MeasurementType()
            
        self.plotStyles(self.titleX, self.titleY, self.title)

        if self.logX:
            self.canvas.SetLogx()
        if self.logY:
            self.canvas.SetLogy()

        for n,graph in enumerate(self.__graphs):
            if n==0:
                graph.Draw(arg)
            else:
                graph.Draw(arg.replace("A","") + "SAME")
        
        self.setLegendParameters()
        self.setLegend()

        self.canvas.Update()

        return True

    def update(self):
        
        try:
            self.canvas.Update()
        except:
            pass
        

    def plotStyles(self, XTitle, YTitle, Title):
        
        self.__graphs[0].GetXaxis().SetTitle(XTitle)
        self.__graphs[0].GetYaxis().SetTitle(YTitle)
        self.__graphs[0].SetTitle(Title)
        if self.titleX == "auto":
            self.__graphs[0].GetXaxis().SetTitle(self.autotitleX)
        if self.titleY == "auto":
            self.__graphs[0].GetYaxis().SetTitle(self.autotitleY)
        if self.title == "auto":
            self.__graphs[0].SetTitle(self.autotitle)
        
        if self.rangeX == "auto":
            self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[1])
        if self.rangeY == "auto":
            self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[2],self.Scale[3])
        if self.rangeX != "auto" and ":" in self.rangeX:
            RangeListX = self.rangeX.split(":")
            self.__graphs[0].GetXaxis().SetRangeUser(float(RangeListX[0]),float(RangeListX[1]))
        if self.rangeY != "auto" and ":" in self.rangeY:
            RangeListY = self.rangeY.split(":")
            self.__graphs[0].GetYaxis().SetRangeUser(float(RangeListY[0]),float(RangeListY[1]))
        if self.rangeX != "auto" or self.rangeY != "auto":
            if not ":" in self.rangeX or ":" in self.rangeY: 
                sys.exit("Invalid X-axis range! Try 'auto' or 'float:float'!")
        
        self.counter = 0
        for i, graph in enumerate(self.__graphs):
            graph.SetMarkerColor(self.getColor())
            if self.GraphGroup == False:
                graph.SetMarkerStyle(self.getMarkerStyle(i))

        if self.GraphGroup == True:
            self.setGroup()
            if self.NameGroup == True:
                for i, Name in enumerate(self.__file):
                    for j, Element in enumerate(self.GroupList):
                        if Name.getName()[:5] == Element:
                            self.__graphs[i].SetMarkerStyle(self.markerSet[0+j])
        
        return True
        
    def arrangeFileList(self):

        TempList1 = []
        TempList2 = []
        IndexList = []
        for i, temp in enumerate(self.__file):
            TempList1.append(temp.getName()[:5])
        for i, temp in enumerate(TempList1):
            if temp not in TempList2:
                TempList2.append(temp)
                
        for i, temp1 in enumerate(TempList1):
            for j, temp2 in enumerate(TempList2):
                if temp1 == temp2:
                    IndexList.append(j)
        
        TempList1[:] = []
        max_index = 0
        for Index in IndexList:
            if Index > max_index:
                max_index = Index
        for Index in range(max_index+1):
            for i, File in enumerate(self.__file):
                if Index == IndexList[i]:
                    TempList1.append(File)
        self.__file = TempList1

#######################
### Automatizations ###
#######################

    def __autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]

        self.perc = 0.05
        ListX = [0]
        ListY = [0]

        for file in self.__file:
            ListX += file.getX()
            ListY += file.getY()

        if self.absX:
            ListX = np.absolute(ListX)
        if self.absY:
            ListY = np.absolute(ListY)
        
        # Find points that are 10000% off
        #for point in ListY:
        #    if point > 100*sum(ListY)/float(len(ListY)) and point != 0:
        #        point = 0
            
        self.Scale = []

        self.xmax = max(ListX)
           # if min(line) < self.xmin:
        self.xmin = min(ListX)
        self.ymax = max(ListY)
           # if min(line) < self.xmin:
        self.ymin = min(ListY)
        
        self.Scale.append(self.xmin*(1.-self.perc))
        self.Scale.append(self.xmax*(1.+self.perc))
        self.Scale.append(self.ymin*(1.-self.perc))
        self.Scale.append(self.ymax*(1.+self.perc))
        
        if (self.Scale[2]/self.Scale[3]) > 1e-4:
            self.logY = True

        return True


###################
### Set methods ###
###################

    def setAxisTitleSize(self, size):

        ROOT.gStyle.SetTitleSize(size,"X")
        ROOT.gStyle.SetTitleSize(size,"Y")
        
        return True

    def setAxisTitleOffset(self, offset):

        ROOT.gStyle.SetTitleOffset(offset,"X")
        ROOT.gStyle.SetTitleOffset(offset,"Y")

        return True


    
    def getMarkerStyle(self, index):
        
        
        if index%9 == 0 and index > 0:
            self.counter += 1
        if index == 40:
            sys.exit("Overflow. Reduce number of graphs!")
        
        return self.markerSet[self.counter]
        
                    
    def setGroup(self):
    
        self.GroupList = []
        TempList = []
        for i, Element in enumerate(self.__file):
            TempList.append(self.__file[i].getName()[:5])
        if self.GraphGroup == True:
            if self.NameGroup == True:
                for i, TempName in enumerate(TempList):
                    if TempName not in self.GroupList:
                        self.GroupList.append(TempList[i])

            elif self.FluenzGroup == True:
                for i, File in enumerate(self.__file):
                    print File.getFluenceP()

        return True

######################
### Legend methods ###
######################

    def setLegend(self):

        self.legend = ROOT.TLegend(self.LegendParameters[0],self.LegendParameters[1],self.LegendParameters[2],self.LegendParameters[3])
        self.legend.SetFillColor(0)
        self.legend.SetTextSize(.02)
        #self.arrangeLegend()

        for i,graph in enumerate(self.__graphs):

            try:
                if self.legendEntry == "name":
                    self.legend.AddEntry(self.__graphs[i], self.__file[i].getName(), "p")
                elif self.legendEntry == "id":
                    self.legend.AddEntry(self.__graphs[i], self.__file[i].getID(), "p")
                else:
                    print "Legend entry type not found. Use 'name' instead"
                    self.legend.AddEntry(self.__graphs[i], self.__file[i].getName(), "p")
            except:
                pass

        self.legend.Draw()
        self.canvas.Update()

    # interferes with arrangeFileList
    #def arrangeLegend(self):
        
    #    TempList = []
    #    self.NameList = []
    #    for i, Name in enumerate(self.__file):
    #        TempList.append(self.__file[i].getName())
    #    TempList.sort()
    #    for Name in TempList:
    #        self.NameList.append(Name)
    #    return True
        

        
    def setLegendParameters(self):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right or outside
        # Plot is arround 80% of canvas from (0.1,0.15) to (0.9,0.9). 
        
        self.LegendParameters = []
        para = 0
        
        if len(self.__file[0].getName()) > para:
            para=len(self.__file[0].getName())
        
        # Top right corner is the default/starting position for the legend box.
        self.TopRight = True
        self.TopLeft = self.BottomRight = True
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-para/100.
        Lymin = Lymax-len(self.__graphs)*0.03

        
        # Check if elements are in the top right corner. 
        for i in range(len(self.__file)):
            for j in range(len(self.__file[i].getX())):
                #print self.__file[i].getX()[j]
                #print (abs(self.__file[i].getX()[j]),self.xmax*(1.+self.perc))
                if abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc)))-0.1 > Lxmin:
                    #print (self.__file[i].getName(), abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))))
                    if abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin:
                        #print (self.__file[i].getName(), abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))))
                        #print ("TR", self.__file[i].getName())
                        self.TopRight = False
        
        if self.TopRight == False:
            Lxmin = 0.18
            Lymax = 0.88
            Lymin = Lymax-len(self.__graphs)*0.03
            Lxmax = 2.2*para/100.
        
        # Check if elements are in the top left corner.
        for i in range(len(self.__file)):
            for j in range(len(self.__file[i].getX())):
                if Lxmin-0.1 < abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))) < Lxmax:
                    if self.TopRight == False and abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin+0.1:
                        self.TopLeft = False
                
        if self.TopLeft == False:
            Lxmax = 0.89
            Lymin = 0.18
            Lxmin = Lxmax-para/100.
            Lymax = Lymin+len(self.__graphs)*0.03
        
        # If the plot is too crowded, create more space on the right.
        for i in range(len(self.__file)):
            for j in range(len(self.__file[i].getX())):
                if abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))) > Lxmin:
                    if self.TopLeft == False and self.TopRight == False and abs(self.__file[i].getY()[len(self.__file[i].getY())-1]/(self.ymax*(1.+self.perc))) < Lymax:
                        self.BottomRight = False

        if self.BottomRight == False:
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-para/100.
            Lymin = Lymax-len(self.__graphs)*0.03
            print "Couldn't find sufficient space!"

        self.LegendParameters.append(Lxmin)
        self.LegendParameters.append(Lymin)
        self.LegendParameters.append(Lxmax)
        self.LegendParameters.append(Lymax)
        

        
       


#####################
### Color methods ###
#####################

    def __initColor(self):

        self.__kitGreen.append(ROOT.TColor(1100, 0./255, 169./255, 144./255))
        self.__kitGreen.append(ROOT.TColor(1101,75./255, 195./255, 165./255))
        self.__kitGreen.append(ROOT.TColor(1102,125./255, 210./255, 185./255))
        self.__kitGreen.append(ROOT.TColor(1103,180./255, 230./255, 210./255))
        self.__kitGreen.append(ROOT.TColor(1104,215./255, 240./255, 230./255))

        self.__kitBlue.append(ROOT.TColor(1200, 67./255, 115./255, 194./255))
        self.__kitBlue.append(ROOT.TColor(1201, 120./255, 145./255, 210./255))
        self.__kitBlue.append(ROOT.TColor(1202, 155./255, 170./255, 220./255))
        self.__kitBlue.append(ROOT.TColor(1203, 195./255, 200./255, 235./255))
        self.__kitBlue.append(ROOT.TColor(1204, 225./255, 225./255, 245./255))

        self.__kitMay.append(ROOT.TColor(1300, 102./255, 196./255, 48./255))

        self.__kitYellow.append(ROOT.TColor(1400, 254./255, 231./255, 2./255))

        self.__kitOrange.append(ROOT.TColor(1500, 247./255, 145./255, 16./255))

        self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))

        self.__kitRed.append(ROOT.TColor(1700, 191./255, 35./255, 41./255))
        self.__kitRed.append(ROOT.TColor(1701, 205./255, 85./255, 75./255))
        self.__kitRed.append(ROOT.TColor(1702, 220./255, 130./255, 110./255))
        self.__kitRed.append(ROOT.TColor(1703, 230./255, 175./255, 160./255))
        self.__kitRed.append(ROOT.TColor(1704, 245./255, 215./255, 200./255))

        self.__kitPurple.append(ROOT.TColor(1800, 188./255, 12./255, 141./255))

        self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))

        KITPlot.__init = True
        
        return True

    def getColor(self,clr=0):
        self.colorSet = [1100,1200,1300,1400,1500,1600,1700,1800,1900]
        KITPlot.__color += 1
        KITPlot.__color %= 9

        return self.colorSet[KITPlot.__color-1]

    def setColor(self):
        for graph in self.__graphs:
            graph.SetMarkerColor(self.getColor())
            
        return True

    def getShade(self):
        i = 0
        self.shadeSet = []
        print self.colorSet
        print len(self.colorSet)
        #if i<range(self.colorSet):
        #    for j in range(4):
        #        self.shadeSet.append(self.colorSet[i]+j)
        #    i +=1
        #else:
        #    print self.shadeSet
        #git     return True


###################
### Get methods ###
###################

    def getGraph(self, graph=None):
        
        if len(self.__graphs) == 1:
            return self.__graphs[0]
        elif (len(self.__graphs) != 1) & (graph is None):
            return self._graphs
        elif (len(self.__graphs) != 1) & (graph.isdigit()):
            return self.__graphs[graph]
        else:
            return False

    def getCanvas(self):
        return self.canvas
        
        

