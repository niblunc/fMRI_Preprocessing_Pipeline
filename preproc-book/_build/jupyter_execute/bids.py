#!/usr/bin/env python
# coding: utf-8

# # BIDS Example with BBX Data
# 
# This notebook is a walkthrough of the steps for processing BBX data into BIDS format.  
# Using the `heudiconv` tool in a Singularity container, the raw dicoms are converted into the BIDS format.  
# 

# In[1]:


"""
# import packages 
"""

import os, glob, shutil, sys
import ipywidgets as widgets
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import subprocess as sp
import seaborn as sns
from nilearn import image, plotting
from multiprocessing import Pool
from IPython.display import SVG, display
from datetime import date
from matplotlib import rcParams
import warnings


sys.path.append("/projects/niblab/go_through/jupyter_notebooks")
import fMRIPreprocessing

plt.rcParams['axes.titlepad'] = 15
plt.rcParams["figure.figsize"] = (20,15)

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('matplotlib', 'inline')


# ## Set Parameters

# In[2]:


"""
# Global Variables
"""

date = date.today()
study_folder_path="/projects/niblab/experiments/bbx"
data_folder_path= os.path.join(study_folder_path, "data")
report_folder_path= os.path.join(study_folder_path, "data/quality_analysis")
bids_data_path=os.path.join(study_folder_path, "data/bids")




sub_ids=[x.split("/")[-1] for x in glob.glob(os.path.join(study_folder_path,"data/bids/bids_trimmed/sub-*"))]
sessions=['ses-1', 'ses-2']

s1_dcm_subject_list=[x.split("/")[-2] for x in 
                   glob.glob(os.path.join(study_folder_path, "data/sourcedata/by_subject/sub-*/ses-1"))]

s2_dcm_subject_list=[x.split("/")[-2] for x in 
                   glob.glob(os.path.join(study_folder_path, "data/sourcedata/by_subject/sub-*/ses-2"))]


remove_subs=['sub-029', 'sub-047', 'sub-049', 'sub-069', 'sub-081', 'sub-094', 'sub-101',
             'sub-105', 'sub-106', 'sub-110', 'sub-113', 'sub-122', 'sub-125', 'sub-126', 
             'sub-139', 'sub-155', 'sub-158', 'sub-165']

s2_drop_subjects=["sub-003", 'sub-012','sub-016', 'sub-018',  "sub-020", "sub-024", "sub-025",'sub-026', 'sub-035',
                  "sub-052", 'sub-056', "sub-059", "sub-060", "sub-064","sub-074", "sub-076", "sub-077", 'sub-087',
                  'sub-108', "sub-147", "sub-150", "sub-167"]


# ---

# View available dicoms

# In[3]:


print("\n\n[INFO] %s session 1 dicoms: \n\n%s\n\n---"%(len(s1_dcm_subject_list),s1_dcm_subject_list))
print("\n\n[INFO] %s session 2 dicoms: \n\n%s\n\n---"%(len(s2_dcm_subject_list),s2_dcm_subject_list))


# ## Run BIDS batch

# In[7]:


"""
# BIDS Batch Method
"""
def run_bids_batch(job_file, sess, x,y,z, submit_job=False):
    # submit batch job
    if submit_job==True: 
        print(' '.join(['sbatch', '--array={}-{}%{}'.format(x, y, z), job_file, sess]))
        sp.run(['sbatch', '--array={}-{}%{}'.format(x, y, z), job_file, sess])
        print('[INFO] submitted bids job.')


# Set and pass in the command parameters to the batch method:  
# `sbatch -array={start_id}-{finish_id}%{z} {bids_job_file}`  
# **Set to `submit_job` to `True` if you want to submit and process batch job**

# In[4]:


# Set Parameters
bids_job_file=os.path.join("/projects/niblab/experiments/bbx/code/preprocessing/bids.job")
start_id=57
finish_id=57
z=1 # how many jobs to run
sess='1'
submit_job= True
# set to True when you want to run the file 

