#!/usr/bin/env python
# coding: utf-8

# ---
# # Volume Trim 
# This method uses the `fslroi` command to trim volumes from a file.  
# For input the method expects an outpath and a functional file. Currently the code below runs the method when passed the volume trim flag, and it is cutting 4 volumes. Please check directory paths for your unique data.  
#   
# `$ fslroi
# Usage: fslroi <input> <output> <xmin> <xsize> <ymin> <ysize> <zmin> <zsize>
#        fslroi <input> <output> <tmin> <tsize>
#        fslroi <input> <output> <xmin> <xsize> <ymin> <ysize> <zmin> <zsize> <tmin> <tsize>
# Note: indexing (in both time and space) starts with 0 not 1! Inputting -1 for a size will set it to the full image extent for that dimension.`

# In[1]:


import os, glob
import subprocess as sp
from shutil import copytree
from multiprocessing import Pool


# In[2]:


bids_trimmed_path='/projects/niblab/experiments/bbx/data/bids/bids_trimmed'
bidstrim_sub_folders=glob.glob(os.path.join(bids_trimmed_path, "sub-*"))
bidstrim_sub_folders.sort()


# In[3]:


bidstrim_sub_folders[1:2]


# In[4]:


bids_path='/projects/niblab/experiments/bbx/data/bids/bids'
bids_sub_folders=glob.glob(os.path.join(bids_path, "sub-*"))
bids_sub_folders.sort()


# In[3]:


# Copy Folders 0
new_basepath='/projects/niblab/experiments/bbx/data/bids/bids_trimmed'
session='ses-2'

for sub_folder in bids_sub_folders:
    subject=sub_folder.split("/")[-1]
    origpath=os.path.join(sub_folder)#, session)
    #print(origpath)
    newpath=os.path.join(new_basepath, subject)#, session)
    #print(newpath)
    if os.path.exists(origpath+'/ses-2'):
        if not os.path.exists(newpath+'/ses-2'):
            print(origpath+'/ses-2', newpath+'/ses-2')
            copytree(origpath+'/ses-2', newpath+'/ses-2')
    
    
    


# In[5]:


def volume_trim(func):
    """
    # FSL Volume Trimming 
    """
    func_outpath=os.path.join(sub_folder, '%s/func'%(session))
    filename=func.split("/")[-1].split(".")[0]
    fslroi_output=os.path.join(func_outpath, filename+".nii.gz")
    fslroi_input=func
    logf = open("/projects/niblab/experiments/bbx/code/trim_data.log", "a+")
    
    fslnvols_cmd=['fslnvols', fslroi_input, '&']
    #print(' '.join(fslnvols_cmd))
    
    process=sp.run(' '.join(fslnvols_cmd),  shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    vol = process.stdout
    if "229" in vol:
        pass
    if "233" in vol:
        fslroi_cmd=['fslroi', fslroi_input, fslroi_output, '4', '-1']
        print(' '.join(fslroi_cmd))
    
        try:
            process=sp.run(' '.join(fslroi_cmd),  shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
            output = process.stdout
        except Exception as e:
            logf.write("Failed to trim file {0}: {1}\n".format(str(func), str(e)))
    #print('[INFO] ', output)
    
    


# In[6]:



brainx=False
vol_trim=True
for sub_folder in bidstrim_sub_folders:
    subject=sub_folder.split("/")[-1]

    for session in ['ses-1', 'ses-2']:

        #print('[INFO] ', func_outpath)
        if brainx==True:
            # all runs
            bids_funcs=glob.glob(os.path.join(
                                    sub_folder,
                                    session, "func/*task-training*.nii.gz"))
        
            bids_funcs.sort()  
            
            for func in bids_funcs:            
                brainX(func, func_outpath)
                
            print("[INFO] completed brain extraction.")
  
        if vol_trim==True:
            
            #preproc_funcs=glob.glob(os.path.join(data_path,
            #   "preprocessed/%s/%s/func/*training*rn-*brain.nii.gz"%(subject, session)))
            
            funcs=glob.glob(os.path.join(sub_folder, "%s/func/*training*run-*.nii.gz"%session))
            
            # restrict to our bids data instead of fmriprep
            funcs=[x for x in funcs if '-preproc' not in x] #if "preproc" not in x]

            funcs.sort()
            
            agents=5
            chunksize=4
                
                
            with Pool(processes=agents) as pool:
                result = pool.map(volume_trim, funcs)
            #for func in funcs:
                
            
                #volume_trim(func_outpath, func, run_cmd=True)y
print("[INFO] completed volume trim.") 

            
                


# In[ ]:


vol_trim(subject="sub-001")


# ### Notes:  
# 
# > Add notes/trouble-shooting for the errros in the logfile     

# ---
