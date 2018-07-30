import matplotlib.pyplot as plt
from numpy import mean, arange
from evaluation import compute_PrecisionRecallF1, computeMeanReciprocalRank


def compute_PRF_at_K(K, query_list, ground_truth_list, recom_list):

    PRF_list = []
    for i in range(len(query_list)):
        PRF = compute_PrecisionRecallF1(
            ground_truth_list[i], recom_list[i][:K])
        PRF_list.append(PRF)

    return PRF_list


def compute_AVG_PRF_at_K(K, query_list, ground_truth_list, recom_list):
    PRF_list = compute_PRF_at_K(K, query_list, ground_truth_list, recom_list)

    avg_precision = mean([el[0] for el in PRF_list])
    avg_recall = mean([el[1] for el in PRF_list])
    avg_f1score = mean([el[2] for el in PRF_list])

    return (avg_precision, avg_recall, avg_f1score)


def experiment_models_a(K, query_list, ground_truth_list, model_recom_list):

    for key, val in model_recom_list.items():
        prf = compute_AVG_PRF_at_K(
            K, query_list, ground_truth_list, model_recom_list[key])
        print(key, prf)


def experiment_models_b(query_list, ground_truth_list, model_recom_list):
    method_prf = {}
    prf = []
    for key, val in model_recom_list.items():
        for k in range(1, 21):
            prf.append(compute_AVG_PRF_at_K(k, query_list,
                                            ground_truth_list, model_recom_list[key]))

        method_prf[key] = prf

    PRF_diagram('P', method_prf)
    PRF_diagram('R', method_prf)
    PRF_diagram('F', method_prf)


def PRF_diagram(metric, method_prf):
    save = False
    if metric == 'P':
        m = 0
        ylabel = "Precision@k"
    elif metric == 'R':
        m = 1
        ylabel = "Recall@k"
        save = True
    elif metric == 'F':
        m = 2
        ylabel = "F1@k"

    plt.figure()
    plt.title("Relevant Recommendations")
    plt.ylabel(ylabel)
    plt.xlabel("Number of Recommendations k")

    for method, prf in method_prf.items():
        metric_values = [el[m] for el in prf]
        diagram(range(1, 21), metric_values,
                arange(1, 20, step=1), label=method)

    plt.show()


def experiment_1_2_a(K, query_list, ground_truth_list, method_recom_list):

    jac_prf = compute_AVG_PRF_at_K(
        K, query_list, ground_truth_list, method_recom_list["jac"])
    w2va_prf = compute_AVG_PRF_at_K(
        K, query_list, ground_truth_list, method_recom_list["avg"])
    w2vs_prf = compute_AVG_PRF_at_K(
        K, query_list, ground_truth_list, method_recom_list["sta"])
    tfidf_prf = compute_AVG_PRF_at_K(
        K, query_list, ground_truth_list, method_recom_list["tf-idf"])
    lsi_prf = compute_AVG_PRF_at_K(
        K, query_list, ground_truth_list, method_recom_list["lsi"])

    print('JAC  ', jac_prf)
    print('W2VA ', w2va_prf)
    print('W2VS ', w2vs_prf)
    print('TFIDF', tfidf_prf)
    print('LSI  ', lsi_prf)


def experiment_1_2_b(query_list, ground_truth_list, method_recom_list):

    jac_prf = []
    w2va_prf = []
    w2vs_prf = []
    tfidf_prf = []
    lsi_prf = []

    for k in range(1, 21):
        jac_prf.append(compute_AVG_PRF_at_K(
            k, query_list, ground_truth_list, method_recom_list["jac"]))
        w2va_prf.append(compute_AVG_PRF_at_K(
            k, query_list, ground_truth_list, method_recom_list["avg"]))
        w2vs_prf.append(compute_AVG_PRF_at_K(
            k, query_list, ground_truth_list, method_recom_list["sta"]))
        tfidf_prf.append(compute_AVG_PRF_at_K(
            k, query_list, ground_truth_list, method_recom_list["tf-idf"]))
        lsi_prf.append(compute_AVG_PRF_at_K(
            k, query_list, ground_truth_list, method_recom_list["lsi"]))

    method_prf = {'JAC': jac_prf, 'W2VA': w2va_prf,
                  'W2VC': w2vs_prf, 'TFIDF': tfidf_prf, 'LSI': lsi_prf}

    PRF_diagram('P', method_prf)
    PRF_diagram('R', method_prf)
    PRF_diagram('F', method_prf)


def diagram(x, y, xticks, label):
    plt.plot(x, y, label=label)
    plt.legend(loc='best', numpoints=1, fancybox=True)
    plt.xticks(xticks)


def experiment_user_feedback(number_of_tests, tests_steps, test_blocks_GT, iterations_test_blocks_R):

    N = number_of_tests

    iteration_MRR_list = []

    for itera in range(len(iterations_test_blocks_R)):
        iteration_MRR = []
        for i in range(N):
            single_test_MRR = computeMeanReciprocalRank(
                test_blocks_GT[i], iterations_test_blocks_R[itera][i])
            iteration_MRR.append(single_test_MRR)
        iteration_MRR_list.append(iteration_MRR)

    plt.figure()
    plt.title("User feedback evaluation")
    plt.xlabel("Tests")
    plt.ylabel("MRR")

    for itera in range(len(iterations_test_blocks_R)):
        print("MRR_list", iteration_MRR_list[itera])
        print("Mean MRR: ", mean(iteration_MRR_list[itera]))
        diagram(range(1, N + 1), iteration_MRR_list[itera],
                arange(1, N + 1, step=1), label="run" + str(itera))


def experiment_time_performance(number_of_tests, recommend_requirements_time, recommend_test_blocks_time):
    N = number_of_tests
    recommend_test_blocks_time_avg = []
    for i in range(N):
        avg_time = mean(recommend_test_blocks_time[i])
        recommend_test_blocks_time_avg.append(avg_time)

    plt.figure()
    plt.title("Speed of Response")
    plt.xlabel("Test Scenarios")
    plt.ylabel("Time (sec)")
    diagram(range(1, N + 1), recommend_requirements_time,
            arange(1, N + 1, step=1), label="Requirements")
    diagram(range(1, N + 1), recommend_test_blocks_time_avg,
            arange(1, N + 1, step=1), label="Test Blocks")

    plt.savefig("../thesis/Figures/plot-time-performance_.png")


def experiment_test_coverage(test_list, automated_test_steps_GT, traced_requirements_GT,
                             automated_test_steps_S, traced_requirements_S):
    N = len(test_list)
    automated_test_steps_coverage = []
    traced_requirements_coverage = []
    for i in range(N):
        automated_test_steps_coverage.append(
            automated_test_steps_S[i] / automated_test_steps_GT[i])
        traced_requirements_coverage.append(
            traced_requirements_S[i] / traced_requirements_GT[i])

    plt.figure()
    plt.title("Test Coverage")
    plt.xlabel("Test Scenarios")
    plt.ylabel("Coverage percentage")
    diagram(range(1, N + 1), traced_requirements_coverage,
            arange(1, N + 1, step=1), label="Traced Requirements")
    diagram(range(1, N + 1), automated_test_steps_coverage,
            arange(1, N + 1, step=1), label="Automated Test Steps")

    print("Total coverage of traced requirements: ",
          mean(traced_requirements_coverage))
    print("Total coverage of automated test steps: ",
          mean(automated_test_steps_coverage))

    plt.savefig("../thesis/Figures/plot-test-coverage_.png")
