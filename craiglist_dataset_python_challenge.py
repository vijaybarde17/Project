import pandas as pd
import matplotlib.pyplot as plt
import unittest

# Load the dataset
data = pd.read_csv('/Users/vijaybarde/Downloads/craigslist_vehicles.csv')

# Convert 'posting_date' column to datetime format
data['posting_date'] = pd.to_datetime(data['posting_date'])

# Aggregate data on a temporal basis
data_agg = data.groupby(['posting_date', 'region', 'type']).size().reset_index(name='count')

# Interactive time-series chart
def plot_time_series(data_agg, region, type):
    subset = data_agg[(data_agg['region'] == region) & (data_agg['type'] == type)]
    plt.figure(figsize=(10, 6))
    plt.plot(subset['posting_date'], subset['count'])
    plt.title(f'Time-Series of Available Vehicles in {region} - {type}')
    plt.xlabel('Posting Date')
    plt.ylabel('Number of Vehicles')
    plt.grid(True)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Force y-axis ticks to display integer values
    plt.yticks(subset['count'].astype(int))
    plt.show()  # Display the plot
    return plt  # Return the plt object

# Function to generate plot without displaying it
def generate_test_plot():
    return plot_time_series(data_agg, 'austin', 'SUV')

class TestTimeSeriesPlot(unittest.TestCase):

    def setUp(self):
        # Example dataset
        self.example_data = pd.DataFrame({
            'posting_date': ['2022-01-01', '2022-01-02', '2022-01-03'],
            'region': ['austin', 'atlanta', 'athens'],
            'type': ['SUV', 'sedan', 'pickup'],
            'count': [10, 15, 12]
        })

    def test_time_series_plot(self):
        # Call the function to generate the test plot
        plot = generate_test_plot()
        
        # Assert that the plot is not empty
        self.assertIsNotNone(plot)

        # Assert that the plot title is set correctly
        self.assertEqual(plot.get_axes()[0].get_title(), 'Time-Series of Available Vehicles in austin - SUV')

        # Assert that the x-axis label is set correctly
        self.assertEqual(plot.get_axes()[0].get_xlabel(), 'Posting Date')

        # Assert that the y-axis label is set correctly
        self.assertEqual(plot.get_axes()[0].get_ylabel(), 'Number of Vehicles')

        # Assert that the grid is enabled
        self.assertTrue(plot.get_axes()[0].get_xaxis().get_gridlines()[0].get_visible())
        self.assertTrue(plot.get_axes()[0].get_yaxis().get_gridlines()[0].get_visible())

if __name__ == '__main__':
    unittest.main()
