import matplotlib.pyplot as plt
import csv

x = []
y = []
  
with open('btc_Time_graph_data.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    start_flag = 0
    for row in lines:
        if start_flag == 0 :
            start_flag = 1
            xlabel = row[0]
            ylabel = row[1]
            continue
        x.append(row[0][0:5])
        y.append(float(row[1]))
  
plt.plot(x, y, color = 'g', linestyle = 'dashed',
         marker = 'o',label = "Weather Data")
  
plt.xticks(rotation=25)
#plt.xlim(xmin=1, xmax=24)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title('Weather Report', fontsize = 20)
plt.grid()
plt.legend()
plt.show()