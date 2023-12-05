"""log 文件自动解析结果，输出csv
>>> python -m scripts.log_parser --file logs/example.log --target_path \
    results/example.csv --thead ds gcn mlp lr sage ARI NMI ACC "Micro F1" "Macro F1" --refresh True
"""
import argparse
import copy
import re

from utils import csv2file

parser = argparse.ArgumentParser(prog='data handler',
                                 description='data handler')

parser.add_argument('--file',
                    type=str,
                    default='./logs/tmp.log',
                    help='data file path')
parser.add_argument('--target_path',
                    type=str,
                    default='./results/tmp.log',
                    help='results file path')
parser.add_argument('--thead',
                    type=str,
                    nargs='+',
                    default=None,
                    help='results file path')
parser.add_argument('--refresh',
                    type=bool,
                    default=False,
                    help='whether to clean target file')

args = parser.parse_args()

# pylint: disable=line-too-long
matrix_re = r"ARI:(\-*\d*\.*\d*e*\-*\d*)|NMI:(\-*\d*\.*\d*e*\-*\d*)|ACC:(\-*\d*\.*\d*e*\-*\d*)|Micro F1:(\-*\d*\.*\d*e*\-*\d*)|Macro F1:(\-*\d*\.*\d*e*\-*\d*)"
dic = []
with open(args.file, 'r', encoding='utf-8') as df:
    lines = df.readlines()
    entry = {}
    for line in lines:
        match = re.search("Cora|Citeseer|Pubmed|ACM|Flickr|BlogCatalog", line)
        if match is not None:
            entry['ds'] = match.group(0)
            # 修改以下内容为自身参数配置，参数间用'\t'间隔
            ls = line.split('\t')
            entry['gcn'] = f"{ls[2]} {ls[3]}".replace(match.group(0), '')
            entry['mlp'] = f"{ls[4]} {ls[5]}"
            entry['lr'] = ls[6]
            entry['sage'] = ls[7]

        match_metric = re.search(
            matrix_re,
            line,
        )
        match_metric_name = re.search(r"ARI|NMI|ACC|Micro F1|Macro F1", line)
        if match_metric is not None:
            entry[match_metric_name.group(0)] = match_metric.group(0).split(
                f"{match_metric_name.group(0)}:")[1]
            if match_metric_name.group(0) == 'Macro F1':
                dic.append(copy.deepcopy(entry))
csv2file(
    target_path=args.target_path,
    thead=args.thead,
    tbody=dic,
    is_dict=True,
    refresh=args.refresh,
)
