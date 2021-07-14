# Running the FMRIPREP container
Image: fmriprep.simg

This container allows us to open up an environment to run fmriprep.  
  
The `fmriprep` workflow takes as principal input the path of the dataset that is to be processed. The input dataset it required to be in valid BIDS format, must include at least one T1w structural image, and a BOLD series(this can be disabled with a flag). 

[Reference the docs](https://fmriprep.readthedocs.io/en/stable/usage.html)
### Command Template: <br>
fmriprep command
```
fmriprep [-h] [--version] [--skip_bids_validation]
                [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                [-t TASK_ID] [--echo-idx ECHO_IDX] [--nthreads NTHREADS]
                [--omp-nthreads OMP_NTHREADS] [--mem_mb MEM_MB] [--low-mem]
                [--use-plugin USE_PLUGIN] [--anat-only] [--boilerplate]
                [--ignore-aroma-denoising-errors] [-v] [--debug]
                [--ignore {fieldmaps,slicetiming,sbref} [{fieldmaps,slicetiming,sbref} ...]]
                [--longitudinal] [--t2s-coreg] [--bold2t1w-dof {6,9,12}]
                [--output-space {T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} [{T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} ...]]
                [--force-bbr] [--force-no-bbr]
                [--template {MNI152NLin2009cAsym}]
                [--output-grid-reference OUTPUT_GRID_REFERENCE]
                [--template-resampling-grid TEMPLATE_RESAMPLING_GRID]
                [--medial-surface-nan] [--use-aroma]
                [--aroma-melodic-dimensionality AROMA_MELODIC_DIMENSIONALITY]
                [--skull-strip-template {OASIS,NKI}]
                [--skull-strip-fixed-seed] [--fmap-bspline] [--fmap-no-demean]
                [--use-syn-sdc] [--force-syn] [--fs-license-file PATH]
                [--no-submm-recon] [--cifti-output | --fs-no-reconall]
                [-w WORK_DIR] [--resource-monitor] [--reports-only]
                [--run-uuid RUN_UUID] [--write-graph] [--stop-on-first-crash]
                [--notrack] [--sloppy]
                bids_dir output_dir {participant}
```
Common fmriprep command for NIBL
```
fmriprep [input directory] [output directory] \
    participant  \
    --participant-label [participant label]  \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 16 \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug \
    --resource-monitor --write-graph --stop-on-first-crash 
```

#### SDC and modifying the jsons 
The fmriprep documentation states, 'Data acquired to correct for B0 inhomogeneities can come in different forms. The current version of this standard considers four different scenarios. Please note that in all cases fieldmap data can be linked to a specific scan(s) it was acquired for by filling the IntendedFor field in the corresponding JSON file.....The IntendedFor field is optional and in case the fieldmaps do not correspond to any particular scans it does not have to be filled.'[BIDS](https://bids.neuroimaging.io/bids_spec.pdf)  
  
We found that we need to do this to get the SDC output from fmriprep.  
The script [fill_fmap_jsons](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/fmriprep/fill_fmap_jsons.py) is made to do this. It will take an input directory and fill in the relevant jsons. Currently it has to be given the input directory where the sub-*/ folders are held, and it will add each available functional for reference to the json. We can modify this to select only a single functional if needed.  
If you run into an error where you cannot modify them, please modify the permissions on the folders.  
  
Run Script
```
# change to the directory holding the script
cd /projects/niblab/bids_projects/code
# run the script --example below gives the Bevel BIDS directory
python fill_fmap_jsons.py -input /projects/niblab/bids_projects/Experiments/Bevel/Nifti
```  
Modify permissions
```
cd /projects/niblab/bids_projects/Experiments/Bevel/Nifti
chmod -R 775 .
```


### Examples

Opening fmriprep
```
# with the shell
singularity shell -B /projects/niblab/bids_projects:/home_dir /projects/niblab/bids_projects/Singularity_Containers/fmriprep.simg  

# with exec
singularity exec -B /projects/niblab/bids_projects:/home_dir /projects/niblab/bids_projects/Singularity_Containers/fmriprep.simg \
fmriprep [input directory] [output directory] \
    participant  \
    --participant-label [participant label]  \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 16 \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug \
    --resource-monitor --write-graph --stop-on-first-crash 

```

Running with shell  
```
sinteractive -m 99000
singularity shell -B /projects/niblab/bids_projects:/home_dir /projects/niblab/bids_projects/Singularity_Containers/fmriprep_5_2019.simg  
cd /home_dir 
fmriprep /home_dir/Experiments/Bevel/BIDS /home_dir/Experiments/Bevel/test \
    participant  \
    --participant-label 001 \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 16 \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-spaces MNI152Lin \
    -w /home_dir/Experiments/Bevel/test \
    --resource-monitor --write-graph --stop-on-first-crash 
```

Running batch processes
[Batch File](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/fmriprep/fmriprep_batch.job)
```
# edit batch file
# submit job
sbatch --array=1-10%10 fmriprep_batch.job
```
