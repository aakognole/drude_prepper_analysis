"""
Generated by CHARMM-GUI (http://www.charmm-gui.org)

openmm_run.py

This program is OpenMM running scripts written in python.

Correspondance: jul316@lehigh.edu or wonpil@lehigh.edu
Last update: March 29, 2017
"""

from __future__ import print_function
import argparse
import sys
import os

from omm_readinputs import *
from omm_readparams import *
from omm_vfswitch import *
from omm_barostat import *
from omm_restraints import *

from simtk.unit import *
from simtk.openmm import *
from simtk.openmm.app import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='inpfile', help='Input parameter file', required=True)
parser.add_argument('-p', dest='psffile', help='Input CHARMM PSF file', required=True)
parser.add_argument('-c', dest='crdfile', help='Input CHARMM CRD file', required=True)
parser.add_argument('-t', dest='toppar', help='Input CHARMM-GUI toppar stream file', required=True)
parser.add_argument('-b', dest='sysinfo', help='Input CHARMM-GUI sysinfo stream file (optional)', default=None)
parser.add_argument('-icrst', metavar='RSTFILE', dest='icrst', help='Input CHARMM RST file (optional)', default=None)
parser.add_argument('-irst', metavar='RSTFILE', dest='irst', help='Input restart file (optional)', default=None)
parser.add_argument('-ichk', metavar='CHKFILE', dest='ichk', help='Input checkpoint file (optional)', default=None)
parser.add_argument('-opdb', metavar='PDBFILE', dest='opdb', help='Output PDB file (optional)', default=None)
parser.add_argument('-orst', metavar='RSTFILE', dest='orst', help='Output restart file (optional)', default=None)
parser.add_argument('-ochk', metavar='CHKFILE', dest='ochk', help='Output checkpoint file (optional)', default=None)
parser.add_argument('-odcd', metavar='DCDFILE', dest='odcd', help='Output trajectory file (optional)', default=None)
args = parser.parse_args()

# Load parameters
print("Loading parameters")
inputs = read_inputs(args.inpfile)
params = read_params(args.toppar)
psf = read_psf(args.psffile)
crd = read_crd(args.crdfile)
if args.sysinfo:
    psf = read_box(psf, args.sysinfo)
else:
    psf = gen_box(psf, crd)

noc = 0
if noc:
    for a in psf.atom_list:
        a.charge = 0.0

# Build system
if inputs.vdw == 'Switch':
    system = psf.createSystem(params, nonbondedMethod=inputs.coulomb,
                              nonbondedCutoff=inputs.r_off*nanometers,
                              switchDistance=inputs.r_on*nanometers,
                              constraints=inputs.cons,
                              ewaldErrorTolerance=inputs.ewald_Tol)
    for force in system.getForces():
        if isinstance(force, NonbondedForce): force.setUseDispersionCorrection(False)
        if isinstance(force, CustomNonbondedForce) and force.getNumTabulatedFunctions() == 2:
            force.setUseLongRangeCorrection(False)
elif inputs.vdw == 'Force-switch':
    system = psf.createSystem(params, nonbondedMethod=inputs.coulomb,
                              nonbondedCutoff=inputs.r_off*nanometers,
                              constraints=inputs.cons,
                              ewaldErrorTolerance=inputs.ewald_Tol)
    system = vfswitch(system, psf, inputs)
elif inputs.vdw == 'LJPME':
    system = psf.createSystem(params, nonbondedMethod=inputs.coulomb,
                              nonbondedCutoff=inputs.r_off*nanometers,
                              constraints=inputs.cons,
                              ewaldErrorTolerance=inputs.ewald_Tol)

if inputs.pcouple == 'yes': system = barostat(system, inputs)
if inputs.rest == 'yes':    system = restraints(system, psf, crd, inputs)

integrator = DrudeLangevinIntegrator(inputs.temp*kelvin, inputs.fric_coeff/picosecond, inputs.drude_temp*kelvin, inputs.drude_fric_coeff/picosecond, inputs.dt*picoseconds)
integrator.setMaxDrudeDistance(inputs.drude_hardwall) # Drude Hardwall

# Set platform
platform = Platform.getPlatformByName('CUDA')
prop = dict(CudaPrecision='mixed')

# Build simulation context
simulation = Simulation(psf.topology, system, integrator, platform, prop)
simulation.context.setPositions(crd.positions)
if args.icrst:
    charmm_rst = read_charmm_rst(args.icrst)
    simulation.context.setPositions(charmm_rst.positions)
    simulation.context.setVelocities(charmm_rst.velocities)
    simulation.context.setPeriodicBoxVectors(charmm_rst.box[0], charmm_rst.box[1], charmm_rst.box[2])
if args.irst:
    with open(args.irst, 'r') as f:
        simulation.context.setState(XmlSerializer.deserialize(f.read()))
if args.ichk:
    with open(args.ichk, 'rb') as f:
        simulation.context.loadCheckpoint(f.read())

# Drude VirtualSites
simulation.context.computeVirtualSites()

# Calculate initial system energy
print("\nInitial system energy")
print(simulation.context.getState(getEnergy=True).getPotentialEnergy())
print('\n')

E = []
g = [1,2,4,8,16,32,64,128,256]
etype = ['BOND','ANGL','DIHE','UREY','IMPR','CMAP','NONB','DRUD','OTH1']
e = 0
for i in range(len(g)):
    e = e + simulation.context.getState(getEnergy=True, groups=g[i]).getPotentialEnergy().value_in_unit(kilocalories_per_mole)
    print(etype[i], simulation.context.getState(getEnergy=True, groups=g[i]).getPotentialEnergy().value_in_unit(kilocalories_per_mole))
    E.append((etype[i], simulation.context.getState(getEnergy=True, groups=g[i]).getPotentialEnergy().value_in_unit(kilocalories_per_mole)))

print("TOTE", e)
E.append(("TOTE", e))
print('\n')

print("BOND+DRUD %12.5f" % (E[0][1]+E[7][1]))
print("ANGL+UREY %12.5f" % (E[1][1]+E[3][1]))
print("DIHE+CMAP %12.5f" % (E[2][1]+E[5][1]))
print("IMPR %12.5f" % (E[4][1]))
print("ELEC+VDW %12.5f" % (E[6][1]))
print("TOTE %12.5f" % (E[9][1]))

exit()
