import matplotlib.pyplot as plt
from numpy import mean, arange
from evaluation import compute_PrecisionRecallF1

def compute_PRF_at_K(K, query_list, ground_truth_list, recom_list):
    
    PRF_list = []
    for i in range(len(query_list)):
        PRF = compute_PrecisionRecallF1(ground_truth_list[i], recom_list[i][:K])
        PRF_list.append(PRF)
    
    return PRF_list

def compute_AVG_PRF_at_K(K, query_list, ground_truth_list, recom_list):
    PRF_list = compute_PRF_at_K(K, query_list, ground_truth_list, recom_list)
    
    avg_precision = mean([el[0] for el in PRF_list])
    avg_recall = mean([el[1] for el in PRF_list])
    avg_f1score = mean([el[2] for el in PRF_list])
      
    return (avg_precision, avg_recall, avg_f1score)

    
def experiment_2a(K, query_list, ground_truth_list, method_recom_list):
    
    jac_prf = compute_AVG_PRF_at_K(K, query_list, ground_truth_list, method_recom_list["jac"])
    w2va_prf = compute_AVG_PRF_at_K(K, query_list, ground_truth_list, method_recom_list["avg"])
    w2vs_prf = compute_AVG_PRF_at_K(K, query_list, ground_truth_list, method_recom_list["sta"])
    tfidf_prf = compute_AVG_PRF_at_K(K, query_list, ground_truth_list, method_recom_list["tf-idf"])
    lsi_prf = compute_AVG_PRF_at_K(K, query_list, ground_truth_list, method_recom_list["lsi"])    
    
    print('JAC  ', jac_prf)
    print('W2VA ', w2va_prf) 
    print('W2VS ', w2vs_prf) 
    print('TFIDF', tfidf_prf)
    print('LSI  ', lsi_prf)
    
def experiment_2b(query_list, ground_truth_list, method_recom_list):
    
    jac_prf = []
    w2va_prf = []
    w2vs_prf = []
    tfidf_prf = []
    lsi_prf = []    

    for k in range(1, 21):
        jac_prf.append(compute_AVG_PRF_at_K(k, query_list, ground_truth_list, method_recom_list["jac"]))
        w2va_prf.append(compute_AVG_PRF_at_K(k, query_list, ground_truth_list, method_recom_list["avg"]))
        w2vs_prf.append(compute_AVG_PRF_at_K(k, query_list, ground_truth_list, method_recom_list["sta"]))
        tfidf_prf.append(compute_AVG_PRF_at_K(k, query_list, ground_truth_list, method_recom_list["tf-idf"]))
        lsi_prf.append(compute_AVG_PRF_at_K(k, query_list, ground_truth_list, method_recom_list["lsi"]))    

    
    
    PRF_diagram('P', jac_prf, w2va_prf, w2vs_prf, tfidf_prf, lsi_prf)
    PRF_diagram('R', jac_prf, w2va_prf, w2vs_prf, tfidf_prf, lsi_prf)
    PRF_diagram('F', jac_prf, w2va_prf, w2vs_prf, tfidf_prf, lsi_prf)

def PRF_diagram(metric, jac_prf, w2va_prf, w2vs_prf, tfidf_prf, lsi_prf):
    if metric == 'P':
        m = 0
    elif metric == 'R':
        m = 1
    elif metric == 'F':
        m = 2
        
    jac_m = [el[m] for el in jac_prf]
    w2va_m = [el[m] for el in w2va_prf]
    w2vs_m = [el[m] for el in w2vs_prf]
    tfidf_m = [el[m] for el in tfidf_prf]
    lsi_m = [el[m] for el in lsi_prf]
    
    plt.figure()
    plt.title(metric)
    diagram(range(1, 21), jac_m, arange(1, 20, step=1), label="JAC")
    diagram(range(1, 21), w2va_m, arange(1, 20, step=1), label="W2VA")
    diagram(range(1, 21), w2vs_m, arange(1, 20, step=1), label="W2VS")
    diagram(range(1, 21), tfidf_m, arange(1, 20, step=1), label="TFIDF")
    diagram(range(1, 21), lsi_m, arange(1, 20, step=1), label="LSI")
    plt.show()
    
    
def diagram(x, y, xticks, label):
    plt.plot(x, y, label=label)
    plt.legend(loc='best', numpoints=1, fancybox=True)
    plt.xticks(xticks)