# single sub
run_bids_batch(bids_job_file,  sess,start_id, finish_id, z, submit_job)

#sub_ids=[ 8, 19, 21, 63, 77, 94, 108, 118, 128, 137, 146, 147]
# multiple sub
#for sub in sub_ids:
 #run_bids_batch(bids_job_file, sub, sess, sub, sub, 1, submit_job)


# ---

# ---  
# 
# ## SDC Setup
# We run this quick modification on BIDS before running FMRIPREPa by dding functional references to the bids fmap (`.json`) files. This enables suscpetibility distortion correction (sdc) results from FMRIPREP.    
# **If you get a `[INFO] can't edit file` error-**  
# - check your bids folder permission and make sure you have writable permissions.  
#     `chmod -R 775 {bids_data_folder}`
# 
# Code here: `/projects/niblab/jupyter_notebooks/fMRIPreprocessing.py`

# In[5]:


# run sdc prep module
run_sdc=True #change to True to tcall the command
# as input the module requires a path to the bids data, containing sub-xx folders, and a session id
if run_sdc==True:
    sdc = fMRIPreprocessing.SDC(bids_data_path+'/bids_trimmed', "ses-2")
    sdc.fill_jsons()


# ---  
# ## Quality Check 

# ---  
# ### Build Reports

# In[6]:


"""
# Build BIDS Report 

"""

def anat_plot(plot_filename, anat_img):
    # get anat file and save plot
    anat_plot=plotting.plot_anat(anat_img, title="%s_%s"%(subject,session),
         display_mode='ortho', dim=-1, draw_cross=False,
        annotate=False, output_file=plot_filename)

def plot_functionals(func_file):
    # Compute the voxel_wise mean of functional images across time.
    # Basically reducing the functional image from 4D to 3D
    mean_img = image.mean_img(func_file)
    filename=func_file.split("/")[-1].split(".")[0]

    plot_filename = os.path.join(report_folder_path,
                                   "%s_mean_img.png"%filename)            
            
    plot_img=plotting.plot_epi(mean_img, title=filename,
        display_mode='ortho', draw_cross=False,
        annotate=False, output_file=plot_filename)
          
            
def build_bids_report(write_files=False):
    
    
    print('[INFO] bids data folder: %s'%bids_data_path)
    #excel_file=os.path.join(report_folder_path, "bbx_preprocessing_report.xlsx")
    sessions=['ses-1', 'ses-2']
    dataframes=[]
    #writer = pd.ExcelWriter(excel_file, engine = 'xlsxwriter')
    logfile=open('/projects/niblab/experiments/bbx/data/quality_analysis/bad_volumes.log', 'a+')
    # loop through sessions
    for session in sessions:
        #print("\n[INFO] %s"%session)

        data_dict={} #initialize data dictionary for session

        # loop through subject set by subject
        for i in range(1,171):
            subject="sub-%s"%f'{i:03}'
            bids_folder=os.path.join(bids_data_path, subject,
                                    session)

           
            if subject not in data_dict:
                data_dict[subject] = {}

                
            #--
            # get anat file
            
            anat_imgs =glob.glob(os.path.join(bids_folder, "anat",
                   '%s_%s_T1w.nii.gz'%(subject, session)))

            #if os.path.exists(anat_img): 
                #plot_filename=os.path.join(report_folder_path, "%s_%s_anat.png"%(subject,session))
            data_dict[subject]["anat_file_ct"]=len(anat_imgs)
            #anat_plot(plot_filename, anat_img) #plot image

            # get fmap files
            
            fmap_magn_imgs =glob.glob(os.path.join(bids_folder, "fmap",
                   '%s_%s_magnitude[0-9].nii.gz'%(subject, session)))
            
            data_dict[subject]["fmap_magnitude_file_ct"]=len(fmap_magn_imgs)

            fmap_phase_imgs =glob.glob(os.path.join(bids_folder, "fmap",
                   '%s_%s_phasediff.nii.gz'%(subject, session)))
            data_dict[subject]["fmap_phasediff_file_ct"]=len(fmap_phase_imgs)

            
            # ---
            
            # get functional files and check their volume and plot images

            func_files=glob.glob(os.path.join(
                    bids_folder, "func/*.nii.gz" ))

            # --initialize variables --
            train_ct=0
            rest_ct=0
            if session == 'ses-2':
                rl_ct=0
            for func_file in func_files:
                task=func_file.split("/")[-1].split("_")[2]
                vol = sp.check_output(["fslnvols", func_file])
                vol=str(vol,'utf-8').strip("\n")

                if "resting" in task:
                    rest_ct+=1
                    var_name="%s_vol"%task
                    data_dict[subject][var_name]=vol
                    if vol != '212':
                        logfile.write("bad volume for %s %s %")
                    
                elif "rl" in task:
                    rl_ct+=1
                    run=func_file.split("/")[-1].split("_")[3]
                    var_name="%s_%s_vol"%(task,run)
                    data_dict[subject][var_name]=vol
                    
                elif "training" in task:
                    train_ct+=1
                    run=func_file.split("/")[-1].split("_")[3]
                    var_name="%s_%s_vol"%(task,run)
                    data_dict[subject][var_name]=vol
                    

            if session == 'ses-2':
                data_dict[subject]["rl_file_ct"]=rl_ct
            data_dict[subject]["train_file_ct"]=train_ct
            data_dict[subject]["rest_file_ct"]=rest_ct
            
        dataframe=pd.DataFrame(data_dict).T
        #dataframe.to_excel(writer, sheet_name="%s_bids"%session, index=False, header=False)
        dataframes.append(dataframe)
    print('[INFO] report building complete.')
    return dataframes;


