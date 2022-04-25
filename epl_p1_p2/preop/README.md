# pre_post_tle_connectivity 

_Any paths shown here are from Graham_ 

- tle3T_phase1 symlinked entire folder
- tle3T_phase2 symlinked anat + func folders; dwi folders created, extracted out `b=1300` shell from `run-01`

```
for subj in `cat subjects.txt`; do singularity exec $SINGULARITY_MRT dwiextract -nthreads 1 -singleshell -shells 0,1300 -fslgrad ${fpath}.bvec ${fpath}.bval -export_grad_fsl ${subj}/dwi/${subj}_acq-multiband_run-01_b1300_dwi.bvec ${subj}/dwi/${subj}_acq-multiband_run-01_b1300_dwi.bval ${fpath}.nii.gz ${subj}/dwi/${subj}_acq-multiband_run-01_b1300_dwi.nii.gz -force; done

```
_where `subjects.txt` contains participant ids from phase 2 and `fpath` contains the directory path and file (without extension) in `/project/ctb-akhanf/cfmm-bids/Peters/...`

## Prepdwi
Changes made to `prepdwi` for preprocessing can be found in the following locations:
[Phase1](https://github.com/kaitj/prepdwi/tree/mtaylor_tle_phase1)