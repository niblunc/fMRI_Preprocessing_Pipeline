# Walkthrough BIDS

## Steps:  
1. Get heuristic file and bash script, or relevant command.....  
2. Submit process.......  
3. QC -
  * Run BIDS validation:  


      # run singularity container

  * Simple commands to check directory:  


       # change to bids directory -  
       i.e `cd /projects/niblab/bids_projects/Experiments/bbx/bids`  

  Then you can run these commands to quickly get some initial information:  

     # count attempted subjects formatted to bids:  
        `ls sub-*/[ses-*] | wc -l`  
     # good check is to count how many functional, `func/`, directories were created:  
        `ls sub-*/[ses-*]/func | wc -l`    


3. Check volume files and scan notes
5. Fill in `.json` files before running fmriprep, this enables fmriprep to run **Susceptibility Distortion Correction(SDC)**   
*NOTE-make sure to add permissions to bids directory or else phasediff json will not be edited.*  

        cd /projects/niblab/bids_projects/Experiments/bbx/bids  
        chmod -R 755 sub-*
Then you can locate the python scripts and run easily by passing in the bids path, can also specify session.  

        $ python json_fill.py --help
        usage: json_fill.py [-h] [-input IN] [-sess] [-sess_id SESS_ID]

        Fill in the jsons in BIDS for Susceptibility Distortion Correction(SDC)

        optional arguments:
        -h, --help        show this help message and exit
        -input IN         Enter input directory where sub-*/ folders are held
        -sess             Use flag if multiple sessions, if only specific session, use -sess_id flag instead
        -sess_id SESS_ID  Use flag if multiple sessions, if only specific session, use -sess_id flag instead

Then you have three options:
  * Run script for all available sessions:
        python json_fill.py -input /projects/niblab/bids_projects/Experiments/bbx/bids -sess
  * Run for specific session:
        python json_fill.py -input /projects/niblab/bids_projects/Experiments/bbx/bids -sess_id ses-1
  * Run for single study, no sessions:
        python json_fill.py -input /projects/niblab/bids_projects/Experiments/bbx/bids

6.
