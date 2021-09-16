import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

dp = []

resnames = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'HSD', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']


resnames = ['ALA','ILE', 'LEU', 'PHE', 'PRO', 'VAL']
for res in resnames:
    print(res)
    df = pd.read_csv('%s.txt' % (res), sep=' ')
    df.dropna(inplace=True)
    df = df[(df != 0).all(1)]
    d = df.to_numpy()
    m = np.mean(d[:,3])
    s = np.std(d[:,3])
    df2 = pd.read_csv('c36.%s.txt' % (res), sep=' ')
    df2.dropna(inplace=True)
    df2 = df2[(df2 != 0).all(1)]
    d2 = df2.to_numpy()
    m2 = np.mean(d2[:,3])
    s2 = np.std(d2[:,3])
    dp.append((res,m,s))
    plt.figure(figsize=(1.4,2.0))
    plt.title("%s\n$\mu$ = %5.3f\n$\sigma$ = %5.3f" % (res,m,s), family="Arial", size='8', weight='bold')
    plt.ylim((0,2))
    plt.hist(d[:,3], bins=50, range=(max(0,m-5*s),m+5*s), density=True, stacked=True, orientation='horizontal', color='xkcd:green')
    plt.hist(d2[:,3], bins=50, range=(max(0,m2-5*s2),m2+5*s2), density=True, stacked=True, orientation='horizontal', color='xkcd:black', alpha=0.4)
    #plt.hist(d[:,3], bins=100, range=(0,2), orientation='horizontal', color='xkcd:green')
    #plt.hist(d2[:,3], bins=100, range=(0,2), orientation='horizontal', color='xkcd:black', alpha=0.4)
    #plt.hist(d[:,3], bins=50, range=(0,15), density=True)
    plt.ylabel('Dipole Moment (Debyes)', family="Arial", size='8', weight='bold')
    plt.xticks(family="Arial", size='8', weight='bold')
    plt.yticks([0,1,2], family="Arial", size='8', weight='bold')
    plt.tight_layout(rect=(0,0,1.075,1.075))
    #plt.tight_layout()
    plt.savefig('%s.aasc_dp.png' % (res), dpi=300)
    plt.close()

resnames = ['CYS', 'MET', 'SER', 'THR', 'TRP', 'TYR']
for res in resnames:
    print(res)
    df = pd.read_csv('%s.txt' % (res), sep=' ')
    df.dropna(inplace=True)
    df = df[(df != 0).all(1)]
    d = df.to_numpy()
    m = np.mean(d[:,3])
    s = np.std(d[:,3])
    df2 = pd.read_csv('c36.%s.txt' % (res), sep=' ')
    df2.dropna(inplace=True)
    df2 = df2[(df2 != 0).all(1)]
    d2 = df2.to_numpy()
    m2 = np.mean(d2[:,3])
    s2 = np.std(d2[:,3])
    dp.append((res,m,s))
    plt.figure(figsize=(1.4,2.0))
    plt.title("%s\n$\mu$ = %5.3f\n$\sigma$ = %5.3f" % (res,m,s), family="Arial", size='8', weight='bold')
    plt.ylim((0,2))
    plt.hist(d[:,3], bins=50, range=(max(0,m-5*s),m+5*s), density=True, stacked=True, orientation='horizontal', color='xkcd:green')
    plt.hist(d2[:,3], bins=50, range=(max(0,m2-5*s2),m2+5*s2), density=True, stacked=True, orientation='horizontal', color='xkcd:black', alpha=0.4)
    #plt.hist(d[:,3], bins=50, range=(0,15), density=True)
    plt.ylabel('Dipole Moment (Debyes)', family="Arial", size='8', weight='bold')
    plt.xticks(family="Arial", size='8', weight='bold')
    plt.yticks([0,1,2,3,4,5], family="Arial", size='8', weight='bold')
    plt.tight_layout(rect=(0,0,1.075,1.075))
    #plt.tight_layout()
    plt.savefig('%s.aasc_dp.png' % (res), dpi=300)
    plt.close()

