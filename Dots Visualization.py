import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_restaurant_prices(file_path):
    """
    Visualize restaurant data based on price categories from a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file containing restaurant price data.
    """
    # Load the CSV file into a DataFrame
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return
    
    # Check for necessary columns
    if 'Price' not in data.columns:
        print("Error: CSV file must contain a 'Price' column.")
        return
    
    # Define price ranges and labels
    bins = [0, 999, 1999, 2999, 3999, 4999, 5999, 6999, 7999, 8999, 9999, float('inf')]
    labels = ["$0-999", "$1000-1999", "$2000-2999", "$3000-3999", "$4000-4999",
              "$5000-5999", "$6000-6999", "$7000-7999", "$8000-8999", "$9000-9999", "$10000+"]
    
    # Categorize the prices into bins
    data['Price Range'] = pd.cut(data['Price'], bins=bins, labels=labels, include_lowest=True)
    
    # Set up the color palette
    palette = sns.color_palette("Spectral", len(labels))
    
    # Plotting the scatter plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=data, x=data.index, y='Price', hue='Price Range', palette=palette, s=50, alpha=0.6)
    
    # Customizing the plot
    plt.title("Restaurant Price Visualization")
    plt.xlabel("Restaurant Index")
    plt.ylabel("Price")
    plt.legend(title="Price Range", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# Specify the file path here
file_path = 'Restaurant - Customers.csv'  # Replace with your actual file path

# Run the function with the specified file path
visualize_restaurant_prices(file_path)
