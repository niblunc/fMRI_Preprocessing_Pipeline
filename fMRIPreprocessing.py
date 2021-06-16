"""
# fMRI preprocessing python module
# Author: Nichollette Acosta
# Orgnaization: NIBL @ UNC Chapel Hill

"""


import argparse
import os
import glob
import subprocess
# preprocessing object
# options: bids, fmriprep, skull stripping, fd check, mocos...
class fMRIPreprocessing:

    def __init__(self, bids, fmriprep, skull_strip, confounds, moco):
        self.bids = bids
        self.fmriprep = fmriprep
        self.skull_strip = skull_strip
        self.confounds = confounds
        self.moco = moco
        
        
    
    def fmriprep_quick_report(self, bids_path,fmriprep_path, sessions):

        sessions_missing={}
        sessions_found={}
        for ses in sessions: 

            bids_subject_list=[x.split("/")[-2] for x in 
                           glob.glob(os.path.join(bids_path, "sub-*/%s"%ses))]

            bids_subject_list=[x for x in bids_subject_list ]#if x not in remove_subs]

            fmriprep_folders=glob.glob(os.path.join(fmriprep_path, "sub-*/ses-*"))

            fprep_subject_list=[x.split("/")[-2] for x in fmriprep_folders if ses in x]

            fprep_missing = [x for x in bids_subject_list if x not in fprep_subject_list]

            sessions_found[ses]=fprep_subject_list
            sessions_missing[ses]=fprep_missing

        missing_list=[]
        for x in sessions_missing.values():
            for y in x:
                missing_list.append(y)

        missing_list=list(set(missing_list))  
        missing_list.sort()
        print('[INFO] missing subjects: ', missing_list)

        for ses in sessions_found:
            print("\n[INFO] %s subjects found (%s total): \n %s \n"%(ses, len(sessions_found[ses]), sessions_found[ses]))
            
            
            
            

class SDC:
    
    def __init__(self, bids_path,session):
        self.bids_path = bids_path
        self.session = session     
        
        
    def fill_jsons(self):

        subjects = glob.glob(os.path.join(self.bids_path, 'sub-*/%s'%self.session))
        
        for subDir in sorted(subjects):
            #initiate the data dictionary
            new_data = {"IntendedFor" : []}
            #grab all the functionals for the subject
            funcs=glob.glob(os.path.join(subDir, "func/*.nii.gz"))
            #fill in our data dictionary with the functionals
            for func in funcs:
                x = func.split("/")[-1]
                x = os.path.join("func",x)
                new_data["IntendedFor"].append(x)
            #get the json files we need to append data to
            jsons=glob.glob(os.path.join(subDir, "fmap/*.json"))
            #loop through jsons and edit each file
            for j in jsons:
                #print(new_data)
                #open the json file
                try:
                    with open(j) as f:
                        data = json.load(f)
                #update the data file with our new data
                    data.update(new_data)
                #add the new update to the json file
                    with open(j, 'w') as f:
                        json.dump(data, f, indent=2)
                except:
                    print("[INFO] can't edit file: ", j)
        print('[INFO] finished editing json files.')
                            