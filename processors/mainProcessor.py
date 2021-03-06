from coffea import hist, processor
import numpy as np
import awkward1 as ak
from utils import utility as utl
from utils.objects import Objects
from utils import baseline as bl
from utils import fatjets as fj

class MainProcessor(processor.ProcessorABC):
        def __init__(self):
                # dataset_axis = hist.Cat("dataset", "Primary dataset")
                # pt_axis = hist.Bin("pt", r"$p_{T}$ [GeV]", 40, 0, 3500)
                ntrack_axis                 = hist.Bin("ntracks",               "Number of Tracks",                                 50,     0.0,    500.0)
                njet_axis                   = hist.Bin("njets",                 "Number of Jets",                                   20,     0.0,    20.0)
                eta_axis                    = hist.Bin("eta",                   r"$\eta$",                                   100,   -3.5, 3.5)
                pt_axis                     = hist.Bin("pt",                    "p_{T} (GeV)",                                   500,    0.0,    500.0)
                trkpt_axis                  = hist.Bin("trkpt",                 "p_{T} (GeV)",                                   200,    0.0,     20.0)
                trkptL_axis                 = hist.Bin("trkptL",                "p_{T} (GeV)",                                   1000,    0.0,     100.0)
                ht_axis                     = hist.Bin("ht",                    "H_{T} (GeV)",                                   500,    0.0,    5000.0)
                st_axis                     = hist.Bin("st",                    "S_{T} (GeV)",                                   500,    0.0,    5000.0)
                met_axis                    = hist.Bin("MET",                   "E_{T}^{miss} (GeV)",                                   200,    0.0,    2000.0)


                self._accumulator = processor.dict_accumulator({
                        # 'jtpt':hist.Hist("Counts", dataset_axis, pt_axis),
                        # 'jteta':hist.Hist("Counts",dataset_axis,eta_axis),
                        'h_ht':            hist.Hist("h_ht",                   ht_axis),
                        'h_st':            hist.Hist("h_st",                   st_axis),
                        'h_met':           hist.Hist("h_met",                  met_axis),
                        'h_ntracks':       hist.Hist("h_ntracks",              ntrack_axis),
                        'h_track_pt':      hist.Hist("h_track_pt",             trkpt_axis),
                        'h_track_eta':     hist.Hist("h_track_eta",            eta_axis),
                        'h_jet_pt':        hist.Hist("h_jet_pt",               pt_axis),
                        'h_jet_eta':       hist.Hist("h_jet_eta",              eta_axis),
                        'h_njets':         hist.Hist("h_njets",                njet_axis),

                        'h_scout_ht':        hist.Hist("h_scout_ht",         ht_axis),
                        'h_scout_ntracks05': hist.Hist("h_scout_ntracks05",  ntrack_axis),
                        'h_scout_ntracks06': hist.Hist("h_scout_ntracks06",  ntrack_axis),
                        'h_scout_ntracks07': hist.Hist("h_scout_ntracks07",  ntrack_axis),
                        'h_scout_ntracks08': hist.Hist("h_scout_ntracks08",  ntrack_axis),
                        'h_scout_ntracks09': hist.Hist("h_scout_ntracks09",  ntrack_axis),
                        'h_scout_ntracks':   hist.Hist("h_scout_ntracks",    ntrack_axis),
                        'h_scout_track_pt':  hist.Hist("h_scout_track_pt",   trkpt_axis),
                        'h_scout_track_ptL': hist.Hist("h_scout_track_ptL",  trkptL_axis),
                        'h_scout_track_eta': hist.Hist("h_scout_track_eta",  eta_axis),
                        'h_scout_jet_pt':    hist.Hist("h_scout_jet_pt",     pt_axis),
                        'h_scout_jet_eta':   hist.Hist("h_scout_jet_eta",    eta_axis),
                        'h_scout_njets':     hist.Hist("h_scout_njets",      njet_axis),

                        'h_scout_ntracks_lowNPV':   hist.Hist("h_scout_ntracks_lowNPV",    ntrack_axis),
                        'h_scout_ntracks_midNPV':   hist.Hist("h_scout_ntracks_midNPV",    ntrack_axis),
                        'h_scout_ntracks_higNPV':   hist.Hist("h_scout_ntracks_higNPV",    ntrack_axis),

                        'h_off_ht':        hist.Hist("h_off_ht",         ht_axis),
                        'h_off_ntracks06': hist.Hist("h_off_ntracks06",  ntrack_axis),
                        'h_off_ntracks08': hist.Hist("h_off_ntracks08",  ntrack_axis),
                        'h_off_ntracks':   hist.Hist("h_off_ntracks",    ntrack_axis),
                        'h_off_track_pt':  hist.Hist("h_off_track_pt",   trkpt_axis),
                        'h_off_track_eta': hist.Hist("h_off_track_eta",  eta_axis),
                        'h_off_jet_pt':    hist.Hist("h_off_jet_pt",     pt_axis),
                        'h_off_jet_eta':   hist.Hist("h_off_jet_eta",    eta_axis),
                        'h_off_njets':     hist.Hist("h_off_njets",      njet_axis),

                        'cutflow':         processor.defaultdict_accumulator(int),
                        'trigger':         processor.defaultdict_accumulator(int),
        
                     #)
                })

        @property
        def accumulator(self):
                return self._accumulator

        def process(self, df):
                output = self.accumulator.identity()

                # important variables
                obj = Objects(df)
                mask = bl.getBaselineMask(df)

                electrons = obj.goodElectrons()[mask]
                muons = obj.goodMuons()[mask]
                jets = obj.goodJets()[mask]
                madHT_cut = df['madHT'][mask]
                met = df['MET'][mask]
                metPhi = df['METPhi'][mask]
                nVtx = df['NVtx'][mask]
                tracks05 = obj.goodTracks05()[mask]
                tracks06 = obj.goodTracks06()[mask]
                tracks07 = obj.goodTracks07()[mask]
                tracks08 = obj.goodTracks08()[mask]
                tracks09 = obj.goodTracks09()[mask]
                tracks = obj.goodTracks()[mask]
                output['cutflow']['all events'] += jets.size
    

                # Hack: defining weights: same length as the number of events in the chunk
                # Check if this is what other people do too
                luminosity = 21071.0+38654.0
                evtw = np.ones(len(df['MET']),dtype=float)
                #evtw = df['Weight'][mask]*luminosity
                #evtw = df['Weight'][mask]*luminosity
                ew = utl.awkwardReshape(electrons,evtw)
                mw = utl.awkwardReshape(muons,evtw)
                jw = utl.awkwardReshape(jets,evtw)
                tw = utl.awkwardReshape(tracks,evtw)
                tw06 = utl.awkwardReshape(tracks06,evtw)
                tw05 = utl.awkwardReshape(tracks05,evtw)

                # Getting subset of variables based on number of AK8 jets
                # calculating event variables
                ht = ak.sum(jets.pt,axis=1)
                st = ht + met
                #dPhiMinJ = utl.deltaPhi(fjets.phi,metPhi).min()
                #dPhiMinj = utl.deltaPhi(jets.phi,metPhi).min()

                #
                # Trigger Study...
                #
                cut_met = met > 250
                cut_ht_offline = ht > 1200 
                cut_ht_scouting = ht > 500
                jets_met      = jets[cut_met]
                jets_off   = jets[cut_ht_offline]
                output['trigger']['all events']  += jets.size
                output['trigger']['met']         += jets_met.size
                output['trigger']['ht_offline']  += jets_off.size


                ## ht scouting 
                tracks05_scout = tracks05[cut_ht_scouting]
                tracks06_scout = tracks06[cut_ht_scouting]
                tracks07_scout = tracks07[cut_ht_scouting]
                tracks08_scout = tracks08[cut_ht_scouting]
                tracks09_scout = tracks09[cut_ht_scouting]
                tracks_scout = tracks[cut_ht_scouting]
                jets_scout = jets[cut_ht_scouting]
                nVtx_scout = nVtx[cut_ht_scouting]
                evtw_scout = evtw[cut_ht_scouting]
                tw_scout = tw[cut_ht_scouting] 
                tw05_scout = tw05[cut_ht_scouting] 
                jw_scout = jw[cut_ht_scouting] 
                output['trigger']['ht_scouting'] += jets_scout.size

                ## npv study scouting 
                cut_lowNPV = nVtx_scout < 20
                cut_midNPV = (nVtx_scout > 20) & (nVtx_scout < 30)
                cut_higNPV = nVtx_scout > 30
                evtw_scout_lowNPV = evtw_scout[cut_lowNPV]
                evtw_scout_midNPV = evtw_scout[cut_midNPV]
                evtw_scout_higNPV = evtw_scout[cut_higNPV]
                tracks_scout_lowNPV = tracks_scout[cut_lowNPV]
                tracks_scout_midNPV = tracks_scout[cut_midNPV]
                tracks_scout_higNPV = tracks_scout[cut_higNPV]

                ## ht offline 
                tracks06_off = tracks06[cut_ht_offline]
                tracks08_off = tracks08[cut_ht_offline]
                tracks_off = tracks[cut_ht_offline]
                jets_off = jets[cut_ht_offline]
                evtw_off = evtw[cut_ht_offline]
                tw_off = tw[cut_ht_offline] 
                tw06_off = tw06[cut_ht_offline] 
                jw_off = jw[cut_ht_offline] 
                output['trigger']['ht_offline']  += jets_off.size

                ## at least 1 AK4 Jet
                cut_1j = jets.counts >= 1
                jets_1j = jets[cut_1j]
                metPhi_1j = metPhi[cut_1j]
                evtw_1j = evtw[cut_1j]
                #dPhij1 = utl.deltaPhi(jets_1j.phi[:,0],metPhi_1j)
                output['cutflow']['one jet'] += jets_1j.size

                ## at least 2 AK4 Jets
                cut_2j = jets.counts >= 2
                jets_2j = jets[cut_2j]
                metPhi_2j = metPhi[cut_2j]
                evtw_2j = evtw[cut_2j]
                j1_eta = np.array(jets_2j.eta[:,0])
                j2_eta = np.array(jets_2j.eta[:,1])
                j1_phi = np.array(jets_2j.phi[:,0])
                j2_phi = np.array(jets_2j.phi[:,1])
                dEtaj12 = abs(j1_eta - j2_eta)
                #deltaR12j = utl.delta_R(j1_phi,j2_phi,j1_eta,j2_eta)
                #dPhij1_2j = utl.deltaPhi(j1_phi,metPhi_2j)
                #dPhij2 = utl.deltaPhi(j2_phi,metPhi_2j)
                output['cutflow']['two jets'] += jets_2j.size

                ### at least 1 AK8 Jet
                #cut_1fj = fjets.counts >= 1
                #fjets_1fj = fjets[cut_1fj]
                #metPhi_1fj = metPhi[cut_1fj]
                #evtw_1fj = evtw[cut_1fj]
                #dPhiJ1 = utl.deltaPhi(fjets_1fj.phi[:,0],metPhi_1fj)
                ### at least 2 AK8 Jets
                #cut_2fj = fjets.counts >= 2
                #fjets_2fj = fjets[cut_2fj]
                #metPhi_2fj = metPhi[cut_2fj]
                #evtw_2fj = evtw[cut_2fj]
                #J1_eta = np.array(fjets_2fj.eta[:,0])
                #J2_eta = np.array(fjets_2fj.eta[:,1])
                #J1_phi = np.array(fjets_2fj.phi[:,0])
                #J2_phi = np.array(fjets_2fj.phi[:,1])
                #dEtaJ12 = abs(J1_eta - J2_eta)
                #deltaR12J = utl.delta_R(J1_phi,J2_phi,J1_eta,J2_eta)
                #dPhiJ1_2fj = utl.deltaPhi(J1_phi,metPhi_2fj)
                #dPhiJ2 = utl.deltaPhi(J2_phi,metPhi_2fj)

                ## twofjets = (fjets.counts >= 2)
                ## difjets = fjets[twofjets]
                ## ptcut = (difjets.pt[:,0] > 200) & (difjets.pt[:,1] > 200)
                ## difjets_pt200 = difjets[ptcut]

                #twofjets = (fjets.counts >= 2)
                #output['cutflow']['two fjets'] += twofjets.sum()

                ## difjets = fjets[twofjets]
                ## difjets_pt200 = difjets[ptcut]
                ## output['jtpt'].fill(dataset=dataset, pt=fjets.pt.flatten())
                ## output['jteta'].fill(dataset=dataset, eta=fjets.eta.flatten())

                output['h_ntracks'].fill(ntracks=tracks.counts.flatten(),weight=evtw)
                output['h_njets'].fill(njets=jets.counts.flatten(),weight=evtw)
                output['h_ht'].fill(ht=ht,weight=evtw)
                output['h_st'].fill(st=st,weight=evtw)
                output['h_met'].fill(MET=met,weight=evtw)

                #output['h_scout_ntracks_v_npv'].fill(npv=nVtx_scout.flatten(),ntracks=tracks_scout.counts.flatten(),weight=evtw_scout)

                output['h_scout_ntracks05'].fill(ntracks=tracks05_scout.counts.flatten(),weight=evtw_scout)
                output['h_scout_ntracks06'].fill(ntracks=tracks06_scout.counts.flatten(),weight=evtw_scout)
                output['h_scout_ntracks07'].fill(ntracks=tracks07_scout.counts.flatten(),weight=evtw_scout)
                output['h_scout_ntracks08'].fill(ntracks=tracks08_scout.counts.flatten(),weight=evtw_scout)
                output['h_scout_ntracks09'].fill(ntracks=tracks09_scout.counts.flatten(),weight=evtw_scout)
                output['h_scout_ntracks'].fill(ntracks=tracks_scout.counts.flatten(),weight=evtw_scout)
                output['h_scout_track_pt'].fill(trkpt=tracks05_scout.pt.flatten(),weight=ak.flatten(tw05_scout))
                output['h_scout_track_ptL'].fill(trkptL=tracks05_scout.pt.flatten(),weight=ak.flatten(tw05_scout))
                output['h_scout_track_eta'].fill(eta=tracks_scout.eta.flatten(),weight=ak.flatten(tw_scout))
                output['h_scout_jet_pt'].fill(pt=jets_scout.pt.flatten(),weight=ak.flatten(jw_scout))
                output['h_scout_jet_eta'].fill(eta=jets_scout.eta.flatten(),weight=ak.flatten(jw_scout))
            # pileup study
                output['h_scout_ntracks_lowNPV'].fill(ntracks=tracks_scout_lowNPV.counts.flatten(),weight=evtw_scout_lowNPV)
                output['h_scout_ntracks_midNPV'].fill(ntracks=tracks_scout_midNPV.counts.flatten(),weight=evtw_scout_midNPV)
                output['h_scout_ntracks_higNPV'].fill(ntracks=tracks_scout_higNPV.counts.flatten(),weight=evtw_scout_higNPV)

