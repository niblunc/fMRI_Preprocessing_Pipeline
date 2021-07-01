import glob, os 
import argparse
import pandas as pd 

def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description='bids conversion')
    parser.add_argument('-in',dest='INDIR',
                        default=False, help='enter directory where the sub-*/ directories are found')
    parser.add_argument('-subj',dest='SUBJ',
                        default=False, help='enter subject to look at')



    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
        
    
set_parser()

DICOM_TSV_PATH = os.path.join(arglist['INDIR'], ".heudiconv/%s/info/dicominfo.tsv"%arglist["SUBJ"])

TSV = pd.read_csv(DICOM_TSV_PATH, sep='\t', header=None)
TSVA = TSV[[2, 6, 7, 8, 9, 13, 14]]
TSVA.columns = ['series_id', 'dim1', 'dim2', 'dim3', 'dim4', 'is_motion_corrected', 'is_derived']
print(TSVA)

