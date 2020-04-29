import FWCore.ParameterSet.Config as cms

process = cms.Process('EXOPIE')
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.options = cms.untracked.PSet(
	allowUnscheduled = cms.untracked.bool(True)
)

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.register ('runOnMC',
		  True,
		  VarParsing.multiplicity.singleton,
		  VarParsing.varType.bool,
		  "runOnMC")


options.register ('period',
		    'G',
		    VarParsing.multiplicity.singleton,
		    VarParsing.varType.string,
		    "period")

options.register ('useJECText',
		  False,
		  VarParsing.multiplicity.singleton,
		  VarParsing.varType.bool,
		  "useJECText")

options.register ('useMiniAOD',
		    True,
		    VarParsing.multiplicity.singleton,
		    VarParsing.varType.bool,
		    "useMiniAOD")

options.parseArguments()



MCJEC='Summer16_23Sep2016V3_MC'
DATAJEC='Summer16_23Sep2016'+options.period+'V3_DATA'

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
# Other statements
if options.runOnMC:
### Needs to be updated
	process.GlobalTag.globaltag='94X_mc2017_realistic_v12'
else:
    #process.GlobalTag.globaltag='92X_dataRun2_Prompt_v11'  #Conditions for prompt Prompt GT
    process.GlobalTag.globaltag='94X_dataRun2_ReReco_EOY17_v6'   #Conditions for the data reprocessing Rereco_GT
    #process.GlobalTag.globaltag='94X_dataRun2_v6'   #recommended here: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD#2017_Data_re_miniAOD_31Mar2018_9



process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)



## New from Egamma 
## https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes#Running_on_2017_MiniAOD_V2
## for 2017 recomended ID is Fall17V2
## a sequence egammaPostRecoSeq has now been created and should be added to your path, eg process.p=cms.Path(process.egammaPostRecoSeq)

from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runVID=True, #if you want the Fall17V2 IDs, set this to True or remove (default is True)
                       era='2017-Nov17ReReco')  #era is new to select between 2016 / 2017,  it defaults to 2017



# Input source
if options.runOnMC:
	#testFile='/store/mc/RunIIFall17MiniAOD/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/16E915A2-E60E-E811-AD53-001E67A3EF70.root'
        testFile='/store/mc/RunIIFall17MiniAODv2/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/FED523F4-C856-E811-8AA7-0025905A60D6.root'
else:
	testFile='/store/data/Run2017B/MET/MINIAOD/31Mar2018-v1/100000/16963797-0937-E811-ABE2-008CFAE45134.root'


process.source = cms.Source("PoolSource",
                            secondaryFileNames = cms.untracked.vstring(),
                            #fileNames = cms.untracked.vstring("file:/tmp/khurana/temp2017.root"),
                            fileNames = cms.untracked.vstring($inputFileNames),
			    #skipEvents = cms.untracked.uint32(0)
                            )




from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

updateJetCollection(
   process,
   jetSource = cms.InputTag('slimmedJetsAK8'), ## output will be selectedUpdatedPatJets
   pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
   svSource = cms.InputTag('slimmedSecondaryVertices'),
   rParam = 0.8,
   jetCorrections = ('AK8PFchs', cms.vstring(['L2Relative', 'L3Absolute']), 'None'),
   #jetCorrections = ('AK8PFPuppi', cms.vstring(['L2Relative', 'L3Absolute']), 'None'),
   btagDiscriminators = [
      'pfBoostedDoubleSecondaryVertexAK8BJetTags',
      'pfDeepDoubleBJetTags:probQ',
      'pfDeepDoubleBJetTags:probH',
      'pfDeepDoubleBvLJetTags:probQCD',
      'pfDeepDoubleBvLJetTags:probHbb',
      'pfDeepDoubleCvLJetTags:probQCD',
      'pfDeepDoubleCvLJetTags:probHcc',
      'pfDeepDoubleCvBJetTags:probHbb',
      'pfDeepDoubleCvBJetTags:probHcc',
      'pfMassIndependentDeepDoubleBvLJetTags:probQCD',
      'pfMassIndependentDeepDoubleBvLJetTags:probHbb',
      'pfMassIndependentDeepDoubleCvLJetTags:probQCD',
      'pfMassIndependentDeepDoubleCvLJetTags:probHcc',
      'pfMassIndependentDeepDoubleCvBJetTags:probHbb',
      
      ## for DeepAK8
      'pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:bbvsLight',
      'pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ccvsLight',
      'pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:TvsQCD',
      'pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZHccvsQCD',
      'pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:WvsQCD',
      'pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZHbbvsQCD',
      ]
        )
