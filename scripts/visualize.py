import seaborn
import pandas as pd


def visualize_algo_detectability(data):
    pos_data = data[data["iter"] >= 0]
    value_counts = pos_data['algo'].value_counts().reset_index()
    value_counts.columns = ['algo', 'count']
    seaborn.barplot(x="algo", y="count", data=value_counts)

def visualize_algo_performance(data):
    pos_data = data[data["iter"] >= 0]
    hist_data = []
    for i in range(0, 1000):
        df = pos_data[pos_data["iter"] <= i].groupby("algo").count().reset_index()
        df['iter'] = i
        hist_data.append(df)

    hist_data = pd.concat(hist_data)
    seaborn.scatterplot(x="iter", y="name", hue="algo", data=hist_data)
