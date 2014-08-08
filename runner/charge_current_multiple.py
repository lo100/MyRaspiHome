#!/usr/bin/env python

#
# parse multiple HDF5 files and print graph
#

import pandas as pd

import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt

from pandas import ExcelWriter

print('Import data from HDF5 files')
store1 = pd.HDFStore("E:\\home\\2014\\07\\logfile_20140701.hdf5", mode='r')
print(store1.root.series.tarom.Total_Charge_Current.data[0:10])
store2 = pd.HDFStore("E:\\home\\2014\\07\\logfile_20140702.hdf5", mode='r')
print(store2.root.series.tarom.Total_Charge_Current.data[0:10])
store3 = pd.HDFStore("E:\\home\\2014\\07\\logfile_20140703.hdf5", mode='r')
print(store3.root.series.tarom.Total_Charge_Current.data[0:10])
store4 = pd.HDFStore("E:\\home\\2014\\07\\logfile_20140704.hdf5", mode='r')
print(store4.root.series.tarom.Total_Charge_Current.data[0:10])

# Example accessing HDF5 using MyRaspiHome framework
# -------------------------------------------------------------
# from data_accessor.data_accessor_hdf5 import DataAccessorHDF5
# da = DataAccessorHDF5()
# da.open("E:\\home\\2014\\07\\logfile_20140701.hdf5", 'r')
# parameter = ('Total_Charge_Current',)
# data = da.read('tarom', parameter)
# print(data)
# da.close()

# convert to pandas dataframes
s1 = pd.Series.from_array(store1.root.series.tarom.Total_Charge_Current.data)
df1 = pd.DataFrame(s1)
s2 = pd.Series.from_array(store2.root.series.tarom.Total_Charge_Current.data)
df2 = pd.DataFrame(s2)
s3 = pd.Series.from_array(store3.root.series.tarom.Total_Charge_Current.data)
df3 = pd.DataFrame(s3)
s4 = pd.Series.from_array(store4.root.series.tarom.Total_Charge_Current.data)
df4 = pd.DataFrame(s3)

print('Merge data')
merged = pd.merge(df1, df2)

print('Print graph')
figure = plt.figure()
#merged.plot(kind='area', stacked=False)
df1.plot(kind='area', stacked=False)
#df2.plot(kind='area', stacked=False)
#df3.plot(kind='area', stacked=False)
#df4.plot(kind='area', stacked=False)
plt.grid(True)
plt.savefig('test.png')
plt.close(figure)

print('To excel')
with ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Dateframe_1')
    #df2.to_excel(writer, sheet_name='Dateframe_2')
    #df3.to_excel(writer, sheet_name='Dateframe_3')
    #df4.to_excel(writer, sheet_name='Dateframe_4')
    #merged.to_excel(writer, sheet_name='Merged')
    
print('done')
