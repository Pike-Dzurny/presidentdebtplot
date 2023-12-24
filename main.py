import datetime
import math
import pandas as pd
import matplotlib.pyplot as plt

print(plt.style.available)

#plt.style.use('seaborn-v0_8')

def plot_data(csv_file, presidencies, start_date=None, end_date=None, window_size=5):
    # Load data
    data = pd.read_csv(csv_file, parse_dates=['DATE'])

    # Filter data based on date range
    if start_date:
        data = data[data['DATE'] >= pd.to_datetime(start_date)]
    if end_date:
        data = data[data['DATE'] <= pd.to_datetime(end_date)]

    # Calculate log of data
    data['log_GFDEBTN'] = data['GFDEBTN'].apply(lambda x: math.log(x))

    # Calculate derivatives
    data['First_Derivative'] = data['GFDEBTN'].diff()
    data['Second_Derivative'] = data['GFDEBTN'].diff().diff()

    # Smooth derivatives with a rolling window
    data['Smoothed_First_Derivative'] = data['First_Derivative'].rolling(window=window_size, center=True).mean()
    data['Smoothed_Second_Derivative'] = data['Second_Derivative'].rolling(window=window_size, center=True).mean()

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Add colored backgrounds for each presidency
    for start, end, color in presidencies:
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end) if end != 'present' else pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        ax1.axvspan(start_date, end_date, color=color, alpha=0.1)

        # Add gray backgrounds for recessions, adjust vertical height with ymin and ymax
    for start, end in recessions:
        ax1.axvspan(start, end, ymin=0.0, ymax=0.8, color='lightgray', alpha=0.5)

    # Plot log-transformed data and its derivative
    ax1.plot(data['DATE'], data['GFDEBTN'], label='Log of Public Debt', color='navy', linewidth=2)
    ax1.set_xlabel('Date', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Log of Total Public Debt', color='navy', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='navy', labelsize=12)

    # Secondary y-axis for smoothed derivative
    ax2 = ax1.twinx()
    ax2.plot(data['DATE'], data['Smoothed_First_Derivative'], label='Smoothed First Derivative', color='red', linewidth=1)
    ax2.plot(data['DATE'], data['Smoothed_Second_Derivative'], label='Smoothed Second Derivative', color='green', linewidth=1)

    ax2.set_ylabel('Smoothed Derivative of Log', color='darkgreen', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='darkgreen', labelsize=12)

    # Adding legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0.05, 0.95), borderaxespad=0.)
    ax2.legend(loc='upper left', bbox_to_anchor=(0.05, 0.90), borderaxespad=0.)

    # Disable scientific notation for y-axis
    ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax2.get_yaxis().get_major_formatter().set_useOffset(False)

    plt.title('GFDEBTN, its Smoothed Derivatives, and Presidential Terms')
    plt.show()

presidencies = [
    ('1977-01-20', '1981-01-20', 'blue'),  # Jimmy Carter, Democrat
    ('1981-01-20', '1989-01-20', 'red'),   # Ronald Reagan, Republican
    ('1989-01-20', '1993-01-20', 'red'),   # George H. W. Bush, Republican
    ('1993-01-20', '2001-01-20', 'blue'),  # Bill Clinton, Democrat
    ('2001-01-20', '2009-01-20', 'red'),   # George W. Bush, Republican
    ('2009-01-20', '2017-01-20', 'blue'),  # Barack Obama, Democrat
    ('2017-01-20', '2021-01-20', 'red'),   # Donald Trump, Republican
    ('2021-01-20', '2025-01-20', 'blue'),     # Joe Biden, Democrat
]

recessions = [
    # Format: (start_date, end_date)
    # Example entries (update with actual dates)
    ('1990-07-01', '1991-03-31'),  # Recession in 1990
    ('2001-03-01', '2001-11-30'),  # Recession in 2001
    ('2007-12-01', '2009-06-30'),  # Great Recession
    ('2020-02-01', '2020-04-01'),  # Covid-19 Recession
]


# Example usage
plot_data('data/GFDEBTN.csv', presidencies, '1977-01-01', '2023-07-01')
