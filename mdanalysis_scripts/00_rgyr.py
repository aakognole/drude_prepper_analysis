import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MDAnalysis as mda

system='cas9-sgrna-dna.proa'
sele='segid PROA'
pdb='nowat.pdb' # pdb at 0 ns
dcd='prod-nowat-proa.dcd'

u = mda.Universe(pdb,dcd)
sel = u.select_atoms(sele)
R = []
for ts in u.trajectory:
    rg = sel.radius_of_gyration()
    R.append((ts.frame/100, rg))
R = np.array(R)
np.savetxt('rgyr_%s.txt' % (system), R, fmt="%s")

# plot for quick look
plt.figure()
plt.title(system)
plt.plot(R[:,0], R[:,1], 'b', lw=1.5)
plt.xlabel('Time (ns)')
plt.ylabel("RGYR ($\AA$)")
plt.grid()
plt.savefig('rgyr_%s.png' % (system), dpi=300)

exit()

