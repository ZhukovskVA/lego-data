# libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# options for table visualization
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth',False)

# making data frames from all csv
inventories=pd.read_csv('inventories.csv')
inventory_minifigs=pd.read_csv('inventory_minifigs.csv')
minifigs=pd.read_csv('minifigs.csv')
inventory_sets=pd.read_csv('inventory_sets.csv')
sets=pd.read_csv('sets.csv')
themes=pd.read_csv('themes.csv')
inventory_parts=pd.read_csv('inventory_parts.csv')
parts=pd.read_csv('parts.csv')
colors=pd.read_csv('colors.csv')
part_categories=pd.read_csv('part_categories.csv')
elements=pd.read_csv('elements.csv')
part_relationships=pd.read_csv('part_relationships.csv')

# Most common minifigures?
full_minifigs = (minifigs.merge(inventory_minifigs, on='fig_num').sort_values(by='quantity', ascending=False)
                 .merge(inventories,left_on='inventory_id',right_on='id')
                 .merge(sets,on='set_num')
                 .merge(themes,left_on='theme_id',right_on='id'))

mnfg_grouped = full_minifigs.groupby('fig_num',as_index=False)['quantity'].sum()
minifigs_necessary=full_minifigs[['fig_num','name_x','name','img_url_x']].rename(columns={'name_x':'minifig_name',
     'name':'theme_name','img_url_x':'minifig_url'})
mnfgs_grouped_head=mnfg_grouped.merge(minifigs_necessary,on='fig_num',how='inner').drop_duplicates(subset='fig_num').sort_values(
    by='quantity',ascending=False).head(10)
# print(mnfgs_grouped_head)
#           fig_num  quantity                                           minifig_name     theme_name                                            minifig_url
# 4817   fig-002330  102       Battle Droid, One Bent Arm, One Straight Arm           Star Wars      https://cdn.rebrickable.com/media/sets/fig-002330.jpg
# 2592   fig-001087  101       Woman, Blue Torso with White Arms, White Legs          Serious Play   https://cdn.rebrickable.com/media/sets/fig-001087.jpg
# 4589   fig-002229  60        Skeleton, Standard Face, Ball Joint Arms (3626b Head)  Service Packs  https://cdn.rebrickable.com/media/sets/fig-002229.jpg
# 2661   fig-001127  51        Classic Spaceman, White with Airtanks (3842a Helmet)   Classic Space  https://cdn.rebrickable.com/media/sets/fig-001127.jpg
# 6865   fig-003612  50        Battle Droid, Two Bent Arms                            Star Wars      https://cdn.rebrickable.com/media/sets/fig-003612.jpg
# 55     fig-000020  50        Classic Spaceman, Red with Airtanks (3842a Helmet)     Classic Space  https://cdn.rebrickable.com/media/sets/fig-000020.jpg
# 13034  fig-007625  34        Pit Crew, Red Torso, Red Legs, Ferrari                 Ferrari        https://cdn.rebrickable.com/media/sets/fig-007625.jpg
# 800    fig-000285  32        Man, Blue Shirt, Blue Legs, Red Hard Hat               Classic Town   https://cdn.rebrickable.com/media/sets/fig-000285.jpg
# 4346   fig-002118  29        Steve                                                  Minecraft      https://cdn.rebrickable.com/media/sets/fig-002118.jpg
# 12168  fig-006974  29        Martian                                                Mars Mission   https://cdn.rebrickable.com/media/sets/fig-006974.jpg
#
# The most common -- fig-002330.

# How have the sizes of LEGO sets changed over time?
avg_by_year=sets.groupby('year',as_index=False)['num_parts'].mean().round(2)
avg_by_year=avg_by_year[avg_by_year['num_parts']>0]

mdn_by_year = sets.groupby('year', as_index=False)['num_parts'].median().round(2)
mdn_by_year = mdn_by_year[mdn_by_year['num_parts'] > 0]


series_avg=avg_by_year.set_index('year').squeeze()             # DataFrame to Series
series_mdn = mdn_by_year.set_index('year').squeeze()

fig, ax = plt.subplots()                                                # Plot
ax.plot(series_avg, label='average')
l, = ax.plot(series_mdn, label='median')
fig.suptitle('LEGO sets set changes over the years')
ax.grid()
ax.legend()
ax.set_xticks(np.arange(min(avg_by_year.year),max(avg_by_year.year)+1,10.0))

# plt.show()

# What are the rarest LEGO pieces?
prts = (inventory_parts.groupby(['part_num','color_id','img_url'], as_index=False)['quantity']
        .sum().sort_values(by='quantity').merge(parts,on='part_num'))
