import ROOT
from array import array
from plothelper import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)

setStyle()


year=2018
lumi=137000#fb-1

def adjust(hist):
    name=hist.GetName()
    if "h_ht" in name: hist.Rebin(10) 
    return

def clean1D(hist):
    adjust(hist)
    hist.SetLineWidth(3)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetXaxis().SetNdivisions(505)
    hist.SetDirectory(0)
    #hist.Scale(1.0/hist.Integral(0,-1))
    return hist

def decay_label(decay):
    if "darkPhoHad" in decay: return "m_{A'}=0.7 GeV"
    if "darkPho" in decay: return "m_{A'}=0.5 GeV"
    if "generic" in decay: return "m_{A'}=m_{#phi}/2, A'#rightarrowu#bar{u}"

def label(mMed,mDark,temp,decay):
    #return "(m_{S},m_{#phi},T)=(%i,%i,%i), %s"%(mMed,mDark,temp,decay_label(decay))
    return "m_{S}=%i, m_{#phi}=%i, T=%i, %s"%(mMed,mDark,temp,decay_label(decay))


def sig_xs(mMed):
    if mMed == 125: return 34.8
    if mMed == 400: return 5.9
    if mMed == 750: return 0.5
    if mMed == 1000: return 0.17
    return 1

def col(mMed,temp,mDark,decay):
    if mMed == 125: return 0 
    if mMed == 400: 
        if mDark==1 : return 0
        if mDark==2 : return 1
        if mDark==5 : return 2
    if mMed == 750: return 2
    if mMed == 1000: return 3
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
    hist_final.SetLineColor(ROOT.kBlack)
    hist_final.SetFillColorAlpha(ROOT.kBlack,0.3)

    return hist_final


def compare1D(hists,labels,filename):
    c = ROOT.TCanvas(filename,"",800,800)

    dy = 0.04*len(hists)
    #dy = 0.05*len(hists)
    leg = ROOT.TLegend(0.18,0.86-dy,0.86,0.86)
    leg.SetTextSize(0.03)
    #leg.SetTextSize(0.035)
    leg.SetBorderSize(0)
    ymax = 0
    for i,hist in enumerate(hists):
        
        if i==0: hist.Draw("hist")
        else : hist.Draw("hist same")

        if hist.GetMaximum() > ymax: ymax=hist.GetMaximum()

        leg.AddEntry(hist,labels[i],"l")

    #leg.Draw()
    c.SetLogy(1)
    hists[0].GetYaxis().SetRangeUser(0.1,ymax*100)
    c.Print("plots/{}_log.png".format(filename))
    hists[0].GetYaxis().SetRangeUser(0,ymax*1.8)
    c.SetLogy(0)
    c.Print("plots/{}_lin.png".format(filename))

def compareMmed(dist):
    mDark=2
    mMeds=[125,400,750,1000]
    temp=2
    decay="darkPhoHad"


    hists=[]
    labels=[]
    hists.append(getQCD(dist))
    labels.append("QCD")
    for mMed in mMeds:
        hist = get1D(mMed,mDark,temp,decay,dist)
        if hist: 
            hists.append(hist)
            labels.append(label(mMed,mDark,temp,decay))

    compare1D(hists,labels,"nTracks/compare_mMed_mDark{}_temp{}_decay_{}_{}".format(mDark,temp,decay,dist))

def compareMdark():
    mDarks=[1,2,5]
    mMed=400
    temp=2
    decay="darkPho"
    dist="h_ntracks"

    hists=[]
    labels=[]
    for mDark in mDarks:
        hist = get1D(mMed,mDark,temp,decay,dist)
        if hist: 
            hists.append(hist)
            labels.append(label(mMed,mDark,temp,decay))

    compare1D(hists,labels,"nTracks/compare_mDark_mMed{}_temp{}_decay_{}_{}".format(mMed,temp,decay,dist))

def compareTemp():
    temps=[1,2,5]
    mMed=400
    mDark=2
    decay="darkPho"
    dist="h_ntracks"

    hists=[]
    labels=[]
    for temp in temps:
        hist = get1D(mMed,mDark,temp,decay,dist)
        if hist: 
            hists.append(hist)
            labels.append(label(mMed,mDark,temp,decay))

    compare1D(hists,labels,"nTracks/compare_temp_mMed{}_mDark{}_decay_{}_{}".format(mMed,mDark,decay,dist))

def compareAll(dist):
    temps=[1,2,5]
    mMed=400
    mDarks=[1,2,5]
    decay="darkPho"
    #decays=["darkPho","darkPhoHad","generic"]
    #dist="h_ntracks"

    hists=[]
    labels=[]
    hists.append(getQCD(dist))
    labels.append("QCD")
    for temp in temps:
        for mDark in mDarks:
            #for decay in decays:
                hist = get1D(mMed,mDark,temp,decay,dist)
                if hist: 
                    hists.append(hist)
                    labels.append(label(mMed,mDark,temp,decay))
    
    
    compare1D(hists,labels,"nTracks/compareAll_mMed{}_{}".format(mMed,dist))


compareAll("h_ntracks")
compareAll("h_ht")
compareAll("h_njets")

compareMmed("h_ntracks")
compareMmed("h_ht")
compareMmed("h_njets")
