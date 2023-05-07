import torch
import numpy as np
import  scipy.stats
from    torch.optim import lr_scheduler
import  random, sys, pickle
import  argparse
from meta import *
from getConfig import modelArch
from data import DataProcessor, task_generator, test_task_generator, test_task_generator_backup
from sklearn.metrics import auc, roc_curve
from utils import  aucPerformance
from analyzer import plot_data



def main():
    # Hyperparameters are defined below
    lr_list = [0.003, 0.007, 0.02, 0.004, 0.03, 0.08] # Different Learning Rates are being used to tune and compare model performances
                                                      # under different configurations

    lr_update = 0.5 # Inner update LR
    step_update, test_step_update = 3, 3 # Inner update steps
    batch_size = 16 # Batch size
    max_epoch = 100 # Number of maximum epochs

    total_run = 100 # In each run the model is trained with a random sample and its performance under the sample is recorded.
                    # So, 100 runs means that 100 different trained FSL models.
    num_graph = 5   # Number of total graphs that will be used in Meta training

    results_dict = dict() # To store the final results for comparison

    itr = 0
    for lr in lr_list:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        random.seed(args.seed)
        torch.manual_seed(args.seed)
        np.random.seed(args.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(args.seed)

        num_labeled_ano = 10 # Each graph (auxiliary or target) has 10 sampled anomaly nodes

        results_meta_gdn = []

        for t in range(total_run):
            dataset = DataProcessor(num_graph = num_graph, degree = 2, data_name = args.data_name)
            dataset.data_loader()

            # training meta-gdn
            print("Meta-GDN training...")
            print("In %d-th run..." % (t + 1))
            [feature_list, l_list, ul_list], [target_feature, target_l_idx, target_ul_idx] = dataset.sample_anomaly(num_labeled_ano)

            config = modelArch(feature_list[0].shape[1], 1)

            maml = Meta(lr, lr_update, step_update, test_step_update, num_graph, config).to(device)
            best_val_auc = 0
            for e in range(1, max_epoch + 1):

                # training
                maml.train()
                x_train, y_train, x_qry, y_qry = task_generator(feature_list, l_list, ul_list, bs = batch_size, device = device)
                loss = maml(x_train, y_train, x_qry, y_qry)
                torch.save(maml.state_dict(), 'temp.pkl')
                # validation
                model_meta_eval = Meta(lr, lr_update, step_update, test_step_update, num_graph, config).to(device)
                model_meta_eval.load_state_dict(torch.load('temp.pkl'))
                model_meta_eval.eval()
                x_train, y_train, x_val, y_val = test_task_generator(target_feature, target_l_idx,
                                                                       target_ul_idx, batch_size,
                                                                       dataset.target_label,
                                                                       dataset.target_idx_val, device)
                auc_roc, auc_pr, ap = model_meta_eval.evaluate(x_train, y_train, x_val, y_val)
                print("%dth Epoch: Training Loss %4f, Validation, AUC-ROC %.4f, AUC-PR %.4f, AP %.4f" % (e, loss.item(), auc_roc, auc_pr, ap))

                if auc_roc > best_val_auc: # Store the best model
                    best_val_auc = auc_roc
                    torch.save(maml.state_dict(), 'best_meta_GDN.pkl')

            print("End of training.")
            # testing
            print("Load the best performing Meta-GDN model and Evaluate")
            maml = Meta(lr, lr_update, step_update, test_step_update, num_graph, config).to(device)
            maml.load_state_dict(torch.load('best_meta_GDN.pkl'))
            maml.eval()
            x_train, y_train, x_test, y_test = test_task_generator(target_feature, target_l_idx,
                                                                   target_ul_idx, batch_size,
                                                                   dataset.target_label,
                                                                   dataset.target_idx_test, device)
            auc_roc, auc_pr, ap = maml.evaluate(x_train, y_train, x_test, y_test)
            print("Testing performance of Meta-GDN: AUC-ROC %.4f, AUC-PR %.4f, AP %.4f" % (auc_roc, auc_pr, ap))
            print("End of evaluating.")
            results_meta_gdn.append(auc_roc)

        results_dict[itr] = {"perf": results_meta_gdn, "lr": lr, "avg": sum(results_meta_gdn) * 1.0 / len(results_meta_gdn)}
        plot_data(results_dict, total_run)
        itr += 1

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--data_name', help='pubmed/yelp', default='pubmed')
    argparser.add_argument('--seed', type=int, default=1234, help='Random seed.')

    args = argparser.parse_args()

    main()