# print(prts[prts['quantity'] == 1][['part_num','color_id','name','quantity','img_url']])
#
#           part_num  color_id                                                                  name  quantity                                                                                                        img_url
# 0      3069bpr0274  14        Tile 1 x 2 with Groove and Brown Square Print                         1         https://cdn.rebrickable.com/media/parts/elements/6289703.jpg
# 1      3069bpr0273  15        Tile 1 x 2 with Groove and Joker Playing Card Print                   1         https://cdn.rebrickable.com/media/parts/elements/6287793.jpg
# 2      upn0491      9999      Wing, Left, Dragon, Azure Bones, Green and Dark Green Webbing         1         https://cdn.rebrickable.com/media/parts/photos/9999/upn0491-9999-a11c2a1c-6fc3-4218-b0fb-448c2718b275.jpg
# 3      3069bpr0267  19        Tile 1 x 2 with Groove and Ginger Bread Man/Baby Under Blanket print  1         https://cdn.rebrickable.com/media/parts/elements/6271241.jpg
# 4      upn0485c02   9999      Dimensions Game Pad - Xbox ONE                                        1         https://cdn.rebrickable.com/media/parts/photos/9999/upn0569c02-9999-2127e48f-847a-4af8-ba90-1bd7bb8ca06b.jpg
# ...           ...    ...                                 ...                                       ..                                                                                                                  ...
# 34390  1022Apr0207  1017      Modulex Tile 2 x 2 with White 'q' print, without Internal Supports    1         https://cdn.rebrickable.com/media/parts/photos/1013/1022A-1013-ecd6cc67-8ad7-4adc-8a2e-91085594e619.jpg
# 34391  004231       9999      Sticker Sheet for Set 263-1                                           1         https://cdn.rebrickable.com/media/parts/photos/9999/004231-9999-780093c7-f60e-4e4e-8ab4-f0d67b08d386.jpg
# 34392  upn0461      9999      Poster, Road Safety Kit                                               1         https://cdn.rebrickable.com/media/parts/photos/9999/upn0486-9999-10f05988-c554-46eb-b3bc-0c92c4e388c8.jpg
# 34393  1042Apr0005  1019      Modulex Tile 2 x 4 with White 'r' print, without Internal Supports    1         https://cdn.rebrickable.com/media/parts/photos/1018/1042Apr0005-1018-99f1a04b-781d-4b93-989f-c98c1e85f510.jpg
# 34394  28621        84        Minifig Head Plain [Vented Stud - 2 Holes]                            1         https://cdn.rebrickable.com/media/parts/elements/6454735.jpg
#
# [34395 rows x 5 columns]

# What are the  top 3 biggest sets?

bgst_st = sets.sort_values(by='num_parts', ascending = False).head(3).merge(themes,left_on='theme_id',right_on='id').rename(
    columns={'name_x':'set_name','name_y':'theme_name'})
# print(bgst_st[['set_num','set_name','theme_name','year','num_parts','img_url']])
#     set_num                       set_name        theme_name  year  num_parts                                              img_url
# 0  31203-1   World Map                      LEGO Art          2021  11695      https://cdn.rebrickable.com/media/sets/31203-1.jpg
# 1  10307-1   Eiffel Tower                   Icons             2022  10001      https://cdn.rebrickable.com/media/sets/10307-1.jpg
# 2  BIGBOX-1  The Ultimate Battle for Chima  Legends of Chima  2015  9987       https://cdn.rebrickable.com/media/sets/bigbox-1.jpg

# What are the top 5 most used colors?
clrs = inventory_parts.groupby('color_id',as_index=False)['quantity'].sum().sort_values(by='quantity',ascending=False).merge(
    colors,left_on='color_id',right_on='id').head(5)
# print(clrs[['color_id','name','rgb','quantity']])
#    color_id               name     rgb  quantity
# 0  0         Black              05131D  790116
# 1  71        Light Bluish Gray  A0A5A9  487428
# 2  15        White              FFFFFF  473885
# 3  72        Dark Bluish Gray   6C6E68  347033
# 4  4         Red                C91A09  306296

# All the necessary information about the parts in one table.
df = pd.merge(
    inventories,inventory_parts,how='left',left_on='id',right_on='inventory_id'
).merge(
    sets,on='set_num', suffixes=('_part','_set')
).merge(
    themes,left_on='theme_id',right_on='id', suffixes=('_set',"_theme")
).merge(
    parts,on='part_num'
).merge(
    colors,left_on='color_id',right_on='id',suffixes=('_part','_col')
).merge(
    part_categories,left_on='part_cat_id',right_on='id', suffixes=('_col','_part_cat')
).rename(
    columns={'num_parts':'num_parts_in_set', 'name':'name_cat'}
).loc[:,['part_num','name_part','parent_id','part_material','part_cat_id','name_cat','id_col','name_col','rgb',
          'quantity','img_url_part','inventory_id','set_num','name_set','year','num_parts_in_set','img_url_set',
          'theme_id','name_theme']].drop_duplicates()
