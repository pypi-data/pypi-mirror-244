"""Category statistics script
"""
import matplotlib.pyplot as plt

from utils import count_label
from utils import get_intra_class_edges
from utils import load_data
from utils.load_data import dgl_datasets
from utils.load_data import ogb_datasets

datasets = dgl_datasets + ogb_datasets
for ds in datasets:
    graph, label, _ = load_data(ds)
    edges = graph.edges()
    u, v = edges[0].numpy(), edges[1].numpy()

    label_cnt = count_label(label)
    intra_class_edges = get_intra_class_edges((u, v), label.numpy())
    intra_class_edges_per_node = {
        key: len(val) / label_cnt[key]
        for key, val in intra_class_edges.items()
    }
    statistical_res = list(zip(*intra_class_edges_per_node.items()))
    print(f"{ds}: {statistical_res}")

    plt.plot(list(statistical_res[0]), list(statistical_res[1]))
    if len(list(statistical_res[0])) < 20:
        plt.xticks(list(statistical_res[0]))

    plt.xlabel('community')
    plt.ylabel('edge num per node')
    plt.title('mean edge num per node in each community')

    plt.savefig(f'./results/{ds}.png')

    plt.clf()

# from utils import get_intra_class_mean_distance
# intra_class_mean_distance = get_intra_class_mean_distance(
#     torch.squeeze(model.get_embedding(), 0), label.numpy())
# print(intra_class_mean_distance)
