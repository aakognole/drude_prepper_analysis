import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import MDAnalysis as mda
import numpy as np
from MDAnalysis.analysis.rms import rmsd
import os

system='cas9-sgrna-dna.proa'
sele="segid PROA and name C CA N"
pdb="nowat.pdb" # pdb at 0 ns
dcd="merged_nowat_PROA.dcd" # DCD aligned w.r.t. PROA

if (os.path.exists('rmsd_%s.txt' % (system)) == False):
    u = mda.Universe(pdb,pdb,dcd) # repeat pdb so that it is counted as first frame
    ref = mda.Universe(pdb)
    rna = u.select_atoms(sele)
    refrna = ref.select_atoms(sele)
    RMSD = []
    for ts in u.trajectory:
        R = rmsd(rna.positions, refrna.positions)
        RMSD.append((ts.frame/100, R))
        #print(ts.frame, R)
    RMSD = np.array(RMSD)
    np.savetxt('rmsd_%s.txt' % (system), RMSD, fmt='%s')
else:
    print('Analysis available, only ploting the output again!')
    RMSD = np.loadtxt('rmsd_%s.txt' % (system))

# plot for quick look    
plt.figure()
plt.title(system)
plt.plot(RMSD[:,0], RMSD[:,1], 'b', lw=1.5, label="BB RMSD")
plt.xlabel("Time (ns)")
plt.ylabel("RMSD ($\AA$)")
plt.legend()
plt.grid()
plt.savefig('rmsd_%s.png' % (system), dpi=300)

exit()
