from matplotlib import pyplot as plt

def plot_pie_chart(credits:float, debits:float):
    fig = plt.figure()

    #create axis for pie chart
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')

    types = ['Credits', 'Debits']
    amounts = [credits, -debits]        # -debits to show the debits on pie chart as +ve num

    ax.pie(amounts, labels=types, autopct='%1.2f%%')    #autopct is auto_percenage

    return fig;