## This is for modified MET, needed only for 2017 data

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD (
    process,
    isData = True, # false for MC
    fixEE2017 = True,
    fixEE2017Params = {'userawPt': True, 'ptThreshold':50.0, 'minEtaThreshold':2.65, 'maxEtaThreshold': 3.139} ,
    postfix = "ModifiedMET"
    )


##
## This is for Uncorrected MET
from RecoMET.METProducers.PFMET_cfi import pfMet
process.pfMet = pfMet.clone(src = "packedPFCandidates")
process.pfMet.calculateSignificance = False # this can't be easily implemented on packed PF candidates at the moment
## Uncorrected MET edns here
##

pvSource = 'offlineSlimmedPrimaryVertices'


bTagDiscriminators = [
    'pfJetBProbabilityBJetTags'
    ,'pfJetProbabilityBJetTags'
    ,'pfPositiveOnlyJetBProbabilityBJetTags'
    ,'pfPositiveOnlyJetProbabilityBJetTags'
    ,'pfNegativeOnlyJetBProbabilityBJetTags'
    ,'pfNegativeOnlyJetProbabilityBJetTags'
    ,'pfTrackCountingHighPurBJetTags'
    ,'pfTrackCountingHighEffBJetTags'
    ,'pfNegativeTrackCountingHighPurBJetTags'
    ,'pfNegativeTrackCountingHighEffBJetTags'
    ,'pfSimpleSecondaryVertexHighEffBJetTags'
    ,'pfSimpleSecondaryVertexHighPurBJetTags'
    ,'pfNegativeSimpleSecondaryVertexHighEffBJetTags'
    ,'pfNegativeSimpleSecondaryVertexHighPurBJetTags'
    ,'pfCombinedSecondaryVertexV2BJetTags'
    ,'pfPositiveCombinedSecondaryVertexV2BJetTags'
    ,'pfNegativeCombinedSecondaryVertexV2BJetTags'
    ,'pfCombinedInclusiveSecondaryVertexV2BJetTags'
    ,'pfPositiveCombinedInclusiveSecondaryVertexV2BJetTags'
    ,'pfNegativeCombinedInclusiveSecondaryVertexV2BJetTags'
    ,'softPFMuonBJetTags'
    ,'positiveSoftPFMuonBJetTags'
    ,'negativeSoftPFMuonBJetTags'
    ,'softPFElectronBJetTags'
    ,'positiveSoftPFElectronBJetTags'
    ,'negativeSoftPFElectronBJetTags'
    ,'pfDeepCSVJetTags:probb'
    ,'pfDeepCSVJetTags:probc'
    ,'pfDeepCSVJetTags:probudsg'
    ,'pfDeepCSVJetTags:probbb'
]


## Jet energy corrections

