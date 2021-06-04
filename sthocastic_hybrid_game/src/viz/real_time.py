

# If we want to draw dynamically
# Generally seems like create another thread an draw in parallel to send the data.
# Tinker https://stackoverflow.com/questions/5618620/create-dynamic-updated-graph-with-python
# https://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib

def plotoutput(ucont, uopt):
    plt.figure()
    plt.plot(tcontinuous, ucont)
    plt.xlim([0, DeltaT*(P+1)])
    plt.figure()
    plt.plot(tcontinuous, prediction(ucont, tcontinuous),
             label='Continuous response')
    plt.plot(tpredict, prediction(extend(uopt)),
             '-o', label='Optimized response')
    plt.plot(tpredict, r, label='Set point')
    plt.legend()
