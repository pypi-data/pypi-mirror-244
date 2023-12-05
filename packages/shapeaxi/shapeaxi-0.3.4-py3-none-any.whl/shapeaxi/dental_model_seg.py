import argparse
import os
from argparse import Namespace
import torch
import pandas as pd
from torch.utils.data import DataLoader
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import sys
from tqdm import tqdm
import vtk
import numpy as np

from . import saxi_eval, post_process, saxi_predict, saxi_nets, utils
from .saxi_folds import bcolors, get_argparse_dict
from .saxi_dataset import SaxiDataset
from .saxi_transforms import UnitSurfTransform


def main(args):
    print(bcolors.INFO, "Start evaluation of the model", bcolors.ENDC)
    
    if args.model is None:
        out_channels = 34
        model = saxi_nets.DentalModelSeg()
    else:
        model = args.model

    # Check if the input is a vtk file or a csv file
    if args.csv:
        df = pd.read_csv(args.csv)
        # saxi_predict_args = get_argparse_dict(saxi_predict.get_argparse())
        # saxi_predict_args['csv'] = args.csv
        # saxi_predict_args['model'] = model
        # saxi_predict_args['nn'] = "SaxiSegmentation"
        # saxi_predict_args['out'] = args.out
        # saxi_predict_args = Namespace(**saxi_predict_args)
        # fname = os.path.basename(args.csv)
        # out_prediction = os.path.join(saxi_predict_args.out, os.path.basename(args.model), fname.replace(".csv", "_prediction" + ".csv"))
        # saxi_predict.main(saxi_predict_args)

        class_weights = None
        out_channels = 34
        # MONAI = getattr(saxi_nets, args.nn)
        # model = MONAI.load_from_checkpoint(args.model)
        ds = SaxiDataset(df, mount_point = args.mount_point, transform=RandomRotation(), surf_column="surf")
        dataloader = DataLoader(ds, batch_size=1, num_workers=args.num_workers, persistent_workers=True, pin_memory=True)
        device = torch.device('cuda')
        model.to(device)
        model.eval()
        softmax = torch.nn.Softmax(dim=2)

        with torch.no_grad():
            for idx, batch in tqdm(enumerate(dataloader), total=len(dataloader)):
                # The generated CAM is processed and added to the input surface mesh (surf) as a point data array
                V, F, CN = batch
                V = V.cuda(non_blocking=True)
                F = F.cuda(non_blocking=True)
                CN = CN.cuda(non_blocking=True).to(torch.float32)
                x, X, PF = model((V, F, CN))
                x = softmax(x*(PF>=0))
                P_faces = torch.zeros(out_channels, F.shape[1]).to(device)
                V_labels_prediction = torch.zeros(V.shape[1]).to(device).to(torch.int64)
                PF = PF.squeeze()
                x = x.squeeze()

                for pf, pred in zip(PF, x):
                    P_faces[:, pf] += pred

                P_faces = torch.argmax(P_faces, dim=0)
                faces_pid0 = F[0,:,0]
                V_labels_prediction[faces_pid0] = P_faces
                surf = ds.getSurf(idx)
                V_labels_prediction = numpy_to_vtk(V_labels_prediction.cpu().numpy())
                V_labels_prediction.SetName(args.array_name)
                surf.GetPointData().AddArray(V_labels_prediction)
                output_fn = os.path.join(args.out, df["surf"][idx])
                output_fn = output_fn.replace("./", "")
                out_dir = os.path.dirname(output_fn)

                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)

                utils.Write(surf , output_fn, print_out=False)

            out_dir = os.path.join(args.out, os.path.basename(args.model))

            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            data = {
                "surf": df["surf"],
                "pred": [os.path.join(args.out, df["surf"][idx]) for idx in range(len(df))]
            }

    elif args.vtk:
        # If it is a vtk file, we run these lines, the changes are in the last lines to save the data
        fname = os.path.basename(args.vtk)
        df = pd.DataFrame([{"surf": args.vtk, "out": args.out}])
        ds = SaxiDataset(df,args.mount_point, transform=UnitSurfTransform(), surf_column="surf")
        dataloader = DataLoader(ds, batch_size=1, num_workers=args.num_workers, persistent_workers=True, pin_memory=True)
        device = torch.device('cuda')
        model.to(device)
        model.eval()
        softmax = torch.nn.Softmax(dim=2)

        with torch.no_grad():
            for idx, batch in tqdm(enumerate(dataloader), total=len(dataloader)):
                # The generated CAM is processed and added to the input surface mesh (surf) as a point data array
                V, F, CN = batch
                V = V.cuda(non_blocking=True)
                F = F.cuda(non_blocking=True)
                CN = CN.cuda(non_blocking=True).to(torch.float32)
                x, X, PF = model((V, F, CN))
                x = softmax(x*(PF>=0))
                P_faces = torch.zeros(out_channels, F.shape[1]).to(device)
                V_labels_prediction = torch.zeros(V.shape[1]).to(device).to(torch.int64)
                PF = PF.squeeze()
                x = x.squeeze()

                for pf, pred in zip(PF, x):
                    P_faces[:, pf] += pred

                P_faces = torch.argmax(P_faces, dim=0)
                faces_pid0 = F[0,:,0]
                V_labels_prediction[faces_pid0] = P_faces
                surf = ds.getSurf(idx)
                V_labels_prediction = numpy_to_vtk(V_labels_prediction.cpu().numpy())
                V_labels_prediction.SetName(args.array_name)
                surf.GetPointData().AddArray(V_labels_prediction)


                #Post Processing
                # start with gum
                post_process.RemoveIslands(surf, V_labels_prediction, 33, 500,ignore_neg1 = True) 

                for label in tqdm(range(out_channels),desc = 'Removing islands'):
                    post_process.RemoveIslands(surf, V_labels_prediction, label, 200,ignore_neg1 = True) 

                # CLOSING OPERATION
                #one tooth at a time
                for label in tqdm(range(out_channels),desc = 'Closing operation'):
                    post_process.DilateLabel(surf, V_labels_prediction, label, iterations=2, dilateOverTarget=False, target=None) 
                    post_process.ErodeLabel(surf, V_labels_prediction, label, iterations=2, target=None) 

                if not os.path.exists(args.out):
                    os.makedirs(args.out)        


                if args.fdi == 1:
                    surf = ConvertFDI(surf)

                if args.segmentation_crown:
                    # Isolate each label
                    surf_point_data = surf.GetPointData().GetScalars(args.array_name) 
                    labels = np.unique(surf_point_data)
                    
                    for label in tqdm(labels, desc = 'Isolating labels'):
                        thresh_label = post_process.Threshold(surf, args.array_name ,label-0.5,label+0.5)
                        if (args.fdi==0 and label != 33) or(args.fdi==1 and label !=0):
                            output_teeth = os.path.join(args.out, f'{os.path.splitext(fname)[0]}_id_{label}.vtk')
                            # utils.Write(thresh_label,f'{out_basename}_id_{label}.vtk',print_out=False) 
                            utils.Write(thresh_label,output_teeth,print_out=False) 
                        else:
                        # gum
                            output_teeth = os.path.join(args.out, f'{os.path.splitext(fname)[0]}_gum.vtk')
                            # utils.Write(thresh_label,f'{out_basename}_gum.vtk',print_out=False) 
                            utils.Write(thresh_label,output_teeth,print_out=False) 
                    # all teeth 
                    no_gum = post_process.Threshold(surf,args.array_name ,33-0.5,33+0.5,invert=True)
                    output_teeth = os.path.join(args.out, f'{os.path.splitext(fname)[0]}_all_teeth.vtk')
                    utils.Write(no_gum,output_teeth,print_out=False)
                    print(bcolors.SUCCESS,"Each teeth are saved", bcolors.ENDC)

                if args.overwrite: 
                    # If the overwrite argument is true, the original file is overwritten
                    output_fn = os.path.join(args.mount_point, f"{os.path.splitext(fname)[0]}_prediction.vtk")
                    utils.Write(surf, output_fn, print_out=False)
                    os.remove(os.path.join(args.mount_point,args.vtk))
                    print(bcolors.SUCCESS,f"Saving results to {output_fn}", bcolors.ENDC)
                else:
                    output_fn = os.path.join(args.out, f"{os.path.splitext(fname)[0]}_prediction.vtk")
                    utils.Write(surf , output_fn, print_out=False)
                    print(bcolors.SUCCESS,f"Saving results to {output_fn}", bcolors.ENDC)



