import sys
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

##############
# Var parser #
##############
options = VarParsing.VarParsing ('standard')
options.register('inputFile',
#                 '/pnfs/desy.de/cms/tier2/store/user/fvazzole/powheg/crab_ZToEE_NLOQCD_LOEW__1_1000/240125_144036/0000/events_1.lhe',
                 'root://dcache-cms-xrootd.desy.de://pnfs/desy.de/cms/tier2/store/user/fvazzole/powheg/crab_ZToEE_NLOQCD_LOEW__1_1000/240125_144036/0000/events_1.lhe',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "input LHE file name")

options.register ('outputFile',
                  'events_1.root', 
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "output ROOT file name")

options.register('seed', 
                 1,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int, 
                 "Seed value")

if(hasattr(sys, "argv")):
  options.parseArguments()
#  print(options)

##################
# Main processor #
##################
process = cms.Process('NANOGEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic50ns13TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('PhysicsTools.NanoAOD.nanogen_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring(options.inputFile)
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/smp-22-010-qed-fsr-cmssw/python/customLHE__Pythia8_no_MPI_Photos__NanoGEN.py nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:' + options.outputFile),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    ExternalDecays = cms.PSet(
        Photospp = cms.untracked.PSet(
            forceBremForDecay = cms.PSet(
                Wm = cms.vint32(0, -24),
                Wp = cms.vint32(0, 24),
                Z = cms.vint32(0, 23),
                parameterSets = cms.vstring(
                    'Z', 
                    'Wp', 
                    'Wm'
                )
            ),
            parameterSets = cms.vstring(
                'setExponentiation', 
                'setInfraredCutOff', 
                'setMeCorrectionWtForW', 
                'setMeCorrectionWtForZ', 
                'setMomentumConservationThreshold', 
                'setPairEmission', 
                'setPhotonEmission', 
                'setStopAtCriticalError', 
                'suppressAll', 
                'forceBremForDecay'
            ),
            setExponentiation = cms.bool(True),
            setInfraredCutOff = cms.double(1e-07),
            setMeCorrectionWtForW = cms.bool(False),
            setMeCorrectionWtForZ = cms.bool(False),
            setMomentumConservationThreshold = cms.double(0.1),
            setPairEmission = cms.bool(False),
            setPhotonEmission = cms.bool(True),
            setStopAtCriticalError = cms.bool(False),
            suppressAll = cms.bool(True)
        ),
        parameterSets = cms.vstring('Photospp')
    ),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring(
            'pythia8CommonSettings', 
            'pythia8CP5Settings', 
            'processParameters'
        ),
        processParameters = cms.vstring(
            'SpaceShower:pTmaxMatch = 2', 
            'TimeShower:pTmaxMatch = 2', 
            'ParticleDecays:allowPhotonRadiation = on', 
            'TimeShower:QEDshowerByL = off', 
            'TimeShower:QEDshowerByOther = off', 
            'BeamRemnants:hardKTOnlyLHE = on', 
            'BeamRemnants:primordialKThard = 2.225001', 
            'SpaceShower:dipoleRecoil = 1', 
            'PartonLevel:MPI = off', 
            'HadronLevel:all = off'
        ),
        pythia8CP5Settings = cms.vstring(
            'Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:ecmPow=0.03344', 
            'MultipartonInteractions:bProfile=2', 
            'MultipartonInteractions:pT0Ref=1.41', 
            'MultipartonInteractions:coreRadius=0.7634', 
            'MultipartonInteractions:coreFraction=0.63', 
            'ColourReconnection:range=5.176', 
            'SigmaTotal:zeroAXB=off', 
            'SpaceShower:alphaSorder=2', 
            'SpaceShower:alphaSvalue=0.118', 
            'SigmaProcess:alphaSvalue=0.118', 
            'SigmaProcess:alphaSorder=2', 
            'MultipartonInteractions:alphaSvalue=0.118', 
            'MultipartonInteractions:alphaSorder=2', 
            'TimeShower:alphaSorder=2', 
            'TimeShower:alphaSvalue=0.118', 
            'SigmaTotal:mode = 0', 
            'SigmaTotal:sigmaEl = 21.89', 
            'SigmaTotal:sigmaTot = 100.309', 
            'PDF:pSet=LHAPDF6:NNPDF31_nnlo_as_0118'
        ),
        pythia8CommonSettings = cms.vstring(
            'Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on'
        )
    ),
    comEnergy = cms.double(13000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)


process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.nanoAOD_step = cms.Path(process.nanogenSequence)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path).insert(0, process.ProductionFilterSequence)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nanogen_cff
from PhysicsTools.NanoAOD.nanogen_cff import customizeNanoGEN 

#call to customisation function customizeNanoGEN imported from PhysicsTools.NanoAOD.nanogen_cff
process = customizeNanoGEN(process)

# End of customisation functions

# Customisation from command line
process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=options.seed
process.genWeightsTable.maxPdfWeights=1000
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