resnames = ['ASN', 'ASP', 'GLN', 'HSD']
for res in resnames:
    print(res)
    df = pd.read_csv('%s.txt' % (res), sep=' ')
    df.dropna(inplace=True)
    df = df[(df != 0).all(1)]
    d = df.to_numpy()
    m = np.mean(d[:,3])
    s = np.std(d[:,3])
    df2 = pd.read_csv('c36.%s.txt' % (res), sep=' ')
    df2.dropna(inplace=True)
    df2 = df2[(df2 != 0).all(1)]
    d2 = df2.to_numpy()
    m2 = np.mean(d2[:,3])
    s2 = np.std(d2[:,3])
    dp.append((res,m,s))
    plt.figure(figsize=(1.2,2.0))
    plt.title("%s\n$\mu$ = %5.3f\n$\sigma$ = %5.3f" % (res,m,s), family="Arial", size='8', weight='bold')
    plt.ylim((3,8))
    plt.hist(d[:,3], bins=50, range=(max(0,m-5*s),m+5*s), density=True, stacked=True, orientation='horizontal', color='xkcd:green')
    plt.hist(d2[:,3], bins=50, range=(max(0,m2-5*s2),m2+5*s2), density=True, stacked=True, orientation='horizontal', color='xkcd:black', alpha=0.4)
    #plt.hist(d[:,3], bins=50, range=(0,15), density=True)
    plt.ylabel('Dipole Moment (Debyes)', family="Arial", size='8', weight='bold')
    plt.xticks(family="Arial", size='8', weight='bold')
    plt.yticks([3,4,5,6,7,8], family="Arial", size='8', weight='bold')
    plt.tight_layout(rect=(0,0,1.075,1.075))
    #plt.tight_layout()
    plt.savefig('%s.aasc_dp.png' % (res), dpi=300)
    plt.close()

resnames = ['ARG', 'GLU', 'LYS']
for res in resnames:
    print(res)
    df = pd.read_csv('%s.txt' % (res), sep=' ')
    df.dropna(inplace=True)
    df = df[(df != 0).all(1)]
    d = df.to_numpy()
    m = np.mean(d[:,3])
    s = np.std(d[:,3])
    df2 = pd.read_csv('c36.%s.txt' % (res), sep=' ')
    df2.dropna(inplace=True)
    df2 = df2[(df2 != 0).all(1)]
    d2 = df2.to_numpy()
    m2 = np.mean(d2[:,3])
    s2 = np.std(d2[:,3])
    dp.append((res,m,s))
    plt.figure(figsize=(1.2,2.0))
    plt.title("%s\n$\mu$ = %5.3f\n$\sigma$ = %5.3f" % (res,m,s), family="Arial", size='8', weight='bold')
    plt.ylim((4,14))
    plt.hist(d[:,3], bins=50, range=(max(0,m-5*s),m+5*s), density=True, stacked=True, orientation='horizontal', color='xkcd:green')
    plt.hist(d2[:,3], bins=50, range=(max(0,m2-5*s2),m2+5*s2), density=True, stacked=True, orientation='horizontal', color='xkcd:black', alpha=0.4)
    #plt.hist(d[:,3], bins=50, range=(0,15), density=True)
    plt.ylabel('Dipole Moment (Debyes)', family="Arial", size='8', weight='bold')
    plt.xticks(family="Arial", size='8', weight='bold')
    plt.yticks([4,6,8,10,12,14], family="Arial", size='8', weight='bold')
    plt.tight_layout(rect=(0,0,1.075,1.075))
    #plt.tight_layout()
    plt.savefig('%s.aasc_dp.png' % (res), dpi=300)
    plt.close()

dp = np.array(dp)
np.savetxt('dipole.txt', dp, fmt="%s")
