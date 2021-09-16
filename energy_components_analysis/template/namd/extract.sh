tail -n 50 namd_energy.out | grep "ENERGY:" | awk '{printf "BOND %f\nANGLE+UREY %f\nDIHE+CMAP %f\nIMPR %f\nELEC %f\nVDW %f\nTOTAL %f\n",$3,$4,$5,$6,$7,$8,$12}'
