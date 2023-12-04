import numpy as np
import matplotlib.pyplot as plt
import datetime

class MultiOpt:
    def __init__(self, X, scores):
        self.X = np.array(X)
        self.scores = scores
        self.font = {'family' : 'Arial',
                'weight' : 'normal',
                'size'   : 23,
                }
        
        now = datetime.datetime.now()
        self.time = now.strftime('%Y-%m-%d %H:%M:%S')

    def BiSearch(self):
        if len(self.scores) == 2: pass
        else: 
            print('Search_bi is implemented for only two design targets')
            raise ValueError
        Tone = (self.scores[0] - self.scores[0].min()) / (self.scores[0].max()-self.scores[0].min())
        Ttwo = (self.scores[1] - self.scores[1].min()) / (self.scores[1].max()-self.scores[1].min())

        pareto_front = find_pareto_front(Tone,Ttwo)
        sums = pareto_front[:,0] + pareto_front[:,1]
        opt_index = np.argmax(sums)
        val_one = pareto_front[:,0][opt_index]
        val_two = pareto_front[:,1][opt_index]
        indices = np.where((pareto_front[:,0] == val_one) & (pareto_front[:,1] == val_two))[0]
        print(indices)
        xx = np.arange(5,95)/100
        
        fig = plt.figure(figsize=[8,8])
        plt.scatter(Tone, Ttwo, marker='o', edgecolor='gray',label='virtual samples')
        plt.scatter(pareto_front[:,0],pareto_front[:,1], marker='o', c='cyan', edgecolor='k',label='Pareto front')
        plt.scatter(val_one,val_two ,marker='*', c='red', s=150, edgecolor='k',label='candidates')
        plt.plot(xx, val_one+val_two-1*xx,c='y',linestyle='--',alpha=0.6,)
        plt.xlabel('utility values of Object onw ',self.font)
        plt.ylabel('utility values of Object two',self.font)
        plt.xlim(-0.05, 1.05)  
        plt.ylim(-0.05, 1.05) 
        plt.legend(fontsize=13,)
        plt.tick_params(labelsize=20)
        plt.legend(fontsize=13,loc=1)
        plt.savefig('{}.png'.format(self.time), dpi=800)
        plt.savefig('{}.svg'.format(self.time), dpi=800)
        plt.show()

        print('The optimal condidate is :', self.X[indices])
        return self.X[indices]

    def plot_distribution(self):
        if len(self.scores) <= 4:
            plt.figure(figsize=(10, 6))
            for i, task_scores in enumerate(self.scores):
                task_scores = (task_scores - task_scores.min()) / (task_scores.max()-task_scores.min())
                plt.subplot(2, 2, i + 1)
                plt.hist(task_scores, bins=20, alpha=0.7, color='skyblue')
                plt.title(f'Distribution of Score {i + 1}')
                plt.xlabel(f'Score{i + 1}')
                plt.ylabel('Frequency')
            plt.tight_layout()
            plt.savefig('distribution.png', dpi=800)
            plt.savefig('distribution.svg', dpi=800)
            plt.show()
        else:
            print("Number of tasks is greater than 4. Cannot plot distribution.")


def is_pareto_efficient(costs):
    """
    Check if a solution is Pareto efficient.
    """
    num_solutions = costs.shape[0]
    is_efficient = np.ones(num_solutions, dtype=bool)

    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] >= c, axis=1)
            is_efficient[i] = True  # Current solution is always part of the Pareto front

    return is_efficient

def find_pareto_front(x_values, y_values):
    """
    Find points belonging to the Pareto front.
    """
    performance_array = np.column_stack((x_values, y_values))
    pareto_front = performance_array[is_pareto_efficient(performance_array)]
    
    return pareto_front
