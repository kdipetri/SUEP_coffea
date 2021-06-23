import ROOT
import math
from array import array
from plothelper import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)

setStyle()


year=2018
lumi=137000#fb-1

def adjust(hist):
    name=hist.GetName()
    if "h_ht" in name: hist.Rebin(10) 
    if "track_pt" in name: hist.GetXaxis().SetRangeUser(0,10) 
    return


def significance(s,b):
    # asymptotive discovery sensitivity 

    # cleanup, approx errs
    if b<1 : b = 1
    s_err = s*0.2
    b_err = b

    # compute significance in steps
    part1 = math.log( ( (s + b)*(b + b_err**2.0 ) )/( b**2.0 + (s + b)*b_err**2.0 )  ) 
    part2 = math.log( 1 + ( b_err**2.0 * s )/( b*(b + b_err**2 ) ) ) 

    tmp = (s+b)*part1 - (b**2/b_err**2) * part2
    if tmp < 0 : return 0 
    signif = ( 2*( (s+b)*part1 - (b**2/b_err**2) * part2 ) ) **0.5 
    return signif 

def getSignificance(hsig, hbkg):
    #takes signal and background ntrack 
    #computes significance as a function of ntracks 
    
    hsigma = hsig.Clone("signif_{}".format(hsig.GetName()))

    for b in range(0,hsigma.GetNbinsX() ):

        sig = hsig.Integral(b,-1)
        bkg = hbkg.Integral(b,-1)

        sigma = significance(sig,bkg)
        print(b, sig, bkg, sigma)
        hsigma.SetBinContent(b,sigma)

    return hsigma


def compare1D(hists,labels,filename):
    c = ROOT.TCanvas(filename,"",800,800)

    dy = 0.04*len(hists)
    #dy = 0.05*len(hists)
    leg = ROOT.TLegend(0.48,0.86-dy,0.86,0.86)
    #leg = ROOT.TLegend(0.18,0.86-dy,0.86,0.86)
    leg.SetTextSize(0.03)
    #leg.SetTextSize(0.035)
    leg.SetBorderSize(0)
    ymax = 0
    for i,hist in enumerate(hists):
        
        if i==0: hist.Draw("hist")
        else : hist.Draw("hist same")

        if hist.GetMaximum() > ymax: ymax=hist.GetMaximum()

        leg.AddEntry(hist,labels[i],"l")

    leg.Draw()
    c.SetLogy(1)
    hists[0].GetYaxis().SetRangeUser(0.1,ymax*100)
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
    hist_qcd = getQCD(dist)

    for mMed in mMeds:
        hist_signal = get1D(mMed,mDark,temp,decay,dist)
        if hist_signal: 
            hist_signif = getSignificance(hist_signal,hist_qcd) 
            hists.append(hist_signif)
            labels.append("m_{S}=%i GeV"%(mMed))
            #labels.append(label(mMed,mDark,temp,decay))
        else: print ("WHOOPS")

    compare1D(hists,labels,"nTracksScan/compare_mMed_mDark{}_temp{}_decay_{}_{}".format(mDark,temp,decay,dist))


def compareDecay(dist):
    temp=2
    mMed=400
    mDark=2
    decays=["darkPho","darkPhoHad","generic"]

    hists=[]
    labels=[]
    hist_qcd = getQCD(dist)

    for decay in decays:
        hist_signal = get1D(mMed,mDark,temp,decay,dist)
        if hist_signal: 
            hist_signif = getSignificance(hist_signal,hist_qcd) 
            hists.append(hist_signif)
            labels.append(decay_label(decay))
            #labels.append(label(mMed,mDark,temp,decay))

    compare1D(hists,labels,"nTracksScan/compare_decay_mMed{}_mDark{}_temp_{}_{}".format(mMed,mDark,decay,dist))

def compareAll(dist):
    temps=[1,2,5]
    mMed=400
    mDarks=[1,2,5]
    decay="darkPho"
    #decays=["darkPho","darkPhoHad","generic"]
    #dist="h_ntracks"

    hists=[]
    labels=[]

    hist_qcd = getQCD(dist)

    for temp in temps:
        for mDark in mDarks:
            #for decay in decays:
                hist_signal = get1D(mMed,mDark,temp,decay,dist)
                if hist_signal: 
                    hist_signif = getSignificance(hist_signal,hist_qcd) 
                    hists.append(hist_signif)
                    labels.append("m_{#phi}=%i, T=%i GeV"%(mDark,temp))
                    #labels.append(label(mMed,mDark,temp,decay))
    
    
    compare1D(hists,labels,"nTracksScan/compareAll_mMed{}_{}".format(mMed,dist))


compareAll("h_ntracks")
#compareAll("h_ht")
#compareAll("h_njets")

compareAll("h_off_ntracks")
compareAll("h_off_ntracks06")
compareAll("h_off_ntracks08")
compareAll("h_off_track_pt")
compareAll("h_scout_ntracks")
compareAll("h_scout_ntracks06")
compareAll("h_scout_ntracks08")
compareAll("h_scout_track_pt")

compareMmed("h_scout_ntracks")
compareMmed("h_scout_ntracks06")
compareMmed("h_scout_ntracks08")
compareMmed("h_off_ntracks")
compareMmed("h_off_ntracks06")
compareMmed("h_off_ntracks08")

compareDecay("h_scout_ntracks")
compareDecay("h_off_ntracks")