# Add 'array_name' argument to specify the name of the output array
def get_argparse():
    parser = argparse.ArgumentParser(description='Evaluate classification result')
    parser.add_argument('--model', type=str, help='Path to the model', default=None)
    parser.add_argument('--vtk', type=str, help='Path to your vtk file', default=None)
    parser.add_argument('--csv', type=str, help='Path to your csv file', default=None)
    parser.add_argument('--out', type=str, help='Output directory', default="./prediction")
    parser.add_argument('--mount_point', type=str, help='Mount point for the dataset', default="./")
    parser.add_argument('--num_workers', type=int, help='Number of workers for loading', default=4)
    parser.add_argument('--segmentation_crown', help='Isolation of each different tooth in a specific vtk file', default=False)
    parser.add_argument('--array_name', type=str, help = 'Predicted ID array name for output vtk', default="PredictedID")
    parser.add_argument('--fdi', type=int, help = 'numbering system. 0: universal numbering; 1: FDI world dental Federation notation', default=0)
    parser.add_argument('--overwrite', help='Overwrite existing file', default=False)


    if '--vtk' in sys.argv and '--csv' in sys.argv:
        parser.error("Only one of --vtk or --csv should be provided, not both.")

    return parser

def cml():
    parser = get_argparse()
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cml()
