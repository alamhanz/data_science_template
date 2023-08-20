from sklearn.metrics import (
    mean_squared_error,
    make_scorer,
    r2_score,
    classification_report,
    confusion_matrix,
    mean_squared_log_error,
)
from sklearn.metrics import (
    precision_recall_curve,
    roc_auc_score,
    plot_precision_recall_curve,
    average_precision_score,
)
import seaborn as sns
import numpy as np


def binary_eval(y_true, y_pred=None, model=None, predictor=None, thrs=0.5):
    """
    [TODO] To output evaluation of binary model

    Args:
        predictor (pandas):
        model (string) : column name for target value
        predictor (array of string) : name of features to be calculated

    Returns:
        auc_pr, auc_roc

    """

    y_val = y_true.copy()

    if model is not None:
        if predictor is not None:
            y_val_pred = model.predict(predictor)
        else:
            print("Insert Data for Model")
            return
    elif y_pred is not None:
        y_val_pred = y_pred.copy()
    else:
        print("Insert Model or Target Prediction")
        return

    y_val_pred2 = y_val_pred.reshape(-1)
    y_val_label = (y_val_pred2 > thrs).astype(int)

    print(classification_report(y_val, y_val_label))

    cm = confusion_matrix(y_val, y_val_label)
    sns.heatmap((cm.transpose() / cm.sum(axis=1)).transpose(), annot=True)

    auc_pr_val = round(average_precision_score(y_val, y_val_pred2), 4)
    auc_roc_val = round(roc_auc_score(y_val, y_val_pred2), 4)

    print("aucpr : ", auc_pr_val)
    print("aucroc : ", auc_roc_val)

    return auc_pr_val, auc_roc_val


## MAPE = mean_absolute_percentage_error
def mape_score(y_true, y_pred):
    ## if ytrue is zero, the mape is 150
    score = np.mean(np.where(y_true == 0, 1.5, np.abs(y_true - y_pred) / y_true)) * 100
    return score


def regression_eval(ytrue, ypred, thrs=3):
    all_pair = np.array(list(zip(ytrue, ypred)))
    overpred_pair = all_pair[all_pair[:, 0] < all_pair[:, 1]]
    underpred_pair = all_pair[all_pair[:, 0] > all_pair[:, 1]]
    all_err = np.abs(ypred - ytrue)
    summary_eval = {}

    summary_eval["MAE"] = all_err.mean()
    summary_eval["MAPE"] = mape_score(ytrue, ypred)

    summary_eval["MAPE_overpred"] = mape_score(overpred_pair[:, 0], overpred_pair[:, 1])
    summary_eval["MAPE_undrpred"] = mape_score(
        underpred_pair[:, 0], underpred_pair[:, 1]
    )

    summary_eval["over_est_" + str(thrs) + "_pct"] = (ypred - ytrue > thrs).mean() * 100
    summary_eval["under_est_" + str(thrs) + "_pct"] = (
        ytrue - ypred > thrs
    ).mean() * 100

    summary_eval["R2"] = r2_score(ytrue, ypred)
    summary_eval["MSE"] = mean_squared_error(ytrue, ypred)
    summary_eval["RMSE"] = np.sqrt(summary_eval["MSE"])
    # summary_eval['RMSLE']=np.sqrt(mean_squared_log_error(ytrue,ypred))

    for k in summary_eval:
        summary_eval[k] = round(summary_eval[k], 2)

    return summary_eval