# offline
                output['h_off_ntracks06'].fill(ntracks=tracks06_off.counts.flatten(),weight=evtw_off)
                output['h_off_ntracks08'].fill(ntracks=tracks08_off.counts.flatten(),weight=evtw_off)
                output['h_off_ntracks'].fill(ntracks=tracks_off.counts.flatten(),weight=evtw_off)
                output['h_off_track_pt'].fill(trkpt=tracks06_off.pt.flatten(),weight=ak.flatten(tw06_off))
                output['h_off_track_eta'].fill(eta=tracks_off.eta.flatten(),weight=ak.flatten(tw_off))
                output['h_off_jet_pt'].fill(pt=jets_off.pt.flatten(),weight=ak.flatten(jw_off))
                output['h_off_jet_eta'].fill(eta=jets_off.eta.flatten(),weight=ak.flatten(jw_off))
                #output['h_jPt'].fill(pt=jets.pt.flatten(),weight=ak.flatten(jw))
                #output['h_jEta'].fill(eta=jets.eta.flatten(),weight=ak.flatten(jw))
                #output['h_jPhi'].fill(phi=jets.phi.flatten(),weight=ak.flatten(jw))
                #output['h_jAxismajor'].fill(axismajor=jets.axismajor.flatten(),weight=ak.flatten(jw))
                #output['h_jAxisminor'].fill(axisminor=jets.axisminor.flatten(),weight=ak.flatten(jw))
                #output['h_jPtD'].fill(ptD=jets.ptD.flatten(),weight=ak.flatten(jw))
                #output['h_jPtAK8'].fill(pt=fjets.pt.flatten(),weight=ak.flatten(fjw))
                #output['h_jEtaAK8'].fill(eta=fjets.eta.flatten(),weight=ak.flatten(fjw))
                #output['h_jPhiAK8'].fill(phi=fjets.phi.flatten(),weight=ak.flatten(fjw))
                #output['h_jAxismajorAK8'].fill(axismajor=fjets.axismajor.flatten(),weight=ak.flatten(fjw))
                #output['h_jAxisminorAK8'].fill(axisminor=fjets.axisminor.flatten(),weight=ak.flatten(fjw))
                #output['h_jGirthAK8'].fill(girth=fjets.girth.flatten(),weight=ak.flatten(fjw))
                #output['h_jPtDAK8'].fill(ptD=fjets.ptD.flatten(),weight=ak.flatten(fjw))
                #output['h_jTau1AK8'].fill(tau1=fjets.tau1.flatten(),weight=ak.flatten(fjw))
                #output['h_jTau2AK8'].fill(tau2=fjets.tau2.flatten(),weight=ak.flatten(fjw))
                #output['h_jTau3AK8'].fill(tau3=fjets.tau3.flatten(),weight=ak.flatten(fjw))
                #output['h_jTau21AK8'].fill(tau21=fjets[fjets.tau1 > 0].tau2.flatten()/fjets[fjets.tau1 > 0].tau1.flatten(),weight=ak.flatten(fjw)[(fjets.tau1 > 0).flatten()])
                #output['h_jTau32AK8'].fill(tau32=fjets[fjets.tau2 > 0].tau3.flatten()/fjets[fjets.tau2 > 0].tau2.flatten(),weight=ak.flatten(fjw)[(fjets.tau2 > 0).flatten()])
                #output['h_jSoftDropMassAK8'].fill(softDropMass=fjets.softDropMass.flatten(),weight=ak.flatten(fjw))
                #output['h_dEtaJ12'].fill(dEtaJ12=dEtaJ12,weight=evtw_2fj)
                #output['h_dRJ12'].fill(dRJ12=deltaR12J,weight=evtw_2fj)
                #output['h_dPhiJ1MET'].fill(dPhiJMET=dPhiJ1,weight=evtw_1fj)
                #output['h_dPhiJ2MET'].fill(dPhiJMET=dPhiJ2,weight=evtw_2fj)
                #output['h_dPhiMinJMET'].fill(dPhiJMET=dPhiMinJ,weight=evtw)
                #output['h_dPhiJ1METrdPhiJ2MET'].fill(dPhiJ1METrdPhiJ2MET=dPhiJ1_2fj[dPhiJ2>0]/dPhiJ2[dPhiJ2>0],weight=evtw_2fj[dPhiJ2>0])
                #output['h_mT'].fill(mT=mtAK8,weight=evtw)
                #output['h_METrHT_pt30'].fill(METrHT_pt30=met[ht>0]/ht[ht>0],weight=evtw[ht>0])
                #output['h_METrST_pt30'].fill(METrST_pt30=met[st>0]/st[st>0],weight=evtw[st>0])
                ## Cut: at least 2 AK8 jets
                #output['h_njets_ge2AK8j'].fill(njets=jets[cut_2fj].counts.flatten(),weight=evtw[cut_2fj])
                #output['h_njetsAK8_ge2AK8j'].fill(njets=fjets[cut_2fj].counts.flatten(),weight=evtw[cut_2fj])
                #output['h_ht_ge2AK8j'].fill(ht=ht[cut_2fj],weight=evtw[cut_2fj])
                #output['h_st_ge2AK8j'].fill(st=st[cut_2fj],weight=evtw[cut_2fj])
                #output['h_met_ge2AK8j'].fill(MET=met[cut_2fj],weight=evtw[cut_2fj])
                #output['h_dPhiJ1MET_ge2AK8j'].fill(dPhiJMET=dPhiJ1[fjets_1fj.counts >= 2],weight=evtw_1fj[fjets_1fj.counts >= 2])
                #output['h_dPhiMinJMET_ge2AK8j'].fill(dPhiJMET=dPhiMinJ[cut_2fj],weight=evtw[cut_2fj])
                #output['h_METrHT_pt30_ge2AK8j'].fill(METrHT_pt30=met[(cut_2fj) & (ht>0)]/ht[(cut_2fj) & (ht>0)],weight=evtw[(cut_2fj) & (ht>0)])
                #output['h_METrST_pt30_ge2AK8j'].fill(METrST_pt30=met[(cut_2fj) & (st>0)]/st[(cut_2fj) & (st>0)],weight=evtw[(cut_2fj) & (st>0)])
                #output['h_mT_ge2AK8j'].fill(mT=mtAK8[cut_2fj],weight=evtw[cut_2fj])
                ## more AK4 jets variables
                #output['h_dEtaj12'].fill(dEtaJ12=dEtaj12,weight=evtw_2j)
                #output['h_dRj12'].fill(dRJ12=deltaR12j,weight=evtw_2j)
                #output['h_dPhij1MET'].fill(dPhiJMET=dPhij1,weight=evtw_1j)
                #output['h_dPhij2MET'].fill(dPhiJMET=dPhij2,weight=evtw_2j)
                #output['h_dPhiMinjMET'].fill(dPhiJMET=dPhiMinj,weight=evtw)
                #output['h_dPhij1METrdPhij2MET'].fill(dPhiJ1METrdPhiJ2MET=dPhij1_2j[dPhij2>0]/dPhij2[dPhij2>0],weight=evtw_2j[dPhij2>0])
                ## Cut: at least 2 AK4 jets
                #output['h_njets_ge2AK4j'].fill(njets=jets[cut_2j].counts.flatten(),weight=evtw[cut_2j])
                #output['h_njetsAK8_ge2AK4j'].fill(njets=fjets[cut_2j].counts.flatten(),weight=evtw[cut_2j])
                #output['h_ht_ge2AK4j'].fill(ht=ht[cut_2j],weight=evtw[cut_2j])
                #output['h_st_ge2AK4j'].fill(st=st[cut_2j],weight=evtw[cut_2j])
                #output['h_met_ge2AK4j'].fill(MET=met[cut_2j],weight=evtw[cut_2j])
                #output['h_dPhij1MET_ge2AK4j'].fill(dPhiJMET=dPhij1[jets_1j.counts >= 2],weight=evtw_1j[jets_1j.counts >= 2])
                #output['h_dPhiMinjMET_ge2AK4j'].fill(dPhiJMET=dPhiMinj[cut_2j],weight=evtw[cut_2j])
                #output['h_METrHT_pt30_ge2AK4j'].fill(METrHT_pt30=met[(cut_2j) & (ht>0)]/ht[(cut_2j) & (ht>0)],weight=evtw[(cut_2j) & (ht>0)])
                #output['h_METrST_pt30_ge2AK4j'].fill(METrST_pt30=met[(cut_2j) & (st>0)]/st[(cut_2j) & (st>0)],weight=evtw[(cut_2j) & (st>0)])
                #output['h_mT_ge2AK4j'].fill(mT=mtAK8[cut_2j],weight=evtw[cut_2j])
                #output['h_madHT'].fill(ht=madHT_cut,weight=evtw)
                return output

        def postprocess(self, accumulator):
                return accumulator
