import glob
import os
import fnmatch
import subprocess
import argparse
import shutil


# Get subjects

def set_paths():
    print ("STARTING PROGRAM, GETTING VARIABLES....")
    global basedir
    global deriv_path
    global subjects
    #basedir=input("Enter your base directory input path: ")
    basedir="/projects/niblab/bids_projects/Experiments/bbx"
    #deriv_path=input("Enter your derivatives path: ")
    deriv_path=os.path.join(basedir, "derivatives")
    subjects = glob.glob("/projects/niblab/bids_projects/Experiments/bbx/fmriprep/sub-*")

# THEN COPY OUR NIFTI FILES FROM FMRIPREP INTO OUR ~/derivatives directory    
def move_anats():
    errors = []
    print ("STARTING THE MOVE FILES PROCESS.........")
    for sub_file in subjects:
        sub = sub_file.split("/")[-1]
        #print("SUBJECT >>>> %s \nSUBJECT FILE >>>> %s" %(sub, sub_file))
        #/single_subject_152_wf/anat_preproc_wf/skullstrip_ants_wf/t1_skull_strip
        fmriprep_path=os.path.join(sub_file, "ses-1", 'fmriprep_wf', 'single_subject_*','anat_preproc_wf/skullstrip_ants_wf/t1_skull_strip/*BrainExtractionBrain*nii.gz')
        anat_output_path=os.path.join(deriv_path,sub, 'ses-1', 'anat')
        #print("OUTPUT PATH: ", anat_output_path)
        #print("FMRIPREP_PATH: ", fmriprep_path)
        for file in glob.glob(fmriprep_path):
            try:
                shutil.copy(file, anat_output_path)
            except: #shutil.Error as error:
                #errors.extend(error.args[0])
                print(">>>>>>>>>>>>ERRROR")

    