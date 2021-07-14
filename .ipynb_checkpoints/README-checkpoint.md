# fMRI Preprocessing Pipeline

![](images/preproc.png)

# Running Singularity Containers
This README contains details for running the currently available Singularity containers.

Log into your HPC:

        RENCI:

        $ ssh -XY your_account@ht4.renci.org
        $ {your_password}


Change to the directory holding your containers:
        $ cd /projects/niblab/bids_projects/Singularity_Containers


To run Singularity Containers:

There are various ways to run a singularity container. For the labs purpose I've currently been using an interactive <br> shell, this gives us access to the environment within the container we have created and flexibility in testing and executing our commands.


      Before running any singularity commands we have to run the sinteractive shell:

          $ sinteractive

          --for large processes increase memory size
          $ sinteractive -m 2400


Here is the main template of running the singularity shell. See how we use the '-B' flag to bind our data directory to the containers directory. Without this we will not have access to our directories. Note that the container directory has been defined during the containers development and is unique for each container.  

          $ singularity shell -B {our_directory}:{container_directory} {image}



      Available Containers and their container directory:

              - heudiconv.simg                /test
              - bids_validator                /test
              - fmriprep_container.simg       /mydirectory


#### Examples:

BIDS Converter with Heudiconv <br>
  Image: heudiconv.simg

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
          $ cd /test
          $ ls


BIDS Validator <br>
  Image: bids_validator.simg

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/bids_validator.simg
          $ cd /test
          $ ls


fMRI Prep<br>
  Image: fmriprep_container.simg

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/mydirectory Singularity_Containers/fmriprep_container.simg
          $ cd /mydirectory
          $ ls

# BIDS  
![](images/bids_flow.png)  
## Steps:  
1. Setup heuristic file and bash heudiconv command script  
2. Submit process  
3. Quality check
  * Run BIDS validation check
  * Check for expected files
  * Volume check
  * Go through scan notes


4. To run **Susceptibility Distortion Correction(SDC)**  add functional file reference to the `fieldmap/*.json` files before running fmriprep, this enables fmriprep  
*NOTE-make sure there are correct permissions to the bids directory or else the phasediff json will not be edited.*  
To do so change directory to the folder. On most systemts the following command is safe:
```
chmod -R 755 sub-*  
```

Then you can locate the python scripts and run easily by passing in the bids path, can also specify session.  

        $ python json_fill.py --help
        usage: json_fill.py [-h] [-input IN] [-sess] [-sess_id SESS_ID]

        Fill in the jsons in BIDS for Susceptibility Distortion Correction(SDC)

        optional arguments:
        -h, --help        show this help message and exit
        -input IN         Enter input directory where sub-*/ folders are held
        -sess             Use flag if multiple sessions, if only specific session, use -sess_id flag instead
        -sess_id SESS_ID  Use flag if multiple sessions, if only specific session, use -sess_id flag instead
Three Examples running SDC setup:
  > Run script for all available sessions  

        python json_fill.py -input /projects/niblab/bids_projects/Experiments/bbx/bids -sess  

  > Run for specific session  

        python json_fill.py -input /projects/niblab/bids_projects/Experiments/bbx/bids -sess_id ses-1

  > Run for single study, no sessions

        python json_fill.py -input /projects/niblab/bids_projects/Experiments/bbx/bids


## BIDS Conversion with heudiconv   
The heudiconv converter is packaged inside a Singularity container we can open and run to convert our data into BIDS format.

Image: `/projects/niblab/singularity_images/heudiconv0.9.0.sif`  
Container Bind directory: `/work_dir`
### Workflow: <br>
> Log into RENCI &#8594; Singularity shell &#8594; Run commands

    $ singularity
    $ singularity shell -B /projects/niblab:/work_dir /projects/niblab/singularity_images/heudiconv0.9.0.sif

    $ heudiconv -b -d {input_directory} -s {SUBJECT} -ss {SESSION} -f {heuristic_file} -c dcm2niix -b  -o {output_directory}


The **heuristic_file** : A unique file of keys we must provide that tells how the files are to be converted. We use the information from our dicominfo.txt to fill in our keys.


#### Examples

> Example 1: getting the `dicominfo.tsv` file

        $ heudiconv -d Data/ChocolateData/{subject}/{session}/Dicoms/dicoms/*/*dcm -s sub-001 \
        -ss wave2 -f convertall.py -c none -o /output/EricData/pre-bids_files

> Example 2: converting a single subject with the shell

        $ cd /projects/niblab/bids_projects
        $ sinteractive
        $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
        $ cd /test
        $ heudiconv -d Data/ChocolateData/{subject}/{session}/Dicoms/dicoms/*/*dcm -s sub-001 \
        -ss wave2 -f eric_conversion.py -c dcm2niix -o output/EricData/ses-wave2


  > Example: Use `exec` to run conversion  

        $ sinteractive
        $ singularity exec -B /:/test /projects/niblab/bids_projects/Singularity_Containers/heudiconv.simg \
        heudiconv -d /test/projects/niblab/bids_projects/raw_data/continuing_studies/BBx/ses-{session}/{subject}/*dcm \
        -f /test/projects/niblab/bids_projects/Heuristic_Files/test_heuristic.py -c dcm2niix \
        -o  /test/projects/niblab/bids_projects/raw_data/continuing_studies/BBx/test -s sub-065 -ss 1

> Example: Converting all subjects  

        To convert multiple subjects we can create a simple script that loops through our subjects.  

## BIDS Validator

Image: `/projects/niblab/singularity_images/bids-validator.sif`  
Container Bind directory: `/data_folder`

### Workflow: <br>
> Log onto RENCI &#8594; Start Singularity shell &#8594; Validate BIDS dataset

    singularity
    singularity shell -B /projects/niblab:/data_folder /projects/niblab/singularity_images/bids-validator.sif  

    BIDS-validator command:
    bids-validator {data_directory}


#### Example:

Validate Bevel bids folder  
<br>
Start sinteractive
```
sinteractive
```   
Open Singularity container  
*--note how I append the ~/bevel directory to our container folder with the -B flag*    
```
singularity shell -B /projects/niblab/experiments:/work_dir /projects/niblab/singularity_images/bids-validator.sif  
```  
Run validation command
```
bids-validator /work_dir/bevel
```
To exit a Singularity container  
```
$ exit
```  
To exit out of sinteractive  
```
$ exit
```


# FMRIPREP

![](images/fmriprep_pipeline.png)
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


## FSL Models
![](images/fsleyes_crop.png)  
