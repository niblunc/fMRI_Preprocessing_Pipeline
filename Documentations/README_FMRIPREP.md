# Running the FMRIPREP container
Image: fmriprep.simg

This container allows us to open up an environment to run fmriprep.  
  
The `fmriprep` workflow takes as principal input the path of the dataset that is to be processed. The input dataset it required to be in valid BIDS format, must include at least one T1w structural image, and a BOLD series(this can be disabled with a flag). 

[Reference the docs](https://fmriprep.readthedocs.io/en/stable/usage.html)
### Command Template: <br>
fmriprep command: 
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


  * Notes:\
    -- heuristic_file: Unique file of keys we must provide that tells how the files are to be converted. \
          We use the information from our dicominfo.txt to fill in our keys.


#### Examples

    Example: getting the dicominfo.tsv file

          $ heudiconv -d Data/{subject}/{session}/Dicoms/dicoms/*/*dcm -s Eric_Data \
          -ss wave2 -f convertall.py -c none -o /output/EricData/pre-bids_files

    Example: converting a single subject

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
          $ cd /test
          $ heudiconv -d Data/{subject}/{session}/Dicoms/dicoms/*/*dcm -s Eric_Data \
          -ss wave2 -f eric_conversion.py -c none -o output/EricData/ses-wave2

    Example: Converting all subjects
             To convert multiple subjects we can create a simple script that loops through our subjects.


          $ cd /projects/niblab/bids_projects
          $ sinteractive -m 24000
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
          $ cd /test
          $ bash scripts/SugarMama_BIDS_conversion.sh

Refer to, <i>SugarMama_BIDS_conversion.sh</i>, for a template and further explanation of converting multiple subjects.
