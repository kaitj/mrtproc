import os
import sys

from nilearn import plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

subj = sys.argv[1]          # subjid
conn_fpath = sys.argv[2]    # Path to connectivity matrix
phase = sys.argv[3]         # pre/postop
gra_user = sys.argv[4]      # graham user 

# Load schaefer atlas networks 
schaefer_labels = "/project/6050199/cfmm-bids/Peters/pre_post_tle_connectivity/denoise_pre_post_tle/resources/schaefer_2018/Schaefer2018_300Parcels_7Networks_order.txt"

df_networks = pd.read_csv(schaefer_labels, sep="\t", header=None,
                           names=['lbl', 'network', 'x', 'y', 'z', '_'])

networks7 = list()
for network in df_networks.network:
    hemi = network.split("_")[1]
    net = network.split("_")[2]
    networks7.append(f"{hemi}_{net}")
    
df_networks['net7'] = networks7
net7_names = df_networks['net7'].unique()

# Get network connectivity (first load Schaefer connectivity)
subj_conn = np.loadtxt(conn_fpath)
subj_conn[subj_conn < 5] = 0 
n_rois = subj_conn.shape[0]
net_conn = np.zeros((len(net7_names), len(net7_names)))

for i,net_i in enumerate(net7_names):
    for j,net_j in enumerate(net7_names):
        i_mask = df_networks['net7'] == net_i
        j_mask = df_networks['net7'] == net_j
        
        mask_rows = np.zeros(subj_conn.shape, dtype='bool')
        mask_cols = np.zeros(subj_conn.shape, dtype='bool')

        mask_rows[i_mask, :] = True
        mask_cols[:, j_mask] = True
        mask = mask_rows & mask_cols
        
        net_conn[i,j] = subj_conn[mask].mean()

# Plot connectivity matrix 
fig = plt.figure(figsize=(4, 4))
plotting.plot_matrix(np.log10(subj_conn.T), figure=fig, tri="diag", colorbar=False,
                     vmin=-4, vmax=4)

np.savetxt(conn_fpath, subj_conn.T)
fpath, fname = os.path.split(conn_fpath)
fig.savefig(f"{fpath}/{fname.split('.')[0]}.png")

        
# Plot Yeo 7 network matrix 
fig = plt.figure(figsize=(4, 4))
plotting.plot_matrix(np.log10(net_conn.T), figure=fig, tri="diag", colorbar=False,
                     vmin=-4, vmax=4, labels=net7_names)


fname = f"{subj}_space-T1w_desc-schaefer_network-Yeo7_conn"
np.savetxt(f"{fpath}/{fname}.csv", net_conn.T)
fig.savefig(f"{fpath}/{fname}.png")
