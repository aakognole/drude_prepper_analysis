import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MDAnalysis
from MDAnalysis.analysis.align import *
from MDAnalysis.analysis.rms import rmsd
from MDAnalysis.analysis.rms import RMSF
import os

system='cas9-sgrna-dna.proa'
sele = "segid PROA and not name H*"
psf = './nowat.psf'
dcd = './prod-nowat-proa.dcd' # DCD aligned w.r.t. segid PROA

if (os.path.exists('rmsf_%s.txt' % (system)) == False):
    u = MDAnalysis.Universe(psf,dcd)
    sel = u.select_atoms(sele)
    R = []
    for i in sel.residues.resids:
        res = sel.select_atoms('resid %d' % (i))
        rmsfer = RMSF(res, verbose=False).run(step=10)
        R.append((i, np.mean(rmsfer.rmsf), np.std(rmsfer.rmsf)))
#        print(i, np.mean(rmsfer.rmsf), np.std(rmsfer.rmsf))
    R = np.array(R)
    np.savetxt('rmsf_%s.txt' % (system), R, fmt="%5.3f")
else:
    print('Analysis available, only ploting the output again!')
    R = np.loadtxt('rmsf_%s.txt' % (system))

# plot for quick look
plt.figure()
plt.title(system)
plt.bar(np.arange(len(R[:,0])),R[:,1],yerr=R[:,2])
plt.xticks(np.arange(0,len(R[:,0]),int(len(R[:,0])/10)),np.arange(int(R[0,0]),int(R[-1,0])+1,int(len(R[:,0])/10)))
plt.ylabel('RMSF ($\AA$)')
plt.xlabel('Residue Number')
plt.tight_layout()
plt.savefig('rmsf_%s.png' % (system), dpi=300)
plt.close()

exit()
