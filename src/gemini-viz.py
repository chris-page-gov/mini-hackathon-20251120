import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load and Filter Data
df = pd.read_csv('OECD.STI.STP,DSD_RDS_GOV@DF_GBARD_NABS07,1.0+all.csv')

# Define comparison group: UK, US, and Major EU Economies
target_countries = ['GBR', 'USA', 'DEU', 'FRA', 'ITA', 'ESP', 'NLD']
target_year = 2023 # Latest year with full coverage for these nations

# Filter for Dollar Values (PPP) and Current Prices
df_filtered = df[
    (df['REF_AREA'].isin(target_countries)) &
    (df['TIME_PERIOD'] == target_year) &
    (df['UNIT_MEASURE'] == 'USD_PPP') &
    (df['PRICE_BASE'] == 'V')
].copy()

# Map NABS codes to readable names
short_names = {
    'NABS01': 'Earth Exploration', 'NABS02': 'Environment',
    'NABS03': 'Space', 'NABS04': 'Transport/Telecom',
    'NABS05': 'Energy', 'NABS06': 'Ind. Production',
    'NABS07': 'Health', 'NABS08': 'Agriculture',
    'NABS09': 'Education', 'NABS10': 'Culture/Media',
    'NABS11': 'Political/Social', 'NABS14': 'Defence',
    'NABS12': 'Gen. Knowledge (Universities)', 
    'NABS13': 'Gen. Knowledge (Other)'
}

# 2. Calculate "Percentage of Total Budget" for Heatmap
# Get Total GBARD for each country to calculate shares
totals = df_filtered[df_filtered['SEO'] == '_T'].set_index('REF_AREA')['OBS_VALUE']

# Filter for specific objectives (excluding totals)
df_main = df_filtered[df_filtered['SEO'].isin(short_names.keys())].copy()
df_main['SEO_Name'] = df_main['SEO'].map(short_names)

# Calculate % share
df_main['Percentage'] = df_main.apply(lambda row: (row['OBS_VALUE'] / totals[row['REF_AREA']]) * 100, axis=1)
df_main['Value_Billion'] = df_main['OBS_VALUE'] / 1000  # Convert Millions to Billions

# 3. Visualisation A: Heatmap (Priorities)
heatmap_data = df_main.pivot(index='REF_AREA', columns='SEO_Name', values='Percentage')
# Sort columns by average popularity for cleaner look
col_order = heatmap_data.mean().sort_values(ascending=False).index
heatmap_data = heatmap_data[col_order]

plt.figure(figsize=(14, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=.5)
plt.title(f'Government R&D Priorities: % of Total Budget ({target_year})')
plt.tight_layout()
plt.savefig('heatmap_priorities.png')

# 4. Visualisation B: Dumbbell Plot (Volumes)
# Sort objectives by Total Volume (Sum across all countries)
seo_order = df_main.groupby('SEO_Name')['Value_Billion'].sum().sort_values(ascending=True).index

plt.figure(figsize=(14, 10))
for i, seo in enumerate(seo_order):
    # Draw the line (range)
    row_data = df_main[df_main['SEO_Name'] == seo]
    plt.hlines(y=seo, xmin=row_data['Value_Billion'].min(), xmax=row_data['Value_Billion'].max(), color='grey', alpha=0.4)
    
    # Draw the points
    uk = row_data[row_data['REF_AREA'] == 'GBR']
    us = row_data[row_data['REF_AREA'] == 'USA']
    others = row_data[~row_data['REF_AREA'].isin(['GBR', 'USA'])]
    
    plt.scatter(others['Value_Billion'], [seo]*len(others), color='grey', s=60, alpha=0.6, label='EU Peers' if i==0 else "")
    plt.scatter(uk['Value_Billion'], [seo]*len(uk), color='red', s=120, label='UK' if i==0 else "", zorder=3)
    plt.scatter(us['Value_Billion'], [seo]*len(us), color='blue', s=120, label='USA' if i==0 else "", zorder=3)

plt.title(f'Absolute R&D Investment by Objective ({target_year})\n(Billions USD PPP)')
plt.xlabel('Billions (USD PPP)')
plt.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('dumbbell_volumes.png')
