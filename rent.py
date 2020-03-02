'''
Sergio Chairez
Maksym Sagadin
Back End
'''

from collections import namedtuple
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib



#Constants
START_MONTH, START_YEAR = 5, 2018
END_MONTH, END_YEAR = 8, 2019

#Decorator
def printNums(func):
    def inner(*args, **kwargs):
        print('Return value of inner fn:\n', f{func(*args, **kwargs)})
        return func(*args, **kwargs)
    return inner


# Part A
def read_data(*filenames):
    '''
    This function will unpack a list of file names and read in the files and create and return
    data structures with the information from the read in files.
    '''
    cityInfoList = []
    CityInfo = namedtuple('CityInfo', ['zip', 'city'])
    unique_cities = []
    for filename in filenames:
        if filename == 'zipCity.csv':
            with open(filename, 'r', newline="") as file1:
                reader = csv.reader(file1)
                for line in reader:
                    cityInfoList.append(CityInfo._make(line))
                    if cityInfo.city not in unique_cities:
                        unique_cities.append(cityInfo.city)
                # for cityInfo in cityInfoList:
                    # if cityInfo.city not in unique_cities:
                    #     unique_cities.append(cityInfo.city)

        elif filename == 'rent.csv':
            rentArr = np.loadtxt("rent.csv", delimiter=',', dtype=float)
        else:
            print("Filename is not found")
            raise IOError # :)

    return cityInfoList, rentArr, unique_cities

  

# part B
@printNums
def mean_rental_price(cityInfoList, rentArr, unique_cities):
    '''
    This function creates and returns an array containing the mean of the monthly rent prices
    '''
    monthlyRentMeanList = []
    cityRowStart, cityRowEnd, idx = 0, 0, 0
    for i in range(len(cityInfoList)):
        if cityInfoList[i].city == unique_cities[idx]:
            cityRowEnd += 1  # 1,2,3,4,11
        else:
            
            monthlyRentMeanList.append(
                rentArr[cityRowStart:cityRowEnd].mean(0))
            cityRowStart, cityRowEnd = cityRowEnd, cityRowEnd + 1
            idx += 1
    monthlyRentMeanList.append(rentArr[cityRowStart:cityRowEnd].mean(0))
    
    return np.array(monthlyRentMeanList, dtype=float)


def x_list_ticks():
    '''
    This function creates and returns a list of the incrementing from the START_MONTH &
    START_YEAR to the end of END_MONTH & END_YEAR
    '''
    startVal = str(START_MONTH) + '/' + str(START_YEAR)
    listX = []
    listX.append(startVal)
    m, y = START_MONTH + 1, START_YEAR
    while listX[-1] != (str(END_MONTH) + '/' + str(END_YEAR)):
        listX.append(str(m) + "/" + str(y))
        m += 1
        if (m > 12):
            m = 1
            y += 1
    return listX


def plot_rental_price_trend(meanMonthlyCityRatesArr, cityInfoList, unique_cities, cityChoice):
    '''
    This function plots the graph of a city that is passed as a parameter and if the values exist in
    the read in csv file it will plot a graph of that city of it's median rental prices or it will 
    plot a graph of the median rental prices for all the cities if all is passed as a parameter
    '''
    xtickList = x_list_ticks()
    # all cities
    if cityChoice == "All":
        index = 0
        '''   old 
        for row in meanMonthlyCityRatesArr:
            plt.title("Rental Prices Over Time")
            plt.ylabel("Rental Prices (dollars)")
            plt.plot(row, '*-', label=unique_cities[index])
            plt.legend(fontsize=7 ,loc='best')
            plt.xticks(np.arange(
            0, 16), xtickList, rotation='vertical')
            index += 1
        '''
         #fixed
        plt.title("Rental Prices Over Time")
        plt.ylabel("Rental Prices (dollars)")
        for row in meanMonthlyCityRatesArr:    
            plt.plot(row, '*-', label=unique_cities[index])
        plt.legend(fontsize=7 ,loc='best')
        plt.xticks(np.arange(
        0, 16), xtickList, rotation='vertical')
        index += 1    
            
        plt.subplots_adjust(bottom=0.15, top=0.95, left=0.08, right=0.94)
        
    # one city
    else: #elif cityChoice in unique_cities:
        index = unique_cities.index(cityChoice)
        title = f"Rental Prices Over Time in {cityChoice}"
        ylabel = "Rental Prices (dollars)"
        plt.title(title)
        plt.ylabel(ylabel)
        plt.plot(meanMonthlyCityRatesArr[index], '*-', label=cityChoice)
        plt.xticks(np.arange(
            0, 16), xtickList, rotation='vertical')
        plt.legend(loc='best')  #clare said tp make this smaller
        plt.subplots_adjust(bottom=0.15, top=0.95, left=0.08, right=0.94)
       
    # else:
    #     return "That city is not part of the list"



# part d

@printNums
def bar_graph_zip(rentArr, cityInfoList):
    '''
    This function creates a bar graph that plots the most current rental prices for each zip code
    and returns a sorted array with the most current rental prices for each zip code
    '''
    num_rows = rentArr.shape[0]
    xDataList = [str(str(cityInfoList[i].zip) + '\n' +
                        str(cityInfoList[i].city)) for i in range(num_rows)]
    yDataList = [rentArr[i, -1] for i in range(num_rows)]
    yLabelStr = 'Median Monthly Rental Prices for Month: ' + str(END_MONTH) + '/' + str(END_YEAR)
    sortedList = [list(a) for a in zip(xDataList, yDataList)]
    sortedList = sorted(sortedList, key=lambda x: x[1])
    #clear the existing lists
    xDataList.clear()
    yDataList.clear()
    # append sorted values
    for zipcode, rentprices in sortedList:
        xDataList.append(zipcode)
        yDataList.append(rentprices)

    plt.bar(xDataList, yDataList, align="center", width=0.6)  
    #ticks,labels
    plt.xticks(xDataList, fontsize = 7, rotation=45)

    plt.xlabel('Zip Codes', va='bottom')
    plt.ylabel(yLabelStr)
    
    axes = plt.gca()
    axes.set_ylim([2400, 4500])
    plt.subplots_adjust(bottom=0.28, top=0.92, left=0.08, right=0.94)
  
    
    # This function / method returns the current rental price for all zip codes
    return np.sort(yDataList)




if __name__ == "__main__":
    # note: 24 * 16 #16 months b/w 05/2018 and 08/2019
    filenames = ['zipCity.csv', 'rent.csv']
    #read in data
    cityInfoList, rentArr, unique_cities = read_data(*filenames)
    # Calculate the mean (average) monthly rental price
    # for cities across all zip codes
    meanMonthlyCityRatesArr = mean_rental_price(cityInfoList, rentArr, unique_cities)

    # # Plot the price trend for SJ (ONE CITY)
    plot_rental_price_trend(meanMonthlyCityRatesArr, cityInfoList, unique_cities, 'San Jose')
    plot_rental_price_trend(meanMonthlyCityRatesArr,
                            cityInfoList,unique_cities, 'All')

                
    
    #Plot the most current prices for all zip codes
    bar_graph_zip(rentArr, cityInfoList)

   

