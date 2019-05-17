import datetime
import random
import matplotlib.pyplot as plt

times = []
for i in range(12):
    times.append(datetime.datetime.now().strftime("%H:%M:%S"))
    time.sleep(2)

#x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
y = [i+random.gauss(0,1) for i,_ in enumerate(times)]

# plot
plt.plot(times,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

#plt.show()

plt.savefig('testPlot.png')
