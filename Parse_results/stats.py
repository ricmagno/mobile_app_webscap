import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_name = 'google_play_reults.xlsx'                    
sheet_name = '571 for all categories'
# sheets = load_workbook(excel_file, read_only=True).sheetnames


# Import the excel file and call it xls_file
excel_file = pd.ExcelFile(file_name)

# View the excel_file's sheet names
print(excel_file.sheet_names)
  
# Load the excel_file's Sheet1 as a dataframe
df = excel_file.parse(sheet_name)
print(df)

# print(excel_file.sheet_names[0])
df1 = (df.groupby(by=['Category'])['Category']
              .count()
              .reset_index(name='cnt'))

df1.sort_values(by=['cnt'], inplace=True, ascending=False)
print(df1)
total = df1['cnt'].sum()
print ('Total apps: ', total)

# df1 = df1.Category.drop_duplicates()
# print(df1)
# exit()

df_selected = df.loc[(df['Category'] == 'Social') |
                     (df['Category'] == 'Dating') |
                     (df['Category'] == 'Lifestyle') |
                     (df['Category'] == 'Communication')]

print(df_selected)
# df.set_index('Category')

# total_selected = df_selected['cnt'].sum() #no need
# print(df_selected, 'Total: ', total_selected, '(', 100*(total_selected/total), '%)' )
# print('Apps dismissed by category', total - total_selected, '(', 100 * (1 - (total_selected/total)), '%)' )


# df1['pareto'] = 100 *df1.cnt.cumsum() / df1.cnt.sum()
# print(df1)

col_name = 'None Target MSM'
df2 = df_selected.loc[(df_selected[col_name].notnull())]
print(df2)


col_name = 'Not MSM social media dating app '
df3 = df2.loc[(df2[col_name].isnull())]
print(df3)


col_name = 'Non English'
df3 = df2.loc[(df2[col_name].isnull())]
print(df3)

col_name = 'Paid app'
df4 = df3.loc[(df3[col_name].isnull())]
print(df4)

col_name = 'Not for NZ users'
df5 = df4.loc[(df4[col_name].isnull())]
print(df5)

col_name = 'Review'
df6 = df5.loc[(df5[col_name].notnull())]
# df6 = df6[col_name], dtype=int)
df6[col_name] = df[col_name].astype(str).astype(float)
df6 = df6.loc[(df6[col_name] > 0)] 
print(df6)


df6.to_csv('android_msm_apps.csv')

# df_selected = df1.loc[(df1[col_name] != 'Social') |
#                       (df1['Category'] == 'Dating') |
#                       (df1['Category'] == 'Lifestyle') |
#                       (df1['Category'] == 'Communication')]




# print(df1['Category'].any({'Dating','Social'}))







# df = df1
# fig, axes = plt.subplots()
# ax1 = df.plot(use_index=True, y='cnt',  kind='bar', ax=axes)
# ax2 = df.plot(use_index=True, y='pareto', marker='D', color="C1", kind='line', ax=axes, secondary_y=True)
# ax2.set_ylim([0,110])
# plt.show()




# df1 = (df.groupby('App name')['Category'].value_counts()
# print(df1.Category.unique())
# df2 = df1.Category.drop_duplicates()
# print(df2)

# df = pd.read_excel (excel_file, 'Sheet_name'=sheets[6])
# print(df)
