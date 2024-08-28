# libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# options
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', False)

# From CSVs to data frames.
inventories = pd.read_csv('inventories.csv')
inventory_minifigs = pd.read_csv('inventory_minifigs.csv')
minifigs = pd.read_csv('minifigs.csv')
inventory_sets = pd.read_csv('inventory_sets.csv')
sets = pd.read_csv('sets.csv')
themes = pd.read_csv('themes.csv')
inventory_parts = pd.read_csv('inventory_parts.csv')
parts = pd.read_csv('parts.csv')
colors = pd.read_csv('colors.csv')
part_categories = pd.read_csv('part_categories.csv')
elements = pd.read_csv('elements.csv')
part_relationships = pd.read_csv('part_relationships.csv')

# Which mini-figures are the most common?

# Five data frames were merged together to determine the theme of each mini-figure.
# Custom suffixes were added to avoid confusion in certain columns.
full_mnfgs = (minifigs.merge(inventory_minifigs, on='fig_num')
              .merge(inventories, left_on='inventory_id', right_on='id')
              .merge(sets, on='set_num', suffixes=('_minifig', '_set'))
              .merge(themes, left_on='theme_id', right_on='id', suffixes=(None, '_theme')))

# The quantity of each mini-figure was determined below.
mnfgs_grouped = full_mnfgs.groupby('fig_num', as_index=False)['quantity'].sum()


# The two previous data frames were joined to get all the necessary information about each mini-figure.
# Themes names were combined into one column, in case, the same mini-figures have more than one theme.
mnfgs = (mnfgs_grouped.merge(full_mnfgs[['fig_num', 'name_minifig', 'name', 'img_url_minifig']],
                             on='fig_num', how='inner')
         .drop_duplicates()
         .groupby(['fig_num', 'quantity', 'name_minifig', 'img_url_minifig'],
                  as_index=False).agg(name_theme=('name', ', '.join))
         .sort_values(by='quantity', ascending=False))

# How have the sizes of LEGO sets changed over time?

# The average number of LEGO parts in a set was calculated by year.
# Years in which no parts were produced were filtered out.
avg_by_year = sets.groupby('year', as_index=False)['num_parts'].mean().round(2)
avg_by_year = avg_by_year[avg_by_year['num_parts'] > 0]
# Calculated the median number.
mdn_by_year = sets.groupby('year', as_index=False)['num_parts'].median().round(2)
mdn_by_year = mdn_by_year[mdn_by_year['num_parts'] > 0]

# The data frames were compressed into a series for plotting.
series_avg = avg_by_year.set_index('year').squeeze()
series_mdn = mdn_by_year.set_index('year').squeeze()
# Plotting.
fig, ax = plt.subplots()
ax.plot(series_avg, label='average')
l, = ax.plot(series_mdn, label='median')
fig.suptitle('LEGO sets set changes over the years')
ax.grid()
ax.legend()
ax.set_xticks(np.arange(min(avg_by_year.year), max(avg_by_year.year)+1, 10.0))

# plt.show()

# What are the rarest LEGO pieces?

prts = (inventory_parts.groupby(['part_num', 'color_id', 'img_url'],
                                as_index=False)['quantity'].sum()
        .sort_values(by='quantity')
        .merge(parts, on='part_num')[['part_num', 'color_id', 'name', 'quantity', 'img_url']])

# What are the top 3 biggest sets?

bgst_st = (sets.sort_values(by='num_parts', ascending=False).head(3)
           .merge(themes, left_on='theme_id', right_on='id')
           .rename(columns={'name_x': 'set_name', 'name_y': 'theme_name'})
           [['set_num', 'set_name', 'theme_name', 'year', 'num_parts', 'img_url']])

# What colours are used more often?

clrs = (inventory_parts.groupby('color_id',
                                as_index=False)['quantity'].sum()
        .sort_values(by='quantity',ascending=False)
        .merge(colors, left_on='color_id', right_on='id'))

# All necessary information about parts in one data frame.

df = (pd.merge(inventories, inventory_parts,
               how='left', left_on='id', right_on='inventory_id')
      .merge(sets,
             on='set_num', suffixes=('_part','_set'))
      .merge(themes,
             left_on='theme_id', right_on='id', suffixes=('_set', "_theme"))
      .merge(parts,
             on='part_num')
      .merge(colors,
             left_on='color_id', right_on='id', suffixes=('_part', '_col'))
      .merge(part_categories,
             left_on='part_cat_id', right_on='id', suffixes=('_col', '_part_cat'))
      .rename(columns={'num_parts': 'num_parts_in_set', 'name': 'name_cat'})
      .loc[:, ['part_num', 'name_part', 'parent_id', 'part_material', 'part_cat_id',
               'name_cat', 'id_col', 'name_col', 'rgb', 'quantity', 'img_url_part',
               'inventory_id', 'set_num', 'name_set', 'year', 'num_parts_in_set',
               'img_url_set','theme_id', 'name_theme']]
      .drop_duplicates()
      )
# The following questions were answered using this data frame.

# What LEGO parts are used most often?

# The number of sets, their IDs and names were placed in three columns respectively for each LEGO part.
gr_prts = (df.groupby(['part_num', 'name_part'], as_index=False)
           .agg(set_cnt=('set_num', 'count'),
                set_num=('set_num', ', '.join),
                set_name=('name_set', ', '.join))
           )

most_used = (df.groupby(['part_num', 'name_part', 'name_cat', 'name_col', 'img_url_part'],
                        as_index=False)['quantity'].sum()
             .merge(gr_prts[['part_num', 'name_part', 'set_cnt']], on=['part_num', 'name_part'])
             .sort_values(by='quantity', ascending=False).iloc[:, [0, 1, 2, 3, 5, 6, 4]])

# What LEGO pieces were included in most sets?

most_number_of_sets = most_used.sort_values('set_cnt', ascending=False)



