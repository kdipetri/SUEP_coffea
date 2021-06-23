import ROOT
from array import array
from plothelper import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)

setStyle()


def compare1D(hists,labels,filename):
    c = ROOT.TCanvas(filename,"",800,700)
    c.SetLeftMargin(0.2)

    dy = 0.04*len(hists)
    #dy = 0.05*len(hists)
    leg = ROOT.TLegend(0.65,0.86-dy,0.86,0.86)
    leg.SetTextSize(0.03)
    leg.SetBorderSize(0)
    ymax = 0
    for i,hist in enumerate(hists):
        
        if i==0: hist.Draw("hist")
        else : hist.Draw("hist same")

        if hist.GetMaximum() > ymax: ymax=hist.GetMaximum()

        if "QCD" in labels[i]: leg.AddEntry(hist,labels[i],"f")
        else : leg.AddEntry(hist,labels[i],"l")

    leg.Draw()
    c.SetLogy(1)
    if "scout_track_pt" in filename: hists[0].GetYaxis().SetRangeUser(10000,ymax*1.8)
    else : hists[0].GetYaxis().SetRangeUser(0.1,ymax*100)
    c.Print("plots/{}_log.png".format(filename))
    hists[0].GetYaxis().SetRangeUser(0,ymax*1.8) 
    c.SetLogy(0)
    c.Print("plots/{}_lin.png".format(filename))

def compareMmed(dist):
    mDark=2
    mMeds=[125,200,300,400,750,1000]
    temp=2
    decay="darkPho"


    hists=[]
    labels=[]
    hists.append(getQCD(dist))
    labels.append("QCD")
    for mMed in mMeds:
        hist = get1D(mMed,mDark,temp,decay,dist)
        if hist: 
            hists.append(hist)
            labels.append("m_{S}=%i GeV"%(mMed))
            #labels.append(label(mMed,mDark,temp,decay))

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

def compareDecay(dist):
    temp=2
    mMed=400
    mDark=2
    decays=["darkPho","darkPhoHad","generic"]

    hists=[]
    labels=[]
    hists.append(getQCD(dist))
    labels.append("QCD")
    for decay in decays:
        hist = get1D(mMed,mDark,temp,decay,dist)
        if hist: 
            hists.append(hist)
            labels.append(decay_label(decay))
            #labels.append(label(mMed,mDark,temp,decay))

    compare1D(hists,labels,"nTracks/compare_decay_mMed{}_mDark{}_temp_{}_{}".format(mMed,mDark,decay,dist))

def compareAll(dist):
    temps=[1,2,5]
    mMed=400
    mDarks=[1,2,5]
    decay="darkPho"
    #decays=["darkPho","darkPhoHad","generic"]
    #dist="h_ntracks"

    hists=[]
    labels=[]
    if "scout_track_pt" not in dist:
        hists.append(getQCD(dist))
        labels.append("QCD")
    for temp in temps:
        for mDark in mDarks:
            #for decay in decays:
                hist = get1D(mMed,mDark,temp,decay,dist)
                if hist: 
                    if "scout_track_pt" in dist: 
                        hist.Rebin()
                        hist.GetXaxis().SetRangeUser(0,10)
                        hist.GetXaxis().SetTitle("track p_{T} [GeV]")
                    hists.append(hist)
                    labels.append("m_{#phi}=%i, T=%i GeV"%(mDark,temp))
                    #labels.append(label(mMed,mDark,temp,decay))
    
    
    compare1D(hists,labels,"nTracks/compareAll_mMed{}_{}".format(mMed,dist))


compareAll("h_ntracks")
compareAll("h_ht")
compareAll("h_njets")

compareAll("h_scout_ntracks")
compareAll("h_scout_ntracks08")
compareAll("h_scout_ntracks06")
compareAll("h_scout_track_eta")
compareAll("h_scout_track_pt")
#compareAll("h_scout_njets")
compareAll("h_scout_jet_eta")
compareAll("h_scout_jet_pt")

compareAll("h_off_ntracks")
compareAll("h_off_ntracks06")
compareAll("h_off_ntracks08")
compareAll("h_off_track_eta")
compareAll("h_off_track_pt")
#compareAll("h_off_njets")
compareAll("h_off_jet_eta")
compareAll("h_off_jet_pt")

compareMmed("h_ntracks")
compareMmed("h_scout_ntracks")
compareMmed("h_scout_ntracks06")
compareMmed("h_scout_ntracks08")
compareMmed("h_off_ntracks")
compareMmed("h_off_ntracks06")
compareMmed("h_off_ntracks08")
compareMmed("h_ht")
compareMmed("h_njets")

compareDecay("h_ntracks")
compareDecay("h_scout_ntracks")
compareDecay("h_scout_ntracks06")
compareDecay("h_scout_ntracks08")
compareDecay("h_off_ntracks")
compareDecay("h_off_ntracks06")
compareDecay("h_off_ntracks08")
compareDecay("h_ht")
compareDecay("h_njets")