# ### Run Report Generator

# In[7]:


"""
# BIDS Variables
"""

bids_data_path=os.path.join(data_folder_path, "bids/bids_trimmed")
report_folder_path=os.path.join(data_folder_path, 'quality_analysis')
bids_folders=glob.glob(os.path.join(bids_data_path, "sub-*/ses-*"))
bids_ses1=[x for x in bids_folders if 'ses-1' in x]
bids_ses2=[x for x in bids_folders if 'ses-2' in x]


# ---

# ### View Reports

# **Session 1**

# In[8]:


# build data report 
# -- if write_files=True, it will write out the report to an excel file
bids_data_path=os.path.join(data_folder_path, "bids/bids")
dataframes_orig=build_bids_report(write_files=False)


# In[9]:


s1_df=dataframes_orig[0]
s1_df.index.name = "patID"
s1_df.drop(remove_subs, inplace=True)


# In[10]:


#s1_df[s1_df.isna().any(axis=1)]
#s1_df.style.highlight_null('red')


# In[11]:


s2_df=dataframes_orig[1]
s2_df.index.name = "patID"
s2_df.drop(remove_subs+s2_drop_subjects, inplace=True)


# In[12]:


s2_df.style.highlight_null('red')


# ---

# BIDS **Trimmed** Data

# In[13]:


bids_data_path=os.path.join(data_folder_path, "bids/bids_trimmed")
dataframes_trim=build_bids_report(write_files=False)


# In[14]:


s1_df_trim=dataframes_trim[0]
s1_df_trim.index.name = "patID"
s1_df_trim.drop(remove_subs, inplace=True)


# In[15]:


#s1_df[s1_df.isna().any(axis=1)]
s1_df_trim.style.highlight_null('red')


# **Session 2**

# In[16]:


s2_df_trim=dataframes_trim[1]
s2_df_trim.index.name = "patID"
s2_df_trim.drop(remove_subs+s2_drop_subjects, inplace=True)


# In[17]:


s2_df_trim.style.highlight_null('red')


# In[18]:


s2_missing=[x for x in list(s2_df_trim[s2_df_trim.isna().any(axis=1)].index.values) if x not in remove_subs and x not in s2_drop_subjects]


