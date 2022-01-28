import csv
import time
import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

file = '3_days_data_Ryan.csv'
#file = '1_month_of_data_Ryan.csv'
#file = '3_months_of_data_Ryan.csv'

# convert date in YYYY-MM-DDTHH:MM:SS to unix timestamp in local time


def convert_unix(s_date):
    year = int(s_date[0:4:1])
    month = int(s_date[5:7:1])
    day = int(s_date[8:10:1])
    t = s_date[11:19:1]

    dt = datetime.datetime(year, month, day)
    u_date = dt.timestamp()
    u_date += int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])

    return u_date


with open(file, 'r') as data:
    csv_reader = csv.reader(data)

    CGM_BGM = []
    IOB = []
    for line in csv_reader:
        if len(line) > 4:
            if line[2] == "EGV":
                CGM_BGM.append((convert_unix(line[3]), int(line[4])))
        if len(line) > 3:
            if line[0] == "IOB":
                convert_unix(line[2])
                IOB.append((convert_unix(line[2]), float(line[3])))

    # outlier detection of IOB
    df = pd.DataFrame(IOB, columns=['time', 'IOB'])
    outliers_fraction = 0.10
    model = IsolationForest(contamination=outliers_fraction)
    pdf = pd.DataFrame(IOB, columns=['time', 'IOB'])
    model.fit(pdf.values)
    pdf['anomaly2'] = pd.Series(model.predict(pdf.values))
    # visualization of IOB outliers
    df['anomaly2'] = pd.Series(pdf['anomaly2'].values, index=df.index)
    a = df.loc[df['anomaly2'] == -1]  # anomaly
    _ = plt.figure(figsize=(18, 6))
    _ = plt.plot(df['IOB'], color='blue', label='Normal')
    _ = plt.plot(a['IOB'], linestyle='none', marker='X',
                 color='red', markersize=12, label='Anomaly')
    _ = plt.xlabel('Time')
    _ = plt.ylabel('IOB')
    _ = plt.title('IOB Anomalies')
    _ = plt.legend(loc='best')
    plt.show()
    IOB = df.values.tolist()
    # outlier detection of EGV
    df = pd.DataFrame(CGM_BGM, columns=['time', 'CGM'])
    outliers_fraction = 0.05
    model = IsolationForest(contamination=outliers_fraction)
    pdf = pd.DataFrame(CGM_BGM, columns=['time', 'CGM'])
    model.fit(pdf.values)
    pdf['anomaly2'] = pd.Series(model.predict(pdf.values))
    # visualization of EGV outliers
    df['anomaly2'] = pd.Series(pdf['anomaly2'].values, index=df.index)
    a = df.loc[df['anomaly2'] == -1]  # anomaly
    _ = plt.figure(figsize=(18, 6))
    _ = plt.plot(df['CGM'], color='blue', label='Normal')
    _ = plt.plot(a['CGM'], linestyle='none', marker='X',
                 color='red', markersize=12, label='Anomaly')
    _ = plt.xlabel('Time')
    _ = plt.ylabel('CGM')
    _ = plt.title('CGM Anomalies')
    _ = plt.legend(loc='best')
    plt.show()
    CGM_BGM = df.values.tolist()

    # lists for data points for plot

    X = []
    Y = []

    for i in IOB:
        if i[2] != -1:
            X.append(i[0])
            Y.append(i[1])

    plt.scatter(X, Y, s=1)
    plt.title('IOB over time')
    plt.show()

    X2 = []
    Y2 = []

    for i in CGM_BGM:
        if i[2] != -1:
            X2.append(i[0])
            Y2.append(i[1])

    plt.scatter(X2, Y2, s=1)
    plt.title('CGM over time')
    plt.show()
