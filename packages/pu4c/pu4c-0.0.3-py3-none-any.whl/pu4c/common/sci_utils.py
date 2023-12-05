import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

colormap = ['blue', 'green', 'red']

def draw_hist(data_dict: dict, min, max, num_bins, 
              normlize=True, colors=None, save_fname=None,
              xticks=5, title=None, xlabel=None, ylabel=None,
              ):
    plt.clf()
    if colors is None: colors = colormap
    
    x = np.linspace(min, max, num_bins)
    for i, (key, data) in enumerate(data_dict.items()):
        hist, bins = np.histogram(data, bins=num_bins, range=(min, max))
        if normlize: hist = hist / sum(hist) * 100
    
        dataframe = pd.DataFrame({'x':x, key:hist})
        sns.barplot(x='x', y=key, data=dataframe, color=colors[i], alpha=0.5, label=key)

    # 设置 x 轴刻度显示
    show_ticks = xticks  # 设置要显示的刻度数量
    x_ticks = np.linspace(0, x.shape[0] - 1, show_ticks).astype(int)
    x_ticklabels = np.round(x[x_ticks])
    plt.xticks(x_ticks, x_ticklabels)
        
    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    
    plt.legend()
    if save_fname:
        plt.savefig(save_fname)
    else:
        plt.show()