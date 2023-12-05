"""Statistic Scripts
python -m scripts.statistic --models=pca_kmeans,vgae_kmeans
"""
import argparse
import os
import re
import subprocess

from utils import refresh_file
from utils import tab_printer

parser = argparse.ArgumentParser(
    prog='EAGLE Graph Clustering Statistical Scripts',
    description='Statistical Scripts Parameters for Graph Clustering')

parser.add_argument(
    '--datasets',
    type=str,
    default='Cora,Citeseer',
    help='Datasets used in the experiments, separated by comma')
parser.add_argument(
    '--models',
    type=str,
    default='dgi_kmeans,vgae_kmeans',
    help='Models need to be run in the experiments, separated by comma')
parser.add_argument('--gpu',
                    type=int,
                    default=0,
                    help='ID of gpu used by cuda')
parser.add_argument(
    '--target_path',
    type=str,
    default="results/statistic.csv",
    help='Target file path to save the experiment results. Defaults to None.')
parser.add_argument('--times',
                    type=int,
                    default=3,
                    help='Running times. Defaults to 3.')

args = parser.parse_args()
tab_printer(args)

# set gpu
gpu = args.gpu

cwd = os.path.abspath(
    f'{os.path.dirname(os.path.realpath(__file__))}').replace('/scripts', '')

datasets = args.datasets.split(',')

target_path = os.path.join(cwd, args.target_path)

# customize models
custom_models = args.models.split(',')

# if custom_models is None, run all models
models = re.findall(
    re.compile(r"\[--target_path TARGET_PATH\].*\{(.*)\}"),
    str(subprocess.check_output([
        'python', 'train.py', '-h'
    ])))[0].split(',') if len(custom_models) == 0 else custom_models

# clear target file in advance. if different shell scripts use\
#  the same target file, commented this line and refresh the file on your own
refresh_file(target_path)

for _ in range(args.times):
    for dataset in datasets:
        for model in models:
            subprocess.call(
                f'python train.py --dataset={dataset} --not_set_seed\
                    --gpu={gpu} --target_path={target_path} {model}',
                shell=True,
                cwd=cwd)
