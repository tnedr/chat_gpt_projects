from pytrends.request import TrendReq
import sys
from anytree import Node, RenderTree


# Define a function to create a tree from the nested dictionary
def build_tree(node, data):
    for child in data.get('children', []):
        child_node = Node(child['name'], parent=node)
        build_tree(child_node, child)


def print_first_level_children(data, path=''):
    # If path is blank, show the top-level children
    if not path:
        for child in data['children']:
            print(child['name'])
    else:
        # Find the node corresponding to the given path
        path_elements = path.split('/')
        node = data
        for element in path_elements:
            node = [child for child in node['children'] if child['name'] == element][0]

        # Print the first-level children of the selected node
        for child in node['children']:
            print(child['name'])


def print_whole(d_cat):
    # Create the root node and build the tree
    root = Node('Root')
    build_tree(root, d_cat)

    # Print the tree
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")


# https://pypi.org/project/pytrends/4.9.2/



# ---------------- API Methods ----------------
# The following API methods are available:
# Interest Over Time: returns historical, indexed data for when the keyword was searched most as shown on Google Trends' Interest Over Time section.
# Multirange Interest Over Time: returns historical, indexed data similar to interest over time, but across multiple time date ranges.
# Historical Hourly Interest: returns historical, indexed, hourly data for when the keyword was searched most as shown on Google Trends' Interest Over Time section. It sends multiple requests to Google, each retrieving one week of hourly data. It seems like this would be the only way to get historical, hourly data.
# Interest by Region: returns data for where the keyword is most searched as shown on Google Trends' Interest by Region section.
# Related Topics: returns data for the related keywords to a provided keyword shown on Google Trends' Related Topics section.
# Related Queries: returns data for the related keywords to a provided keyword shown on Google Trends' Related Queries section.
# Trending Searches: returns data for latest trending searches shown on Google Trends' Trending Searches section.
# Top Charts: returns the data for a given topic shown in Google Trends' Top Charts section.
# Suggestions: returns a list of additional suggested keywords that can be used to refine a trend search.


# initialization
pytrends = TrendReq()
d_cat = pytrends.categories()

print_whole(d_cat)
# print_first_level_children(d_cat)
sys.exit()

['united_states', 'india', 'japan', 'singapore', 'israel', 'australia', 'hong_kong', 'taiwan', 'canada', 'germany', 'netherlands', 'indonesia', 'south_korea', 'turkey', 'philippines', 'italy', 'vietnam', 'egypt', 'argentina', 'poland', 'colombia', 'ukraine', 'saudi_arabia', 'kenya', 'chile', 'romania', 'south_africa', 'belgium', 'sweden', 'austria', 'switzerland', 'greece', 'denmark', 'norway', 'nigeria', 'new zealand', 'ireland', 'czech_republic', 'portugal', 'mexico', 'malaysia', 'hungary', 'russia', 'thailand', 'brazil', 'france', 'united_kingdom', 'finland']

# trending searches
print(pytrends.trending_searches(pn='united_states'))



kw_list = ['pizza', 'bagel']
timeframe=['2022-09-04 2022-09-10']

# pytrends.build_payload(kw_list=kw_list, timeframe='today 5-d')
# print(pytrends.interest_over_time())

print(pytrends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0))
print(pytrends.get_historical_interest([], year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0))
sys.exit()

pytrends.build_payload(kw_list, timeframe=['2022-09-04 2022-09-10', '2022-09-18 2022-09-24'])
df1 = pytrends.multirange_interest_over_time()
print(df1)

df2 = pytrends.trending_searches(pn='united_states') # trending searches in real time for United States
df3 = pytrends.trending_searches(pn='japan') # Japan
print(df2)
print(df3)

print(pytrends.top_charts(2020, hl='en-US', tz=300, geo='GLOBAL'))

# Set the time range to the desired date
pytrends.build_payload(kw_list=[], timeframe='today 5-d', geo='hu')

# Get the top 20 searches
top_searches = pytrends.top_charts(20, cid='entity-HU')

# Print the top 20 searches
print(top_searches)