## For jet energy correction
if options.runOnMC:
	jetCorrectionsAK4CHS       = ('AK4PFchs', ['L1FastJet','L2Relative', 'L3Absolute'], 'None')
	jetCorrectionsAK4Puppi     = ('AK4PFPuppi', ['L2Relative', 'L3Absolute'], 'None')
	jetCorrectionsAK8CHS       = ('AK8PFchs', ['L1FastJet','L2Relative', 'L3Absolute'], 'None')
	jetCorrectionsAK8CHSL23    = ('AK8PFchs', ['L2Relative', 'L3Absolute'], 'None')
	jetCorrectionsAK8Puppi     = ('AK8PFPuppi', ['L2Relative', 'L3Absolute'], 'None')
	jetCorrectionLevelsFullCHS = ['L1FastJet', 'L2Relative', 'L3Absolute']
	jetCorrectionLevels23CHS   = ['L2Relative', 'L3Absolute']
	jetCorrectionLevelsPuppi   = ['L2Relative', 'L3Absolute']

	AK4JECTextFiles = [
		MCJEC+'_L1FastJet_AK4PFchs.txt',
		MCJEC+'_L2Relative_AK4PFchs.txt',
		MCJEC+'_L3Absolute_AK4PFchs.txt'
		]
	AK4JECUncTextFile = MCJEC+'_Uncertainty_AK4PFchs.txt'

	AK8JECTextFiles = [
		MCJEC+'_L1FastJet_AK8PFchs.txt',
		MCJEC+'_L2Relative_AK8PFchs.txt',
		MCJEC+'_L3Absolute_AK8PFchs.txt'
		]
	AK8JECUncTextFile = MCJEC+'_Uncertainty_AK8PFchs.txt'
	prunedMassJECTextFiles = [
		MCJEC+'_L2Relative_AK8PFchs.txt',
		MCJEC+'_L3Absolute_AK8PFchs.txt'
		]

	AK4PuppiJECTextFiles = [
		MCJEC+'_L2Relative_AK4PFPuppi.txt',
		MCJEC+'_L3Absolute_AK4PFPuppi.txt'
		]
	AK4PuppiJECUncTextFile = MCJEC+'_Uncertainty_AK4PFPuppi.txt'

	AK8PuppiJECTextFiles = [
		MCJEC+'_L2Relative_AK8PFPuppi.txt',
		MCJEC+'_L3Absolute_AK8PFPuppi.txt'
		]
	AK8PuppiJECUncTextFile = MCJEC+'_Uncertainty_AK8PFPuppi.txt'
else:
        jetCorrectionsAK4CHS       = ('AK4PFchs', ['L1FastJet','L2Relative', 'L3Absolute','L2L3Residual'], 'None')
	jetCorrectionsAK4Puppi     = ('AK4PFPuppi', ['L2Relative', 'L3Absolute','L2L3Residual'], 'None')
	jetCorrectionsAK8CHS       = ('AK8PFchs', ['L1FastJet','L2Relative', 'L3Absolute','L2L3Residual'], 'None')
	jetCorrectionsAK8CHSL23    = ('AK8PFchs', ['L2Relative', 'L3Absolute','L2L3Residual'], 'None')
	jetCorrectionsAK8Puppi     = ('AK8PFPuppi', ['L2Relative', 'L3Absolute','L2L3Residual'], 'None')
	jetCorrectionLevelsFullCHS = ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']
	jetCorrectionLevels23CHS   = ['L2Relative', 'L3Absolute','L2L3Residual']
	jetCorrectionLevelsPuppi   = ['L2Relative', 'L3Absolute','L2L3Residual']
	AK4JECTextFiles = [
		DATAJEC+'_L1FastJet_AK4PFchs.txt',
		DATAJEC+'_L2Relative_AK4PFchs.txt',
		DATAJEC+'_L3Absolute_AK4PFchs.txt',
		DATAJEC+'_L2L3Residual_AK4PFchs.txt'
		]
	AK4JECUncTextFile = DATAJEC+'_Uncertainty_AK4PFchs.txt'
	AK8JECTextFiles = [
		DATAJEC+'_L1FastJet_AK8PFchs.txt',
		DATAJEC+'_L2Relative_AK8PFchs.txt',
		DATAJEC+'_L3Absolute_AK8PFchs.txt',
		DATAJEC+'_L2L3Residual_AK8PFchs.txt'
		]
	AK8JECUncTextFile = DATAJEC+'_Uncertainty_AK8PFchs.txt'
	prunedMassJECTextFiles = [
		DATAJEC+'_L2Relative_AK8PFchs.txt',
		DATAJEC+'_L3Absolute_AK8PFchs.txt',
		DATAJEC+'_L2L3Residual_AK8PFchs.txt'
		]

	AK4PuppiJECTextFiles = [
		DATAJEC+'_L2Relative_AK4PFPuppi.txt',
		DATAJEC+'_L3Absolute_AK4PFPuppi.txt',
		DATAJEC+'_L2L3Residual_AK4PFPuppi.txt'
		]
	AK4PuppiJECUncTextFile = DATAJEC+'_Uncertainty_AK4PFPuppi.txt'

	AK8PuppiJECTextFiles = [
		DATAJEC+'_L2Relative_AK8PFPuppi.txt',
		DATAJEC+'_L3Absolute_AK8PFPuppi.txt',
		DATAJEC+'_L2L3Residual_AK8PFPuppi.txt'
		]
	AK8PuppiJECUncTextFile = DATAJEC+'_Uncertainty_AK8PFPuppi.txt'

