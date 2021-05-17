import ROOT

hists1D = {}
hists2D = {}
plotdir = "plots/hists"

doPng=True
doPdf=False
doC=False

year=2018
lumi=137000#fb-1

one   = ROOT.TColor(2001,143/255.,45 /255.,86/255.,"darkPurple")#quinacridone magenta
two   = ROOT.TColor(2002,119/255.,104/255.,174/255.,"blahBlue")#blue-violet
three = ROOT.TColor(2003,239/255.,41 /255.,81/255.,"pinkRed")#paradise pink
four  = ROOT.TColor(2004,247/255.,138/255.,18/255.,"orange")#orange
five  = ROOT.TColor(2005,65 /255.,167/255.,143/255.,"PersianGreen")# persian green
six   = ROOT.TColor(2006,38 /255.,70 /255.,83 /255.,"Charcol")# charcol
seven = ROOT.TColor(2007,116/255.,165/255.,127/255.,"Green")#forest green
eight = ROOT.TColor(2008,233/255.,196/255.,106/255.,"Maize")# maize
nine  = ROOT.TColor(2009,85/255.,153/255.,216/255.,"BlueSaph")#blue saphire 
ten   = ROOT.TColor(2010,231/255.,111/255.,81 /255.,"TerraCotta")# terra cotta
elev  = ROOT.TColor(2011,118/255., 30/255., 141/255.,"Englishviolet")
colors = [] #[2001,2002,2003,2004,2005,2006,2007,2008,2009,2010]
#colors.append(2001)#quinacridone magenta
#colors.append(2010)#terra cotta
colors.append(2003)#paradise
colors.append(2004)#orange
colors.append(2008)#maize
colors.append(2005)#persian green
#colors.append(2007)#forest green
colors.append(2009)#bluesapphire
colors.append(2002)#blue-violet
colors.append(2011)#english violet
colors.append(2006)#charcol

