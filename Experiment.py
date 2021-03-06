from Evolution import *

num_experiments = 10
nn_layer = [2,3,3,2]

def preprocessing_data(x):
    avg = np.average(x, axis=0)
    m = np.min(x, axis=0)
    M = np.max(x, axis=0)
    return [avg, avg-m, M-avg]

exp_h_fmax=[]
exp_h_favg=[]
exp_h_div=[]

if __name__=='__main__':
    for e in range(num_experiments):
        ea = Evolution(nn_layer)
        ea.evolution(verbose=False)
        exp_h_fmax.append(ea.h_fmax)
        exp_h_favg.append(ea.h_favg)
        exp_h_div.append(ea.h_div)
        print('Experiment {e} done')

    x=np.arange(ea.num_gen)

    exp_h_fmax = preprocessing_data(exp_h_fmax)
    y = exp_h_fmax[0].tolist()
    yl = exp_h_fmax[1].tolist()
    yh = exp_h_fmax[2].tolist()
    plt.figure()
    plt.title('Max Fit')
    plt.errorbar(x, y, yerr=[yl,yh])
    plt.show()

    exp_h_favg = preprocessing_data(exp_h_favg)
    y = exp_h_favg[0].tolist()
    yl = exp_h_favg[1].tolist()
    yh = exp_h_favg[2].tolist()
    plt.figure()
    plt.title('Avg Fit')
    plt.errorbar(x, y, yerr=[yl,yh])
    plt.show()

    exp_h_div = preprocessing_data(exp_h_div)
    y = exp_h_div[0].tolist()
    yl = exp_h_div[1].tolist()
    yh = exp_h_div[2].tolist()
    plt.figure()
    plt.title('Diversity')
    plt.errorbar(x, y, yerr=[yl,yh])
    plt.show()