from PhysicsTools.PatAlgos.tools.jetTools import *


NOTADDHBBTag=False


#-------------------------------------
from PhysicsTools.PatAlgos.tools.pfTools import *
## Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag(pvSource))



#### Add reclustered AK8 Puppi jet by Eiko


process.load('CommonTools/PileupAlgos/Puppi_cff')
process.puppi.candName       = cms.InputTag('packedPFCandidates')
process.puppi.vertexName     = cms.InputTag('offlineSlimmedPrimaryVertices')

from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox


### CA15Puppi
### do we still need this? I guess no.
jetToolbox( process, 'ca15', 'jetSequence', 'out', PUMethod='Puppi', miniAOD=options.useMiniAOD, runOnMC=options.runOnMC,
	    bTagDiscriminators=(bTagDiscriminators + ([] if NOTADDHBBTag else ['pfBoostedDoubleSecondaryVertexCA15BJetTags'])),
	    JETCorrPayload='AK8PFPuppi',JETCorrLevels=jetCorrectionLevelsPuppi,
	    subJETCorrPayload='AK4PFPuppi',subJETCorrLevels=jetCorrectionLevelsPuppi,
	    Cut='pt>120',
	    addSoftDrop=True,addSoftDropSubjets=True, betaCut=1.0, zCutSD=0.15,
	    addNsub=True )




## Jet Energy Resolution
process.patSmearedJets = cms.EDProducer("SmearedPATJetProducer",
    src = cms.InputTag("appliedRegJets"),

    enabled = cms.bool(True),  # If False, no smearing is performed

    rho = cms.InputTag("fixedGridRhoFastjetAll"),

    skipGenMatching = cms.bool(False),  # If True, always skip gen jet matching and smear jet with a random gaussian

    # Resolution and scale factors source.
    # Can be either from GT or text files
    # For GT: only 'algo' must be set
    # For text files: both 'resolutionFile' and 'scaleFactorFile' must point to valid files

    # Read from GT
    algopt = cms.string('AK4PFchs_pt'),
    algo = cms.string('AK4PFchs'),

    # Or from text files
    #resolutionFile = cms.FileInPath('path/to/resolution_file.txt'),
    #scaleFactorFile = cms.FileInPath('path/to/scale_factor_file.txt'),

    # Gen jet matching
    genJets = cms.InputTag("slimmedGenJets"),
    dRMax = cms.double(0.2),  # = cone size (0.4) / 2
    dPtMaxFactor = cms.double(3),  # dPt < 3 * resolution

    # Systematic variation
    # 0: Nominal
    # -1: -1 sigma (down variation)
    # 1: +1 sigma (up variation)
    variation = cms.int32(0),  # If not specified, default to 0

    seed = cms.uint32(37428479),  # If not specified, default to 37428479
    useDeterministicSeed = cms.bool(True),

    debug = cms.untracked.bool(False)
)




## Tau ID embedding 

from ExoPieElement.TreeMaker.runTauIdMVA import *
na = TauIDEmbedder(process, cms,
		   debug=True,
		   toKeep = ["2017v2"]
		   )
na.runTauID()

## adding payloads for Tau ID discriminator 