# print(df)

#                part_num                                                                               name_part  parent_id part_material  part_cat_id                  name_cat  id_col              name_col     rgb  quantity                                                                                             img_url_part  inventory_id set_num                                                  name_set  year  num_parts_in_set                                        img_url_set  theme_id     name_theme
# 0        48379c04        Large Figure Torso and Legs, with Black Feet                                            458.0      Plastic       41           Large Buildable Figures   72      Dark Bluish Gray      6C6E68  1.0       https://cdn.rebrickable.com/media/parts/photos/1/48379c01-1-839cbcec-62de-4733-ba23-20f35f4dd5d5.jpg     1.0           7922-1  McDonald's Sports Set Number 6 - Orange Vest Snowboarder  2004  5                 https://cdn.rebrickable.com/media/sets/7922-1.jpg  460       Gravity Games
# 1        48395           Sports Snowboard from McDonald's Promotional Set                                        458.0      Plastic       27           Minifig Accessories       7       Light Gray            9BA19D  1.0       https://cdn.rebrickable.com/media/parts/photos/7/48395-7-b9152acf-2fa5-4836-a04d-5b7fd39c2406.jpg        1.0           7922-1  McDonald's Sports Set Number 6 - Orange Vest Snowboarder  2004  5                 https://cdn.rebrickable.com/media/sets/7922-1.jpg  460       Gravity Games
# 2        stickerupn0077  Sticker Sheet for Set 7922-1                                                            458.0      Plastic       58           Stickers                  9999    [No Color/Any Color]  05131D  1.0       NaN                                                                                                      1.0           7922-1  McDonald's Sports Set Number 6 - Orange Vest Snowboarder  2004  5                 https://cdn.rebrickable.com/media/sets/7922-1.jpg  460       Gravity Games
# 3        upn0342         Sports Promo Paddle from McDonald's Sports Sets                                         458.0      Plastic       27           Minifig Accessories       0       Black                 05131D  1.0       https://cdn.rebrickable.com/media/parts/photos/135/upn0342-135-cde3e1b7-1f79-40bf-9b79-46fcf5dbae96.jpg  1.0           7922-1  McDonald's Sports Set Number 6 - Orange Vest Snowboarder  2004  5                 https://cdn.rebrickable.com/media/sets/7922-1.jpg  460       Gravity Games
# 4        upn0350         Sports Promo Figure Head Torso Assembly McDonald's Set 6 (7922)                         458.0      Plastic       13           Minifigs                  25      Orange                FE8A18  1.0       NaN                                                                                                      1.0           7922-1  McDonald's Sports Set Number 6 - Orange Vest Snowboarder  2004  5                 https://cdn.rebrickable.com/media/sets/7922-1.jpg  460       Gravity Games
# ...          ...                                                                     ...                           ...          ...       ..                ...                  ..         ...                   ...  ...       ...                                                                                                      ...              ...                                                       ...   ... ..                                                               ...  ...                 ...
# 1195722  62360           Windscreen 3 x 6 x 1 Curved with 2 Circular Stud Holders in Bottom                     NaN         Plastic       47           Windscreens and Fuselage  47      Trans-Clear           FCFCFC  1.0       https://cdn.rebrickable.com/media/parts/elements/4523573.jpg                                             232327.0      8092-1  Luke's Landspeeder                                        2010  163               https://cdn.rebrickable.com/media/sets/8092-1.jpg  158       Star Wars
# 1195723  64567           Weapon Lightsaber Hilt with Bottom Ring                                                NaN         Plastic       27           Minifig Accessories       80      Metallic Silver       A5A9B4  2.0       https://cdn.rebrickable.com/media/parts/elements/4548731.jpg                                             232327.0      8092-1  Luke's Landspeeder                                        2010  163               https://cdn.rebrickable.com/media/sets/8092-1.jpg  158       Star Wars
# 1195724  75c21           Hose Rigid 3mm D. 21L / 16.8cm                                                         NaN         Plastic       30           Tubes and Hoses           71      Light Bluish Gray     A0A5A9  2.0       https://cdn.rebrickable.com/media/parts/elements/4567861.jpg                                             232327.0      8092-1  Luke's Landspeeder                                        2010  163               https://cdn.rebrickable.com/media/sets/8092-1.jpg  158       Star Wars
# 1195725  85080           Brick Round Corner 2 x 2 Macaroni with Stud Notch and Reinforced Underside [New Style] NaN         Plastic       20           Bricks Round and Cones    0       Black                 05131D  2.0       https://cdn.rebrickable.com/media/parts/elements/4164471.jpg                                             232327.0      8092-1  Luke's Landspeeder                                        2010  163               https://cdn.rebrickable.com/media/sets/8092-1.jpg  158       Star Wars
# 1195726  87087           Brick Special 1 x 1 with Stud on 1 Side                                                NaN         Plastic       5            Bricks Special            72      Dark Bluish Gray      6C6E68  6.0       https://cdn.rebrickable.com/media/parts/elements/4558955.jpg                                             232327.0      8092-1  Luke's Landspeeder                                        2010  163               https://cdn.rebrickable.com/media/sets/8092-1.jpg  158       Star Wars
#
# [1173531 rows x 19 columns]
#
# All sets in one column for each part
gr_prts = df.groupby(['part_num','name_part'],as_index=False).agg(set_cnt=('set_num','count'),set_num=('set_num',', '.join),set_name=('name_set',', '.join))

