# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 10:23:23 2026

@author: Luche_Cameron
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('C:/Users/Luche_Cameron/Downloads/Super Store dataset/train.csv')
print(df.isnull().sum())

#Task 1 : Basic cleaning ,preparing and formating of the data

print(df.info())

df=df.dropna()
print(df.isnull().sum())

#converting date format
df['Order Date'] = pd.to_datetime(df['Order Date'], format = '%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format = '%d/%m/%Y')
print(df.duplicated().any())

df['Postal Code'] = df['Postal Code'].astype('str')

#==============================================================================
# Task 2 : Sales Performance over view
Total_Sales = df['Sales'].sum()
print('The total amount of Sales for this duration is R',Total_Sales)

AOV = df.groupby('Order ID')['Sales'].sum().mean()
print('The average Sales per oreder is : ' , AOV)

uniqueCX = df['Customer ID'].nunique()
print('The amount of unique customers is:' , uniqueCX)

uniqueOrder = df['Order ID'].nunique()
print('The amount of unique orders is :', uniqueOrder)
 
''' 
Business Question: How is the business performing overall?
Over a Span of 3 years this is the KPIs and it indicates the performance of the
business:
The total amount of Sales for this duration is R 2252607.4127
The amount of unique customers is 793
The amount of unique orders is 4916.
'''
#=============================================================================
# Task 3: Sales by Category & Sub-Category

CategoryRevenue = df.groupby('Category')['Sales'].sum().sort_values()
print(CategoryRevenue)
SubCategoryRevenue = df.groupby('Sub-Category')['Sales'].sum().sort_values()
print('The total sales by Sub-Category is :' , SubCategoryRevenue)

print('The top 5 performing sub-categories in terms of revenue is :' ,
      SubCategoryRevenue.tail())
print('The bottom 5 performing categories in terms of revenue is : ' , 
      SubCategoryRevenue.head())
'''
Business Question: Which products drive the most revenue?

This is the 5 Product categories  the brings in the most amount of revenue:
    
Binders        R200028.78
Tables         R202810.62
Storage        R217779.10
Chairs         R322107.53
Phones         R326487.69
'''
#==============================================================================
# Task 4: Regional insights.

RegionRevenue = df.groupby('Region')['Sales'].sum()
print(RegionRevenue)

StatesRevenue = df.groupby('State')['Sales'].sum().sort_values().reset_index()
print('The top 5 states by sales are', StatesRevenue.tail())

CityRevenue = df.groupby('City')['Sales'].sum().sort_values()
print('The cities with highest revenues are ' , CityRevenue.tail(10))

#Bonus
CustomerRevenue = (
    df.groupby('Region').agg(total_sales = ('Sales' , 'sum'),
                             customer_count= ('Customer ID', 'nunique'))
    )
CustomerRevenue['CustomerRevenue'] = (CustomerRevenue['total_sales'] /
                                      CustomerRevenue['customer_count'])
print(CustomerRevenue)

'''
Business Question: Which regions and states perform best?
Region
Central   R492646.9132
East      R660589.3560
South     R389151.4590
West      R710219.6845
 
The top 5 states by sales are            
  Pennsylvania-R116276.6500
    Washington-R135206.8500
         Texas-R168572.5322
      New York-R306361.1470
    California-R446306.4635
    
    
'''
#==============================================================================
#Task 5 : Customer Segement Analysis
SegmentRev = df.groupby('Segment')['Sales'].sum().reset_index().sort_values('Sales', ascending = False)
pd.options.display.float_format = '{:,.2f}'.format
print(SegmentRev)

aovPerSegment = (df.groupby('Segment').agg(total_sales = ('Sales','sum') , 
                                           total_orders = ('Order ID', 'nunique')))

aovPerSegment['aovPerSegment'] = (aovPerSegment['total_sales']/aovPerSegment['total_orders'])
print(aovPerSegment)

orders_per_customer = (
    df.groupby('Segment')
      .agg(orders=('Order ID','nunique'),
           customers=('Customer ID','nunique'))
)
orders_per_customer['orders_per_customer'] = (
    orders_per_customer['orders'] / orders_per_customer['customers']
)

'''
Business Question: Which customer segments are most valuable?
The most valuable customer segment is Consumer with an amount of R1,146,708.15.
'''
#==============================================================================
#task 6 :Time-Series Analysis

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['YearMonth'] = df['Order Date'].dt.to_period('M')

# Aggregate monthly sales
monthly_sales = (
    df.groupby('YearMonth')['Sales']
      .sum()
      .reset_index()
)

# Convert Period to Timestamp for plotting
monthly_sales['YearMonth'] = monthly_sales['YearMonth'].dt.to_timestamp()

print("Monthly Sales:")
print(monthly_sales)


df['Year'] = df['Order Date'].dt.year
yearly_sales = df.groupby('Year')['Sales'].sum()
yoy_growth = yearly_sales.pct_change() * 100

print("Year-over-Year Sales Growth (%):")
print(yoy_growth)

peak_sales_months = monthly_sales.sort_values('Sales', ascending=False).head(3)

print("\nTop 3 Peak Sales Months:")
print(peak_sales_months)


monthly_sales['Rolling_3_Month_Avg'] = (
    monthly_sales['Sales']
    .rolling(window=3)
    .mean()
)

print("\nMonthly Sales with Rolling Average:")
print(monthly_sales)


plt.figure(figsize=(10, 5))
plt.plot(monthly_sales['YearMonth'], monthly_sales['Sales'], label='Monthly Sales')
plt.plot(
    monthly_sales['YearMonth'],
    monthly_sales['Rolling_3_Month_Avg'],
    label='3-Month Rolling Average'
)

plt.title('Monthly Sales Trend with Rolling 3-Month Average')
plt.xlabel('Month')
plt.ylabel('Sales Amount')
plt.legend()
plt.tight_layout()
plt.show()

#==============================================================================
#Task 7 :Shipping Performance
RevenueShipMode = df.groupby('Ship Mode')['Sales'].sum()
print(RevenueShipMode.sort_values())

df['Delivery Time(Days)'] = (df['Ship Date'] - df['Order Date']).dt.days

OrdAmountByMode = df['Ship Mode'].value_counts()
print(OrdAmountByMode)
'''
Business Question: Does shipping mode affect sales?
Standard Class has the highest revenue but the longest delivery time,
 indicating customers prioritize cost over speed.

 '''
#==============================================================================
#Task 8 :Product-Level Insights
ProductRevenue = df.groupby('Product Name')['Sales'].sum().sort_values()
print('The  top 10 products  value is ', ProductRevenue.tail(10))
print('Products with very low sales', ProductRevenue.head(10))
'''
Business Question: Which products should we promote or drop?
The top 5 product products based on revenue is :
    GBC DocuBind TL300 Electric Binding System                                 -R19,823.48
    HON 5400 Series Task Chairs for Big and Tall                               -R21,870.58
    Cisco TelePresence System EX90 Videoconferencing Unit                      -R22,638.48
    Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bin -R27,453.38
    Canon imageCLASS 2200 Advanced Copier                                      -R1,599.82
    
Theses are also the product i would recommend promoting

The bottom 5 products based on value is :
    Eureka Disposable Bags for Sanitaire Vibra Groomer I Upright Vac -R1.62
    Avery 5                                                          -R5.76
    Xerox 20                                                         -R6.48
    Grip Seal Envelopes                                              -R7.07
    Acme Serrated Blade Letter Opener                                -R7.63
These are the product i recommend dropping
 '''

#==============================================================================
#Task 9 :Data Visualization


   #Bar chart: Sales by Category
CategoryRevenue.plot(kind = 'bar' , x = 'Category' , y = 'Sales',
                     legend = False)
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Sales Amount')
plt.show()

#Line chart: Monthly sales trend
monthly_sales.plot(kind='line', x='YearMonth', y='Sales', legend=False)
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales Amount')
plt.show()


#Bar chart: Sales by Segment
SegmentRev.plot(kind = 'bar' , x = 'Segment', y = 'Sales')
plt.title('Sales by Segment')
plt.xlabel('Segment')
plt.ylabel('Total Sales Amount')
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.show()



# creating a map chart in python, 
# make sue you have the revelant variable for it
import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'browser'


# now what you doing here is preparing you country names and making sort3
# it is the correct format so thet the system can locate it on the map
us_state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
    'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN',
    'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}


StatesRevenue['State Code'] = StatesRevenue['State'].map(us_state_abbrev)

# Craeting the actul color map

fig = px.choropleth(
    StatesRevenue,
    locations = 'State Code',
    locationmode = 'USA-states',
    color = 'Sales',
    scope = 'usa',
    title = 'Sales by State',
    color_continuous_scale = 'Blues' , 
    labels = {'Sales': 'Total Sales'}
    )

fig.show()