byIsolationMVArun2017v2DBoldDMwLTraw2017 = cms.string('byIsolationMVArun2017v2DBoldDMwLTraw2017'),
byVVLooseIsolationMVArun2017v2DBoldDMwLT2017 = cms.string('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017'),
byVLooseIsolationMVArun2017v2DBoldDMwLT2017 = cms.string('byVLooseIsolationMVArun2017v2DBoldDMwLT2017'),
byLooseIsolationMVArun2017v2DBoldDMwLT2017 = cms.string('byLooseIsolationMVArun2017v2DBoldDMwLT2017'),
byMediumIsolationMVArun2017v2DBoldDMwLT2017 = cms.string('byMediumIsolationMVArun2017v2DBoldDMwLT2017'),
byTightIsolationMVArun2017v2DBoldDMwLT2017 = cms.string('byTightIsolationMVArun2017v2DBoldDMwLT2017'),
byVTightIsolationMVArun2017v2DBoldDMwLT2017 = cms.string('byVTightIsolationMVArun2017v2DBoldDMwLT2017'),
byVVTightIsolationMVArun2017v2DBoldDMwLT2017 = cms.string('byVVTightIsolationMVArun2017v2DBoldDMwLT2017')


## For normal AK4 jets jet energy correction on top of miniAOD
from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
process.patJetCorrFactorsReapplyJECAK4 = updatedPatJetCorrFactors.clone(
	src = cms.InputTag("patSmearedJets"),
	levels = jetCorrectionLevelsFullCHS,
	payload = 'AK4PFchs' ) # Make sure to choose the appropriate levels and payload here!

from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
process.patJetsReapplyJECAK4 = updatedPatJets.clone(
	jetSource = cms.InputTag("patSmearedJets"),
	jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECAK4"))
  )

process.jetCorrSequenceAK4 = cms.Sequence( process.patJetCorrFactorsReapplyJECAK4 + process.patJetsReapplyJECAK4 )




### For normal AK8 jet energy correction on top of miniAOD
process.patJetCorrFactorsReapplyJECAK8 = updatedPatJetCorrFactors.clone(
	src = cms.InputTag("slimmedJetsAK8"),
	levels = jetCorrectionLevelsFullCHS,
	payload = 'AK8PFPuppi' ) # Make sure to choose the appropriate levels and payload here!

process.patJetsReapplyJECAK8 = updatedPatJets.clone(
	jetSource = cms.InputTag("slimmedJetsAK8"),
	jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECAK8"))
  )


process.jetCorrSequenceAK8 = cms.Sequence( process.patJetCorrFactorsReapplyJECAK8 + process.patJetsReapplyJECAK8 )



## For normal AK4Puppi jets jet energy correction on top of miniAOD
from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
process.patJetCorrFactorsReapplyJECAK4Puppi = updatedPatJetCorrFactors.clone(
	src = cms.InputTag("slimmedJetsPuppi"),
	levels = jetCorrectionLevelsPuppi,
	payload = 'AK4PFPuppi' ) # Make sure to choose the appropriate levels and payload here!

from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
process.patJetsReapplyJECAK4Puppi = updatedPatJets.clone(
	jetSource = cms.InputTag("slimmedJetsPuppi"),
	jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECAK4Puppi"))
  )

process.jetCorrSequenceAK4Puppi = cms.Sequence( process.patJetCorrFactorsReapplyJECAK4Puppi + process.patJetsReapplyJECAK4Puppi )


## For correcting pruned jet mass + CHS
process.patJetCorrFactorsReapplyJECForPrunedMass = updatedPatJetCorrFactors.clone(
	src = cms.InputTag("slimmedJetsAK8"),
	levels = jetCorrectionLevels23CHS,
	payload = 'AK8PFchs' ) # Make sure to choose the appropriate levels and payload here!

process.patJetsReapplyJECForPrunedMass = updatedPatJets.clone(
	jetSource = cms.InputTag("slimmedJetsAK8"),
	jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECForPrunedMass"))
	)

process.jetCorrSequenceForPrunedMass = cms.Sequence( process.patJetCorrFactorsReapplyJECForPrunedMass + process.patJetsReapplyJECForPrunedMass )