# print(gr_prts)
# What are the most used LEGO parts?
most_used = df.groupby(['part_num',
                        'name_part',
                        'name_cat',
                        'name_col',
                        'img_url_part'], as_index=False
                       )['quantity'].sum().merge(gr_prts[['part_num','name_part','set_cnt']],on=['part_num','name_part']
).sort_values(by='quantity',ascending=False).iloc[:,[0,1,2,3,5,6,4]]
# print(most_used.head(10))
#       part_num                                                         name_part       name_cat name_col  quantity  set_cnt                                                  img_url_part
# 13539  2780     Technic Pin with Friction Ridges Lengthwise and Center Slots      Technic Pins   Black    69433.0   4597     https://cdn.rebrickable.com/media/parts/elements/4121715.jpg
# 35608  43093    Technic Axle Pin with Friction Ridges Lengthwise                  Technic Pins   Blue     22680.0   2336     https://cdn.rebrickable.com/media/parts/elements/4206482.jpg
# 50436  6558     Technic Pin Long with Friction Ridges Lengthwise, 2 Center Slots  Technic Pins   Blue     20619.0   1479     https://cdn.rebrickable.com/media/parts/elements/4514553.jpg
# 46939  61332    Technic Pin with Friction Ridges Lengthwise with No Center Slots  Technic Pins   Black    19805.0   1097     https://cdn.rebrickable.com/media/parts/elements/6279875.jpg
# 17624  3023     Plate 1 x 2                                                       Plates         Black    17907.0   22662    https://cdn.rebrickable.com/media/parts/elements/302326.jpg
# 17856  3024     Plate 1 x 1                                                       Plates         White    16228.0   17467    https://cdn.rebrickable.com/media/parts/elements/302401.jpg
# 15107  3004     Brick 1 x 2                                                       Bricks         White    16223.0   14708    https://cdn.rebrickable.com/media/parts/elements/300401.jpg
# 24162  32062    Technic Axle 2 Notched                                            Technic Axles  Red      15153.0   2946     https://cdn.rebrickable.com/media/parts/elements/4142865.jpg
# 17700  3023     Plate 1 x 2                                                       Plates         White    14373.0   22662    https://cdn.rebrickable.com/media/parts/elements/302301.jpg
# 15369  3005     Brick 1 x 1                                                       Bricks         White    12892.0   10672    https://cdn.rebrickable.com/media/parts/elements/300501.jpg



# What parts are in the most number of sets?
most_number_of_sets = most_used.sort_values('set_cnt',ascending=False)

# print(most_number_of_sets.head(10))
#       part_num                          name_part                        name_cat         name_col  quantity  set_cnt                                                  img_url_part
# 47092  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  White            10028.0   28402    https://cdn.rebrickable.com/media/parts/elements/614101.jpg
# 47075  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Sand Green       143.0     28402    https://cdn.rebrickable.com/media/parts/elements/6403175.jpg
# 47082  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Trans-Green      1747.0    28402    https://cdn.rebrickable.com/media/parts/elements/3005748.jpg
# 47080  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Trans-Dark Blue  1689.0    28402    https://cdn.rebrickable.com/media/parts/elements/3005743.jpg
# 47058  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Magenta          103.0     28402    https://cdn.rebrickable.com/media/parts/elements/6248970.jpg
# 47081  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Trans-Dark Pink  911.0     28402    https://cdn.rebrickable.com/media/parts/elements/4599535.jpg
# 47067  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Orange           1581.0    28402    https://cdn.rebrickable.com/media/parts/elements/4157103.jpg
# 47094  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Yellowish Green  171.0     28402    https://cdn.rebrickable.com/media/parts/elements/6057898.jpg
# 47063  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Metallic Silver  938.0     28402    https://cdn.rebrickable.com/media/parts/elements/4249039.jpg
# 47072  6141     Plate Round 1 x 1 with Solid Stud  Plates Round Curved and Dishes  Red              4995.0    28402    https://cdn.rebrickable.com/media/parts/elements/614121.jpg





