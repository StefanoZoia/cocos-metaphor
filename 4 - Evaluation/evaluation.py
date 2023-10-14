import csv
import eval_config as cfg
import statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# reads a google form csv answers and computes relevant statistics
def main():
    with open(cfg.ANSWER_FILE, encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        questions = next(reader)    # read the questions separately
        overall_eval = list()       # list of overall points assigned to the semantic extraction

        # the row of the csv have shape (timestamp, [answer for question N]*)
        for row in reader:
            for i in range(cfg.FIRST_EVAL_INDEX, cfg.LAST_EVAL_INDEX):
                if row[i] != '':
                    overall_eval.append(int(row[i]))

    print('Evaluation results:\n')
    mean = statistics.mean(overall_eval)
    print(f'Overall mean: {mean:.2f}')
    print(f'Overall median: {statistics.median(overall_eval)}')
    print(f'Overall mode: {statistics.mode(overall_eval)}')
    print(f'Overall skewness: {stats.skew(overall_eval):.2f}')
    print(f'Overall st. dev.: {statistics.stdev(overall_eval):.2f}')
    print(f'Overall min: {min(overall_eval)}')
    print(f'Overall max: {max(overall_eval)}')

    n, bins, patches = plt.hist(overall_eval, bins=np.arange(-0.5, 10.5, 1))
    for p in patches:
        p.set_edgecolor('black')
    plt.xlabel('evaluation score')
    plt.xticks(range(0, 10))
    plt.ylabel('n. of answers')
    line = plt.axvline(mean, color='red')
    plt.legend([line], [f'mean = {mean:.2f}'])
    plt.title('Overall evaluation')
    plt.show()




if __name__ == '__main__' : main()