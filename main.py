import pandas as pd

PROJECTNAME = 'TURQUOISE'

# IMPORT SALE DF
sale_df = pd.read_csv('./sample/sale_sample.csv', usecols=['project', 'transaction.contractDate', 'transaction.area', 'transaction.price', 'transaction.propertyType', 'transaction.tenure', 'transaction.floorRange', 'transaction.typeOfSale', 'transaction.district'])
sale_df.columns = ['project', 'contractDate', 'area', 'price', 'propertyType', 'tenure', 'floorRange', 'typeOfSale', 'district']
sale_df = sale_df[(sale_df['propertyType'] == 'Condominium') | (sale_df['propertyType'] == 'Apartment')]

# IMPORT RENT DF
rent_df = pd.read_csv('./sample/rent_sample.csv', usecols=['project', 'street', 'rental.leaseDate', 'rental.propertyType', 'rental.areaSqm', 'rental.areaSqft', 'rental.rent', 'rental.district', 'rental.noOfBedRoom'])
rent_df.columns = ['project', 'street', 'contractDate', 'propertyType', 'areaSqm', 'areaSqft', 'rent', 'district', 'noOfBedRoom']
rent_df = rent_df[rent_df['propertyType'] == 'Non-landed Properties']

# MERGING RENT AND SALE
merged = pd.merge(rent_df, sale_df, on=['project', 'district'], how='inner')
split = merged.areaSqm.str.split('-',expand=True)
merged['lowSqmAdj'] = pd.to_numeric(split[0], errors='coerce')
merged['highSqmAdj'] = pd.to_numeric(split[1], errors='coerce')
merged['isSameSize'] = ((merged.area > merged.lowSqmAdj) & (merged.area < merged.highSqmAdj))
merged = merged[merged.isSameSize == True]
merged = merged[merged.area >= 50]
merged.to_csv('merged.csv')

# GENERATING ANALYSIS TABLES
aggByProjDf = merged.groupby(['project', 'street', 'areaSqm', 'noOfBedRoom', 'tenure']).agg({'rent': 'mean', 'price': 'mean', 'district': 'count'})
aggByProjDf['calc_yield'] = (aggByProjDf.rent * 12) / aggByProjDf.price * 100
aggByProjDf.sort_values(by='calc_yield', ascending=False)
aggByProjDf.to_csv('aggByProjDf.csv')

# DRILL DOWN SPECIFIC PROJECTS
project_drill_sale = sale_df[sale_df['project'] == PROJECTNAME]
project_drill_sale.to_csv('./drilldown/project_drill_sale.csv')
project_drill_rent = rent_df[rent_df['project'] == PROJECTNAME]
project_drill_rent.to_csv('./drilldown/project_drill_rent.csv')
project_drill_merge = merged[merged['project'] == PROJECTNAME]
project_drill_merge.to_csv('./drilldown/project_drill_merge.csv')