process.load('ExoPieElement.TreeMaker.TreeMaker_cfi')
process.tree.useJECText            = cms.bool(options.useJECText)
process.tree.THINjecNames          = cms.vstring(AK4JECTextFiles)
process.tree.THINjecUncName        = cms.string(AK4JECUncTextFile)
process.tree.FATprunedMassJecNames = cms.vstring(prunedMassJECTextFiles)
process.tree.FATjecNames           = cms.vstring(AK8PuppiJECTextFiles)
process.tree.FATjecUncName         = cms.string(AK8PuppiJECUncTextFile)
process.tree.AK4PuppijecNames      = cms.vstring(AK4PuppiJECTextFiles)
process.tree.AK4PuppijecUncName    = cms.string(AK4PuppiJECUncTextFile)
process.tree.AK8PuppijecNames      = cms.vstring(AK8PuppiJECTextFiles)
process.tree.AK8PuppijecUncName    = cms.string(AK8PuppiJECUncTextFile)
process.tree.CA15PuppijecNames     = cms.vstring(AK8PuppiJECTextFiles)
process.tree.CA15PuppijecUncName   = cms.string(AK8PuppiJECUncTextFile)
process.tree.fillCA15PuppiJetInfo  = cms.bool(True)


if options.useJECText:
	process.tree.THINJets      = cms.InputTag("patSmearedJets")
	process.tree.FATJets       = cms.InputTag("selectedUpdatedPatJets")#("slimmedJetsAK8")
	process.tree.FATJetsForPrunedMass       = cms.InputTag("slimmedJetsAK8")
	process.tree.AK4PuppiJets  = cms.InputTag("slimmedJetsPuppi")




## output file name 
#process.TFileService = cms.Service("TFileService",fileName = cms.string("ExoPieElementTuples.root"))
process.TFileService = cms.Service("TFileService",fileName = cms.string('$outputFileName'))


##Trigger Filter
process.trigFilter = cms.EDFilter('TrigFilter',
				  TrigTag = cms.InputTag("TriggerResults::HLT"),
				  TrigPaths = cms.vstring("HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60",
							  "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
							  "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight",
							  
							  "HLT_Ele27_WPTight_Gsf",
							  "HLT_Ele32_WPTight_Gsf_L1DoubleEG",
							  "HLT_Ele35_WPTight_Gsf",
							  
							  "HLT_IsoMu24",
							  "HLT_IsoMu27",
							  "HLT_IsoTkMu27",
							  "HLT_IsoTkMu24",
							  
							  "HLT_Photon200" ),
				  isMC_ = cms.bool(options.runOnMC)
				  )



process.appliedRegJets= cms.EDProducer('bRegressionProducer',
                                           JetTag=cms.InputTag("slimmedJets"),
                                           rhoFixedGridCollection = cms.InputTag('fixedGridRhoFastjetAll'),
                                           #bRegressionWeightfile= cms.untracked.string("/afs/cern.ch/work/d/dekumar/public/flashgg_setup/CMSSW_8_0_28/src/flashgg/MetaData/data/DNN_models/model-18"),
                                           y_mean = cms.untracked.double(1.0454729795455933) ,
                                           y_std = cms.untracked.double( 0.31628304719924927)
                                           )

if not options.useJECText:
	process.analysis = cms.Path(
		process.trigFilter
		*process.rerunMvaIsolationSequence
		*process.NewTauIDsEmbedded+
		process.egammaPostRecoSeq+
		process.appliedRegJets+ 
		process.fullPatMetSequenceModifiedMET+ 
		process.patSmearedJets+
		process.pfMet+
		process.jetCorrSequenceAK4+  ## only when using JEC text files
		process.jetCorrSequenceAK8+  ## only when using JEC text files
		process.jetCorrSequenceAK4Puppi+ ## only when using JEC text files
		process.jetCorrSequenceForPrunedMass+ ## only when using JEC text files
		process.tree
		)
else:
	process.analysis = cms.Path(
		process.trigFilter
		*process.rerunMvaIsolationSequence
		*process.NewTauIDsEmbedded+
		process.egammaPostRecoSeq+
		process.appliedRegJets+
		process.fullPatMetSequenceModifiedMET+
		process.patSmearedJets+
		process.pfMet+
		process.tree
		)


#print process.dumpPython()
