import pandas as pd
from collections import defaultdict

# Define the age, gender, activity level
age = 47
gender = 'male'
activity_level = 3
# Now use the slider to add more products
slider_value = 1  # Replace this with the actual slider value between 0 and 1



def load_data_into_dataframe():
    # data = {
    # 'Product': ['NAD+ Spark', 'NAD+ Shield', 'SirtuLife', 'Senophase', 'AGEFyt', 'Telogene', 'BoroZIne', 'CreaTaure', 'SynerGP', 'Radiance3X'],
    # 20: [0, 0, 0, 0, 0, 0, 0.5, 0.2, 0.2, 0],
    # 25: [0.1, 0.1, 0, 0, 0.3, 0, 0.6, 0.4, 0.3, 0.2],
    # 30: [0.3, 0.3, 0.1, 0.1, 0.5, 0.1, 0.7, 0.5, 0.5, 0.4],
    # 35: [0.5, 0.5, 0.2, 0.2, 0.7, 0.2, 0.8, 0.7, 0.6, 0.5],
    # 40: [0.7, 0.7, 0.4, 0.4, 0.9, 0.4, 0.9, 0.8, 0.8, 0.7],
    # 45: [0.8, 0.8, 0.6, 0.6, 1, 0.6, 1, 0.9, 0.9, 0.8],
    # 50: [1, 1, 0.8, 0.8, 1, 0.8, 1, 1, 1, 1],
    # 55: [1, 1, 0.9, 0.9, 1, 0.9, 1, 1, 1, 1],
    # 60: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # }
    # df = pd.DataFrame(data)
    # df.set_index('Product', inplace=True)
    df = pd.read_csv('age_matrix.csv', index_col=0)
    return df

# Example usage
age_matrix = load_data_into_dataframe()

# Define functional preferences of the user
functional_preferences = ['Energy Boosting', 'Muscle & Cognitive Performance', 'Skin Health & Repair']

# Define the product efficiency dictionary
product_efficiency = {
    'Inflammation Control': [(0.5, 'BoroZIne'), (0.7, 'SirtuLife'), (0.8, 'AGEFyt')],
    'Energy Boosting': [(0.9, 'NAD+ Spark'), (0.6, 'NAD+ Shield')],
    'DNA Integrity': [(0.8, 'SirtuLife'), (0.7, 'Telogene')],
    'Skin Health & Repair': [(0.9, 'Radiance3X'), (0.4, 'AGEFyt'), (0.6, 'NAD+ Shield')],
    'Muscle & Cognitive Performance': [(0.9, 'CreaTaure')],
    'Antioxidant & Detox Support': [(0.9, 'SynerGP'), (0.7, 'AGEFyt')],
    'Hormonal Balance': [(0.8, 'BoroZIne')],
    'Tissue Rejuvenation': [(0.8, 'Senophase'), (0.7, 'Radiance3X')]
}

# Calculate the recommended products
recommended_products = []

for functionality in functional_preferences:  # Loop through the functional preferences
    for efficiency, product in product_efficiency.get(functionality, []):  # Get the product list for each functionality
        age_col = (age//5) * 5
        if age_col > 60:
            age_col = 60
        # get age efficiency for the product from age_matrix
        age_efficiency = age_matrix.loc[product, str(age_col)]  # Get the age-specific efficiency from the matrix
        if age_efficiency > 0:  # If the age-specific efficiency is greater than 0
            weighted_efficiency = efficiency * age_efficiency  # Apply the age-specific value
            recommended_products.append((product, functionality, weighted_efficiency))  # Now a 3-element tuple  # Append to the recommended list

# Sort the recommended products based on their weighted efficiency
recommended_products.sort(reverse=True, key=lambda x: x[2])

# Initialize final list of products to recommend
final_recommendations = []

# Initialize a set to keep track of functionalities already covered
covered_functionalities = set()

# Always include the top product for each functionality
for functionality in functional_preferences:
    for product, func, weighted_efficiency in recommended_products:
        if func == functionality and func not in covered_functionalities:
            final_recommendations.append((product, func, weighted_efficiency))
            covered_functionalities.add(func)
            break

additional_products = len(recommended_products)-len(final_recommendations)
additional_products = int(additional_products * slider_value)

for product, func, weighted_efficiency in recommended_products:
    if additional_products <= 0:
        break
    if (product, func, weighted_efficiency) not in final_recommendations:
        final_recommendations.append((product, func, weighted_efficiency))
        additional_products -= 1

print(final_recommendations)

# Initialize a dictionary to hold products and their aggregated functionalities and weighted efficiencies
aggregated_products = defaultdict(list)

# Iterate through the final recommendations
for product, functionality, weighted_efficiency in final_recommendations:
    aggregated_products[product].append((functionality, weighted_efficiency))

# Generate a new list for final recommendations
new_final_recommendations = [(product, aggregated_functions) for product, aggregated_functions in aggregated_products.items()]

# Optionally sort by the first weighted efficiency of each product (you could choose another sorting method)
new_final_recommendations.sort(key=lambda x: x[1][0][1], reverse=True)

print(new_final_recommendations)