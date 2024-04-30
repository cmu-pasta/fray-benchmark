import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def visualize_algo_detectability(data):
    pos_data = data[data["iter"] >= 0]
    plot_data = []
    # Process each algorithm separately
    for algo in pos_data['algo'].unique():
        # Filter data for the current algorithm
        temp_data = pos_data[pos_data['algo'] == algo]
        # Sort the DataFrame by the 'time' column
        temp_data_sorted = temp_data.sort_values(by='time')
        # Calculate the cumulative count of rows where 'time' is greater than each value in the sorted list
        cumulative_counts = temp_data_sorted['time'].shape[0] - (temp_data_sorted['time'][::-1] <= temp_data_sorted['time'].iloc[-1]).cumsum()[::-1]
        # cumulative_counts = (temp_data_sorted['time'].shape[0] - temp_data_sorted['time'].cumcount())
        # Append to the plot data DataFrame
        temp_df = pd.DataFrame({
            'Time': temp_data_sorted['time'],
            'Cumulative Count': cumulative_counts,
            'Algorithm': algo  # Add the algorithm as a column
        })
        plot_data.append(temp_df)
    plot_data = pd.concat(plot_data)
    # Plotting using Seaborn
    plt.figure(figsize=(12, 8))
    grid =sns.lineplot(data=plot_data, x='Time', y='Cumulative Count', hue='Algorithm', marker='o')
    grid.set_xscale('log')
    plt.xlabel('Time')
    plt.ylabel('Count of Rows with Time > x')
    plt.title('Cumulative Count of Rows by Time for Each Algorithm')
    plt.grid(True)
    plt.show()


def visualize_algo_performance(data):
    pos_data = data[data["iter"] >= 0]
    hist_data = []
    for i in range(0, 1000):
        df = pos_data[pos_data["iter"] <= i].groupby("algo").count().reset_index()
        df['iter'] = i
        hist_data.append(df)

    hist_data = pd.concat(hist_data)
    seaborn.scatterplot(x="iter", y="name", hue="algo", data=hist_data)
