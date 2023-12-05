"""
training method and args definition
"""
# pylint: disable=unused-import
import time

import scipy.sparse as sp

from egc.model import AGC
from egc.model import AGCN
from egc.model import age_cluster
from egc.model import ClusterNet
from egc.model import ComE
from egc.model import CommunityGAN
from egc.model import ContrastiveClustering
from egc.model import DAEGC
from egc.model import DANMF
from egc.model import DFCN
from egc.model import DGIKmeans
from egc.model import DGL_GAEKmeans
from egc.model import DGL_VGAEKmeans
from egc.model import GALA
from egc.model import GDCL
from egc.model import GMIKmeans
from egc.model import IDEC
from egc.model import MNMF
from egc.model import MVGRL
from egc.model import pca_kmeans
from egc.model import SDCN
from egc.model import SEComm
from egc.model import SENetKmeans
from egc.model import SGCKmeans
from egc.model import SUBLIME
from egc.model import VGAECD
from egc.model import VGAEKmeans
from egc.module import agm_pretrain
from egc.module import kmeans_pretrain
from egc.utils import csv2file
from egc.utils import get_undireced_motifs
from egc.utils import load_data
from egc.utils import parse_all_args
from egc.utils import set_device
from egc.utils import set_seed
from egc.utils.evaluation import evaluation

