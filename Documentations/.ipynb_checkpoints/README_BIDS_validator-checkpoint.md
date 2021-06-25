# BIDS Validator

Image: bids_validator.simg  
Location: /projects/niblab/bids_projects/Singularity_Containers 

### Workflow: <br>
Log onto RENCI --> Start Singularity shell --> Validate BIDS dataset

    BIDS-validator command:
          $ bids-validator {data_directory}


#### Example:

Validate Bevel:
```
cd /projects/niblab/bids_projects
sinteractive
# note how I append the ~/Bevel directory to our container
singularity shell -B /projects/niblab/bids_projects/Experiments/Bevel:/test Singularity_Containers/bids_validator.simg
bids-validator /test/BIDS

# to get out of container
exit
# to get out of sinteractive 
exit

```
