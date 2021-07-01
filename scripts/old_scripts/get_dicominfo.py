import glob, os 
import argparse
import subprocess


def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description='Run Heudiconv Drypass')
    parser.add_argument('-in',dest='INDIR',
                        default=False, help='enter directory where the sub-*/ directories are found')
    parser.add_argument('-out',dest='OUT',
                        default=False, help='enter directory where you want the output to go')
    parser.add_argument('-ext',dest='EXT',
                        default=False, help='enter dicom extension (IMA or dcm)')


    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
        

        
# get parameters         
set_parser() 

SUBS = glob.glob(os.path.join(arglist['INDIR'], 'sub-*'))
ids = []
for sub_dir in SUBS:
    sub_id = sub_dir.split("/")[-1]
    ids.append(sub_id)
    
sub_string = ' '.join(ids)
# grab dicominfo.tsv file by running heudiconv command --aka "DRY PASS"
inpath = "/test"+arglist['INDIR']+"/{subject}/*"+arglist['EXT']
outpath = "/test"+arglist["OUT"]
heudiconv_cmd = "singularity exec -B /:/test /projects/niblab/bids_projects/Singularity_Containers/heudiconv.simg heudiconv -d %s -s %s -f /test/projects/niblab/bids_projects/Heuristic_Files/convertall.py -c none -o %s"%(inpath, sub_string, outpath)
#print(newpath)
print(heudiconv_cmd)
print("STARTING RUN.....")
run_batch=subprocess.Popen(["sbatch", "/projects/niblab/bids_projects/Heudiconv_drypass/drypass.job", heudiconv_cmd])