if __name__ == "__main__":
    args = parse_all_args()
    param_keys = list(vars(args).keys())
    param_values = list(vars(args).values())

    device = set_device(args.gpu)

    set_seed(args.seed)

    # Load Dataset for Graph Clustering
    graph, label, n_clusters = load_data(
        dataset_name=args.dataset,
        directory=args.dir,
    )
    n_nodes = graph.num_nodes()
    features = graph.ndata["feat"]
    adj_csr = graph.adj_external(scipy_fmt="csr")
    adj = graph.adj()
    edges = graph.edges()
    features_lil = sp.lil_matrix(features)

    start_time = time.time()
    res = []
    if args.model == "pca_kmeans":
        res = pca_kmeans(
            X=features,
            n_components=args.dim,
            n_clusters=n_clusters,
        )
    elif args.model == "gae_kmeans":
        model = DGL_GAEKmeans(
            epochs=args.epochs,
            n_clusters=n_clusters,
            fead_dim=features.shape[1],
            n_nodes=features.shape[0],
            hidden_dim1=args.hidden1,
            dropout=args.dropout,
            lr=args.lr,
            early_stop=args.early_stopping_epoch,
            activation=args.activation,
        )
        model.fit(
            adj_csr=adj_csr,
            features=features,
            device=device,
        )
        res = model.get_memberships()
    elif args.model == "vgae_kmeans":
        # model = DGL_VGAEKmeans(
        #     epochs=args.epochs,
        #     n_clusters=n_clusters,
        #     fead_dim=features.shape[1],
        #     n_nodes=features.shape[0],
        #     hidden_dim1=args.hidden1,
        #     hidden_dim2=args.hidden2,
        #     dropout=args.dropout,
        #     lr=args.lr,
        #     early_stop=args.early_stopping_epoch,
        #     activation=args.activation,
        # )
        # model.fit(adj_csr, features)
        model = VGAEKmeans(
            in_features=features_lil.shape[1],
            hidden_units_1=args.hidden1,
            hidden_units_2=args.hidden2,
            lr=args.lr,
            early_stopping_epoch=args.early_stopping_epoch,
            n_epochs=args.epochs,
            model_filename=args.model_filename,
        )
        model.fit(features_lil, adj_csr, n_clusters)
        res = model.get_memberships()
    elif args.model == "VGAECD":
        model = VGAECD(
            in_features=features_lil.shape[1],
            n_clusters=n_clusters,
            alpha=args.alpha,
            beta=args.beta,
            hidden_units_1=args.hidden1,
            hidden_units_2=args.hidden2,
            lr=args.lr,
            early_stopping_epoch=args.early_stopping_epoch,
            n_epochs=args.n_epochs,
            n_epochs_pretrain=args.n_epochs_pretrain,
            activation=args.activation,
        )
        model.fit(features_lil, adj_csr)
        res = model.get_memberships()
    elif args.model == "SDCN":
        model = SDCN(
            graph,
            features,
            label,
            features.shape[1],
            n_clusters,
            args.hidden1,
            args.hidden2,
            args.hidden3,
            args.lr,
            args.epochs,
            args.pretrain_ae_lr,
            args.pretrain_ae_epochs,
            args.hidden4,
            args.v,
            args.gpu,
        )
        model.fit()
        res = model.get_memberships()
    elif args.model == "DANMF":
        model = DANMF(graph, args)
        model.pre_training()
        res = model.training()
    elif args.model == "MNMF":
        model = MNMF(
            dimensions=args.dimensions,
            clusters=n_clusters,
            alpha=args.alpha,
            beta=args.beta,
            lambd=args.lambd,
            eta=args.eta,
            iterations=args.iterations,
            lower_control=args.lower_control,
        )
        model.fit(graph)
        res = model.get_memberships()
    elif args.model == "sgc_kmeans":
        graph = graph.remove_self_loop().add_self_loop()
        model = SGCKmeans(
            in_feats=features.shape[1],
            n_epochs=args.n_epochs,
            hidden_units=args.out_feats_list,
            lr=args.lr,
            early_stop=args.early_stopping_epoch,
            inner_act=lambda x: x,
            n_lin_layers=args.n_lin_layers,
            n_gnn_layers=args.n_gnn_layers,
        )
        model.fit(
            graph=graph,
            n_clusters=n_clusters,
            device=device,
        )
        res = model.get_memberships()
    elif args.model == "dgi_kmeans":
        graph = graph.remove_self_loop().add_self_loop()
        model = DGIKmeans(
            in_feats=features.shape[1],
            out_feats_list=args.out_feats_list,
            n_epochs=args.n_epochs,
            early_stopping_epoch=args.early_stopping_epoch,
            neighbor_sampler_fanouts=args.neighbor_sampler_fanouts,
            lr=args.lr,
            l2_coef=args.l2_coef,
            # batch_size=args.batch_size,
            batch_size=n_nodes,
            activation=args.activation,
            model_filename=args.model_filename,
        )
        model.fit(
            graph=graph,
            n_clusters=n_clusters,
            device=device,
        )
        res = model.get_memberships(
            graph=graph,
            device=device,
        )
    elif args.model == "gmi_kmeans":
        if args.gcn_depth is None and args.dataset in (
                "Citeseer",
                "Pubmed",
                "CoraFull",
        ):
            gcn_depth = 1
        else:
            gcn_depth = args.gcn_depth if args.gcn_depth is not None else 2
        model = GMIKmeans(
            in_features=features.shape[1],
            hidden_units=args.hidden_units,
            n_epochs=args.n_epochs,
            early_stopping_epoch=args.early_stopping_epoch,
            lr=args.lr,
            l2_coef=args.l2_coef,
            alpha=args.alpha,
            beta=args.beta,
            gamma=args.gamma,
            activation=args.activation,
            gcn_depth=gcn_depth,
        )
        model.fit(
            features_lil,
            adj_csr,
            n_clusters,
            neg_list_num=5,
        )
        res = model.get_memberships()
    elif args.model == "SENet_kmeans":
        # pass
        # NOTE: delete this comment when fixed
        # pylint: disable=fixme
        # FIXME shoule pass adj as csr matrix as large graphs' adjs can't be converted to dense
        model = SENetKmeans(
            feature=features,
            labels=label,
            adj=adj,
            n_clusters=n_clusters,
            hidden0=args.hidden0,
            hidden1=args.hidden1,
            lr=args.lr,
            epochs=args.epochs,
            weight_decay=args.weight_decay,
            lam=args.lam,
            n_iter=args.n_iter,
        )
        model.fit()
        res = model.get_memberships()
    elif args.model == "DFCN":
        model = DFCN(
            graph,
            features,
            label,
            n_clusters=n_clusters,
            n_node=features.size()[0],
            device=device,
            args=args,
        ).to(device)
        model.fit(args.epochs)
        res = model.get_memberships()
    elif args.model == "CommunityGAN":
        if args.pretrain == "agm":
            embed = agm_pretrain(
                edges,
                n_clusters,
                overlapping=True,
            )
        elif args.pretrain == "VGAEKmeans":
            embed = kmeans_pretrain(
                features_lil,
                adj_csr,
                n_clusters,
                label,
            )
        else:
            raise ValueError(
                f"'pretrain' only supports agm or VGAEKmeans but got {args.pretrain}!"
            )

        id2motifs, neighbor_set, total_motifs = get_undireced_motifs(
            n_nodes=n_nodes,
            motif_size=args.motif_size,
            edges=edges,
        )

        model = CommunityGAN(
            n_nodes=features.shape[0],
            node_emd_init_gen=embed,
            node_emd_init_dis=embed,
            max_value=args.max_value,
            n_epochs=args.n_epochs,
            n_epochs_gen=args.n_epochs_gen,
            n_epochs_dis=args.n_epochs_dis,
            gen_interval=args.gen_interval,
            dis_interval=args.dis_interval,
            update_ratio=args.update_ratio,
            n_sample_gen=args.n_sample_gen,
            n_sample_dis=args.n_sample_dis,
            lr_gen=args.lr_gen,
            lr_dis=args.lr_dis,
            l2_coef=args.l2_coef,
            batch_size_gen=args.batch_size_gen,
            batch_size_dis=args.batch_size_dis,
        )
        model.fit(
            total_motifs=total_motifs,
            id2motifs=id2motifs,
            neighbor_set=neighbor_set,
            motif_size=args.motif_size,
        )
        res, _ = model.get_disjoint_memberships()
    elif args.model == "ComE":
        model = ComE(
            graph=graph,
            n_clusters=n_clusters,
            size=graph.ndata["feat"].shape[1],
            down_sampling=args.down_sampling,
            table_size=100000000,
            labels=label.numpy(),
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            negative=args.negative,
            lr=args.lr,
            window_size=args.window_size,
            num_walks=args.num_walks,
            walk_length=args.walk_length,
            num_iter=args.num_iter,
            output_file=args.dataset,
            alpha=args.alpha,
            beta=args.beta,
            reg_covar=args.reg_covar,
        )
        model.fit()
        res = model.get_memberships()
    elif args.model == "AGE":
        model = age_cluster(
            dims=args.dims,
            feat_dim=features.shape[1],
            gnnlayers_num=args.gnnlayers,
            linlayers_num=args.linlayers,
            lr=args.lr,
            upth_st=args.upth_st,
            upth_ed=args.upth_ed,
            lowth_st=args.lowth_st,
            lowth_ed=args.lowth_ed,
            upd=args.upd,
            bs=args.bs,
            epochs=args.epochs,
            norm=args.norm,
            renorm=args.renorm,
            estop_steps=args.estop_steps,
            n_clusters=n_clusters,
        )
        model.fit(adj_csr, features)
        res = model.get_memberships()
    elif args.model == "AGCN":
        model = AGCN(
            graph,
            features,
            label,
            features.shape[1],
            n_clusters,
            args.hidden1,
            args.hidden2,
            args.hidden3,
            args.lr,
            args.epochs,
            args.pretrain_ae_lr,
            args.pretrain_ae_epochs,
            args.hidden4,
            args.v,
            args.gpu,
        )
        model.fit()
        res = model.get_memberships()
    elif args.model == "DAEGC":
        # NOTE: delete this comment when fixed
        # pylint: disable=fixme
        # FIXME shoule pass adj as csr matrix as large graphs' adjs can't be converted to dense
        model = DAEGC(
            num_features=features.shape[1],
            hidden_size=args.hidden_size,
            embedding_size=args.embedding_size,
            alpha=args.alpha,
            num_clusters=n_clusters,
            pretrain_lr=args.pretrain_lr,
            lr=args.lr,
            weight_decay=args.weight_decay,
            pre_epochs=args.pre_epochs,
            epochs=args.epochs,
            update_interval=args.update_interval,
            estop_steps=args.estop_steps,
            t=args.t,
            v=args.v,
        )
        # adj=graph.adj()
        # model.fit(adj.to_dense(), features, label)
        model.fit(adj_csr, features, label)
        res = model.get_memberships()

    elif args.model == "GALA":
        # pass
        # NOTE: delete this comment when fixed
        # pylint: disable=fixme
        # FIXME shoule pass adj as csr matrix as large graphs' adjs can't be converted to dense
        model = GALA(
            adj,
            X=graph.ndata["feat"],
            lr=args.lr,
            epochs=args.epochs,
            hidden1=args.hidden1,
            hidden2=args.hidden2,
            n_clusters=n_clusters,
        )
        model.fit()
        res = model.get_memberships()
    elif args.model == "AGC":
        # pass
        # NOTE: delete this comment when fixed
        # pylint: disable=fixme
        # FIXME shoule pass adj as csr matrix as large graphs' adjs can't be converted to dense
        model = AGC(
            adj=adj,
            feature=features,
            labels=label,
            epochs=args.epochs,
            rep=args.rep,
            n_clusters=n_clusters,
        )
        model.fit()
        res = model.get_memberships()
    elif args.model == "idec":
        graph = graph.remove_self_loop().add_self_loop()
        model = IDEC(
            in_feats=features.shape[1],
            out_feats_list=args.out_feats_list,
            n_clusters=n_clusters,
            aggregator_type=args.aggregator_type,
            bias=args.bias,
            batch_size=args.batch_size,
            alpha=args.alpha,
            beta=args.beta,
            n_epochs=args.n_epochs,
            n_pretrain_epochs=args.n_pretrain_epochs,
            lr=args.lr,
            l2_coef=args.l2_coef,
            early_stopping_epoch=args.early_stopping_epoch,
            model_filename=args.model_filename,
        )
        model.fit(graph, device)
        res = model.get_memberships(graph, device)
    elif args.model == "SEComm":
        graph = graph.remove_self_loop().add_self_loop()
        model = SEComm(
            n_clusters=n_clusters,
            n_nodes=features.shape[0],
            num_features=features.shape[1],
            activation=args.activation,
            base_model=args.base_model,
            batch_size=args.batch_size,
            num_hidden=args.num_hidden,
            num_layers=args.num_layers,
            num_proj_hidden=args.num_proj_hidden,
            tau=args.tau,
            num_cl_hidden=args.num_cl_hidden,
            dropout=args.dropout,
            pretrain_epochs=args.pretrain_epochs,
            learning_rate=args.learning_rate,
            weight_decay=args.weight_decay,
            drop_edge_rate_1=args.drop_edge_rate_1,
            drop_edge_rate_2=args.drop_edge_rate_2,
            drop_feature_rate_1=args.drop_feature_rate_1,
            drop_feature_rate_2=args.drop_feature_rate_2,
            x_norm=args.x_norm,
            iterations=args.iterations,
            threshold=args.threshold,
            se_epochs=args.se_epochs,
            se_alpha=args.se_alpha,
            se_patience=args.se_patience,
            se_lr=args.se_lr,
            cluster_epochs=args.cluster_epochs,
            cluster_alpha=args.cluster_alpha,
            final_beta=args.final_beta,
            cluster_patience=args.cluster_patience,
        )
        model.fit(graph, features, label)
        res = model.get_memberships()
    elif args.model == "cc":
        graph = graph.remove_self_loop().add_self_loop()
        model = ContrastiveClustering(
            in_feats=features.shape[1],
            out_feats_list=args.out_feats_list,
            n_clusters=n_clusters,
            aggregator_type=args.aggregator_type,
            bias=args.bias,
            batch_size=args.batch_size,
            instance_temperature=args.instance_temperature,
            cluster_temperature=args.cluster_temperature,
            aug_types=args.aug_types,
            n_epochs=args.n_epochs,
            lr=args.lr,
            l2_coef=args.l2_coef,
            early_stopping_epoch=args.early_stopping_epoch,
            model_filename=args.model_filename,
        )
        model.fit(graph=graph, device=device)
        res = model.get_memberships(graph, device)
    elif args.model == "clusternet":
        graph = graph.remove_self_loop().add_self_loop()
        model = ClusterNet(
            in_feats=features.shape[1],
            out_feats_list=args.out_feats_list,
            n_clusters=n_clusters,
            cluster_temp=args.cluster_temp,
            dropout=args.dropout,
            n_epochs=args.n_epochs,
            lr=args.lr,
            l2_coef=args.l2_coef,
            early_stopping_epoch=args.early_stopping_epoch,
            model_filename=args.model_filename,
        )
        model.fit(graph=graph, device=device)
        res = model.get_memberships(graph, device)
    elif args.model == "GDCL":  # BUG
        model = GDCL(
            in_feats=features.shape[1],
            n_clusters=n_clusters,
            n_h=args.n_h,
            nb_epochs=args.nb_epochs,
            lr=args.lr,
            alpha=args.alpha,
            mask_num=args.mask_num,
            batch_size=args.batch_size,
            update_interval=args.update_interval,
            model_filename=args.model_filename,
            beta=args.beta,
            weight_decay=args.weight_decay,
            pt_n_h=args.pt_n_h,
            pt_model_filename=args.pt_model_filename,
            pt_nb_epochs=args.pt_nb_epochs,
            pt_patience=args.pt_patience,
            pt_lr=args.pt_lr,
            pt_weight_decay=args.pt_weight_decay,
            pt_sample_size=args.pt_sample_size,
            pt_batch_size=args.pt_batch_size,
            sparse=args.sparse,
            dataset=args.dataset,
            device=device,
        )
        model.fit(graph=graph, labels=label)
        res = model.get_memberships()
    elif args.model == "MVGRL":
        model = MVGRL(
            in_feats=features.shape[1],
            n_clusters=n_clusters,
            n_h=args.n_h,
            model_filename=args.model_filename,
            sparse=args.sparse,
            nb_epochs=args.nb_epochs,
            patience=args.patience,
            lr=args.lr,
            weight_decay=args.weight_decay,
            sample_size=args.sample_size,
            batch_size=args.batch_size,
            dataset=args.dataset,
        )
        model.fit(adj_csr, features)
        res = model.get_memberships()
    elif args.model == "SUBLIME":
        model = SUBLIME(
            nfeats=features.shape[1],
            n_clusters=n_clusters,
            sparse=args.sparse,
            type_learner=args.type_learner,
            k=args.k,
            sim_function=args.sim_function,
            activation_learner=args.activation_learner,
            nlayers=args.nlayers,
            hidden_dim=args.hidden_dim,
            rep_dim=args.rep_dim,
            proj_dim=args.proj_dim,
            dropout=args.dropout,
            dropedge_rate=args.dropedge_rate,
            lr=args.lr,
            w_decay=args.w_decay,
            epochs=args.epochs,
            maskfeat_rate_anchor=args.maskfeat_rate_anchor,
            maskfeat_rate_learner=args.maskfeat_rate_learner,
            contrast_batch_size=args.contrast_batch_size,
            tau=args.tau,
            c=args.c,
            eval_freq=args.eval_freq,
            n_clu_trials=args.n_clu_trials,
        )
        model.fit(adj_csr, features)
        res = model.get_memberships()

    else:
        raise ValueError(f"{args.model} is not implemented!")

    elapsed_time = time.time() - start_time

    # from utils import get_intra_class_mean_distance
    # import matplotlib.pyplot as plt
    # import torch

    # intra_class_mean_distance = get_intra_class_mean_distance(
    #     torch.squeeze(model.get_embedding(), 0), label.numpy()).cpu()
    # print(intra_class_mean_distance)
    # plt.plot(range(len(intra_class_mean_distance)),
    #          intra_class_mean_distance.numpy().flatten())
    # if len(intra_class_mean_distance) < 20:
    #     plt.xticks(range(len(intra_class_mean_distance)))

    # plt.xlabel('community')
    # plt.ylabel('mean distance between nodes and community embedding')
    # plt.title(f'{args.model}/{args.dataset} - mean distance of each community')

    # plt.savefig(f'./results/{args.dataset}_{args.model}.png')

    # plt.clf()

    if len(res) != 0:
        (
            ARI_score,
            NMI_score,
            ACC_score,
            Micro_F1_score,
            Macro_F1_score,
        ) = evaluation(label, res)
        print("\n"
              f"Elapsed Time:{elapsed_time:.2f}s\n"
              f"ARI:{ARI_score}\n"
              f"NMI:{ NMI_score}\n"
              f"ACC:{ACC_score}\n"
              f"Micro F1:{Micro_F1_score}\n"
              f"Macro F1:{Macro_F1_score}\n")

        if args.target_path is not None:
            csv2file(
                args.target_path,
                param_keys + [
                    "ARI",
                    "NMI",
                    "ACC",
                    "Micro F1",
                    "Macro F1",
                    "Elapsed Time",
                ],
                param_values + [
                    ARI_score,
                    NMI_score,
                    ACC_score,
                    Micro_F1_score,
                    Macro_F1_score,
                    elapsed_time,
                ],
            )

        # def get_str_time():
        #     output_file = 'time_' + time.strftime("%m%d%H%M%S",
        #                                           time.localtime())
        #     return output_file

        # from utils.evaluation import best_mapping
        # import pandas as pd
        # labels_true, labels_pred = best_mapping(label.cpu().numpy(), res)
        # df_res = pd.DataFrame({'label': labels_true, 'pred': labels_pred})
        # time_name = get_str_time()
        # df_res.to_pickle(
        #     f'./preds/{args.model}/{args.model}_{args.dataset}_pred_{time_name}.pkl')
        # print('write to',
        #       f'./preds/{args.model}/{args.model}_{args.dataset}_pred_{time_name}.pkl')

    else:
        raise ValueError("No pred result got, please check your args.")