# In[19]:


s2_missing


# In[20]:


s2_df_trim[s2_df_trim.isna().any(axis=1)]


# ---
# 

# ---

# ## Write Files

# In[22]:


from pandas import ExcelWriter


# In[17]:


pathT='/projects/niblab/experiments/bbx/data/quality_analysis/bbx_fmri_data_report.xlsx'
path='/projects/niblab/experiments/bbx/data/quality_analysis/bbx_fmri_data_report.xlsx'


# In[18]:


with pd.ExcelWriter(pathT, engine='xlsxwriter') as writer:    
    s1_df_trim.to_excel(writer, 'ses-1_bids')   
    s2_df_trim.to_excel(writer, 'ses-2_bids')   
    writer.save()  


# In[25]:


with pd.ExcelWriter(path, engine='xlsxwriter') as writer:    
    s1_df.to_excel(writer, 'ses-1_bids')   
    #s2_df.to_excel(writer, 'ses-2_bids')   
    writer.save()  


# In[27]:


new_excel=pd.read_excel(path, sheet_name="ses-1_bids")


# In[28]:


new_excel.head()


# Session 2

# Missing Dicoms: 
# - session 2: 
#     sub-003, sub-012, sub-018, sub-026, 

# ## View Functionals

# In[29]:


def display(sub_id='sub-001', sess_id='ses-1'):
    print("[INFO] viewing report for %s"%sub_id)
    path=os.path.join(data_folder_path,
                      'quality_analysis/bids_pngs/%s*%s*.png'%(sub_id,sess_id))
    if not glob.glob(path):
        print("[INFO] no data found")
    else:
        for file in glob.glob(path):
            #print(file)
            try:
                img = mpimg.imread(file)
                plt.imshow(img)
                plt.show()
            except:
                pass



# In[30]:


"""
# Run BIDS .png viewer widget 
"""
sub_ids.sort()
w= widgets.Select(options=sub_ids)
widgets.interactive(display, sub_id=sub_ids, sess_id=sessions)


# In[44]:


def print_report():
    
    bids_s1_ids=list(s1_df_trim.index.values)
    bids_s2_ids=list(s2_df.index.values)
    
    early_drop=['sub-029', 'sub-047', 'sub-049', 'sub-069', 'sub-081', 'sub-094', 'sub-101',
             'sub-105', 'sub-106', 'sub-110', 'sub-113', 'sub-122', 'sub-125', 'sub-126', 
             'sub-139', 'sub-155', 'sub-158', 'sub-165']
    
    
    #scan2_drops =[ "sub-147", "sub-150" ]
    
    s1_dcm_ids=[x.split("/")[-2] for x in 
                   glob.glob(os.path.join(data_folder_path, "sourcedata/by_subject/sub-*/ses-1"))]

    s2_dcm_ids=[x.split("/")[-2] for x in 
                   glob.glob(os.path.join(data_folder_path, "sourcedata/by_subject/sub-*/ses-2"))]

    
    
    s1_good_ids=[x for x in bids_s1_ids if x not in early_drop]
    s2_good_ids=[x for x in bids_s2_ids if x not in early_drop]# and x not in scan2_drops]
    
    s2_mia_ids=[x for x in s2_dcm_ids if x not in bids_s2_ids]
    
    
    
    #print("[INFO] %s session 1 dicom subjects found."%len(s1_dcm_ids))
    print("[INFO] %s bids subject folders found for session 1."%len(s1_good_ids))
    print("[INFO] session-1 subjects: \n\n %s \n"%s1_good_ids)
    
    
    #print("[INFO] %s session 2 dicom subjects found."%len(s2_dcm_ids))
    print("[INFO] %s session 2 bids folders "%len(s2_good_ids))
    print("[INFO] session-2 subjects: \n\n %s \n"%s2_good_ids)
    #print("[INFO] subjects missing: ", missing_s2_subs)


    
    
    


# In[45]:


print_report()


# In[35]:


s1_df.index.values


# ---