def setStyle():
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetLabelSize(0.05,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"t")
    ROOT.gStyle.SetTitleSize(0.06,"xyz")
    ROOT.gStyle.SetTitleSize(0.06,"t")

    ROOT.gStyle.SetPadBottomMargin(0.14)
    ROOT.gStyle.SetPadLeftMargin(0.14)

    ROOT.gStyle.SetPadGridX(0)
    ROOT.gStyle.SetPadGridY(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

    ROOT.gStyle.SetTitleOffset(1,'y')
    ROOT.gStyle.SetLegendTextSize(0.04)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridColor(14)

    ROOT.gStyle.SetMarkerSize(1.0) #large markers
    ROOT.gStyle.SetHistLineWidth(2) # bold lines
    ROOT.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes

    #one = ROOT.TColor(2001,0.906,0.153,0.094)
    #two = ROOT.TColor(2002,0.906,0.533,0.094)
    #three = ROOT.TColor(2003,0.086,0.404,0.576)
    #four =ROOT.TColor(2004,0.071,0.694,0.18)
    #five =ROOT.TColor(2005,0.388,0.098,0.608)
    #six=ROOT.TColor(2006,0.906,0.878,0.094)
    #seven=ROOT.TColor(2007,0.99,0.677,0.614)
    #colors = [1,2001,2002,2003,2004]
    return       

def adjust(hist):
    name=hist.GetName()
    if "h_ht" in name: hist.Rebin(10) 
    if "track_pt" in name: hist.GetXaxis().SetRangeUser(0,10) 
    return

def ytitle(hist):
    name = hist.GetName()
    if "track_" in name: hist.GetYaxis().SetTitle("Tracks")
    elif "jet_" in name: hist.GetYaxis().SetTitle("Jets")
    else: hist.GetYaxis().SetTitle("Events")

def clean1D(hist):
    adjust(hist)
    hist.SetLineWidth(3)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetYaxis().SetTitleSize(0.05)
    hist.GetXaxis().SetNdivisions(505)
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleSize(0.05)
    hist.SetTitle("")
    ytitle(hist)
    hist.SetDirectory(0)
    #hist.Scale(1.0/hist.Integral(0,-1))
    return hist

def decay_label(decay):
    if "darkPhoHad" in decay: return "m_{A'}=0.7 GeV A'#rightarrowee/#mu#mu/#pi#pi"
    if "darkPho" in decay: return "m_{A'}=0.5 GeV, A'#rightarrowee/#mu#mu/#pi#pi"
    if "generic" in decay: return "m_{A'}=m_{#phi}/2, A'#rightarrowu#bar{u}"

def label(mMed,mDark,temp,decay):
    #return "(m_{S},m_{#phi},T)=(%i,%i,%i), %s"%(mMed,mDark,temp,decay_label(decay))
    return "m_{S}=%i, m_{#phi}=%i, T=%i, %s"%(mMed,mDark,temp,decay_label(decay))


def sig_xs(mMed):
    if mMed == 125: return 34.8
    if mMed == 200: return 13.6
    if mMed == 300: return 8.9
    if mMed == 400: return 5.9
    if mMed == 750: return 0.5
    if mMed == 1000: return 0.17
    return 1

def col(mMed,temp,mDark,decay):
    if mMed == 125: return 0 
    if mMed == 200: return 1
    if mMed == 300: return 2
    if mMed == 400: 
        if decay=="generic": return 2
        if decay=="darkPhoHad": return 4
        if mDark==1 : return 2
        if mDark==2 : return 3
        if mDark==5 : return 4
    if mMed == 750: return 4
    if mMed == 1000: return 5
    return 1

def line(mMed,temp,mDark,decay):
    if temp==2 : return 1
    elif temp==1 : return 2
    else : return 3

def get1D(mMed,mDark,temp,decay,histname):

    # Get hist
    filename = "output/{}_mMed-{}_mDark-{}_temp-{}_decay-{}.root".format(year,mMed,mDark,temp,decay)
    f = ROOT.TFile.Open(filename)
    if not f : return 0
    hist = f.Get(histname)
    if hist :
        hist.Scale( sig_xs(mMed) / 10000. * lumi)
        hist.SetLineColor( colors[col(mMed,mDark,temp,decay)] )
        hist.SetLineStyle( line(mMed,mDark,temp,decay) )
        clean1D(hist)
        return hist
    else : return 0

def qcd_xs(sample):
    if "QCD_HT200to300"   in sample : return 1559000  / 100000. * lumi
    if "QCD_HT300to500"   in sample : return 347700 / 100000. * lumi
    if "QCD_HT500to700"   in sample : return 32100 / 100000. * lumi 
    if "QCD_HT700to1000"  in sample : return 6831 / 100000. * lumi 
    if "QCD_HT1000to1500" in sample : return 1207 / 100000. * lumi 
    if "QCD_HT1500to2000" in sample : return 119.9 / 100000. * lumi 
    if "QCD_HT2000toInf"  in sample : return 25.24 / 100000. * lumi 
    return 1

def getQCD(dist):

    # Get hist
    samples =[]
    #samples.append("{}_QCD_HT200to300".format(year))# do slicing later
    samples.append("{}_QCD_HT300to500".format(year))# do slicing later
    samples.append("{}_QCD_HT500to700".format(year))# do slicing later
    samples.append("{}_QCD_HT700to1000".format(year))# do slicing later
    samples.append("{}_QCD_HT1000to1500".format(year))# do slicing later
    samples.append("{}_QCD_HT1500to2000".format(year))# do slicing later
    samples.append("{}_QCD_HT2000toInf".format(year))# do slicing later

    hists = []
    for sample in samples:
        f = ROOT.TFile.Open("output/{}.root".format(sample))
        if not f: continue
        h = f.Get(dist)
        if not h: continue
        h.SetDirectory(0)
        h.Scale(qcd_xs(sample))
        hists.append(h)
        #print(sample, qcd_xs(sample), h.Integral(0,-1))

    hist_final = hists[0].Clone("QCD_"+dist)
    for i,hist in enumerate(hists):
        if i>0: hist_final.Add(hist)

    print(dist, "INT", hist_final.Integral(0,-1))

    clean1D(hist_final)
    #hist_final.SetLineColor(ROOT.kBlack)
    hist_final.SetLineColor(ROOT.kGray)
    hist_final.SetFillColorAlpha(ROOT.kGray,0.8)

    return hist_final



def plot1D(name, title, x, nbinsx, xmin, xmax, weight=1.):
    if name in hists1D:
        # fill
        hists1D[name].Fill(x,weight)
    else : 
        # create and fill
        hist = ROOT.TH1F(name, title, nbinsx, xmin, xmax)
        hist.SetDirectory(0)
        hist.Fill(x,weight)
        hists1D[name] = hist
    return

def plot2D(name, title, x, y, nbinsx, xmin, xmax, nbinsy, ymin, ymax, weight=1.):
    if name in hists2D:
        # fill
        hists2D[name].Fill(x,y,weight)
    else : 
        # create and fill
        hist = ROOT.TH2F(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
        hist.SetDirectory(0)
        hist.Fill(x,weight)
        hists2D[name] = hist

    return

def draw1D(c1,h, drawopt="hist"):  
    c1.cd() 
    c1.Clear()
    h.Draw(drawopt)
    if doPng: c1.Print("{}/{}.png".format(plotdir,h.GetName()))
    if doPdf: c1.Print("{}/{}.pdf".format(plotdir,h.GetName()))
    if doC  : c1.Print("{}/{}.C".format(plotdir,h.GetName()))
    h.Write()
    return 

def draw2D(c2, h, drawopt="COLZ"):  
    c2.cd() 
    c2.Clear()
    c2.SetTopMargin(0.05)
    c2.SetLeftMargin(0.2)
    c2.SetBottomMargin(0.2)
    c2.SetRightMargin(0.2);
    h.Draw(drawopt)

    if doPng: c2.Print("{}/{}.png".format(plotdir,h.GetName()))
    if doPdf: c2.Print("{}/{}.pdf".format(plotdir,h.GetName()))
    if doC  : c2.Print("{}/{}.C".format(plotdir,h.GetName()))
    h.Write()
    return 

def drawAll1D(c1,drawopt="hist"):
    for n, h in hists1D.items():
        draw1D(c1,h, drawopt);
    return

def drawAll2D(c2,drawopt="hist"):
    for n, h in hists2D.items():
        draw2D(c2,h, drawopt);
    return 
