from riotwatcher import LolWatcher, ApiError
import pandas as pd
import matplotlib.pyplot as plt

# golbal variables
api_key = 'RGAPI-e519ffe0-0128-442c-a21f-85488ccc3a2a'
watcher = LolWatcher(api_key)
my_region = 'na1'

me = watcher.summoner.by_name(my_region, 'AresV1')
#print(me)

my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

# fetch last match detail
last_match = my_matches['matches'][0]
match_detail = watcher.match.by_id(my_region, last_match['gameId'])

participants = []
for row in match_detail['participants']:
    participants_row = {}
    participants_row['champion'] = row['championId']
    participants_row['spell1'] = row['spell1Id']
    participants_row['spell2'] = row['spell2Id']
    participants_row['win'] = row['stats']['win']
    participants_row['kills'] = row['stats']['kills']
    participants_row['deaths'] = row['stats']['deaths']
    participants_row['assists'] = row['stats']['assists']
    participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
    participants_row['goldEarned'] = row['stats']['goldEarned']
    participants_row['champLevel'] = row['stats']['champLevel']
    participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
    participants_row['item0'] = row['stats']['item0']
    participants_row['item1'] = row['stats']['item1']
    participants.append(participants_row)

#print(df)  


latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
static_item_list = watcher.data_dragon.items(latest, 'en_US')

#print(static_item_list)

# champ static list data to dict for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

for row in participants:
    print(str(row['champion']) + ' ' + champ_dict[str(row['champion'])])
    #print(str(row['item0']) + ' ' + champ_dict[str(row['item'])])
    row['championName'] = champ_dict[str(row['champion'])]


# item static list data to dict for looking up
item_dict = {}
for key in static_item_list['data']:
    row = static_item_list['data'][key]
    item_dict[row['key']] = row['name']
for row in participants:
    print(str(row['item0']) + ' ' + champ_dict[str(row['item'])])
    row['item0C'] = champ_dict[str(row['item0'])]
 
df = pd.DataFrame(participants)

#print df in pyplot/MathPlotLib
fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
my_table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
my_table.auto_set_column_width(col=list(range(len(df.columns))))
my_table.auto_set_font_size(False)
my_table.set_fontsize(16)
fig.tight_layout()
plt.show()