import json
import matplotlib.pyplot as plt
from collections import Counter

# Load JSON data
def load_metadata(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Visualization function for themes and formats using pie charts
def visualize_pie_chart(data, title):
    counter = Counter(data)
    labels = counter.keys()
    sizes = counter.values()
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# Special visualization for color distribution without labels and percentages
def visualize_color_distribution(colors):
    counter = Counter(colors)
    sizes = counter.values()
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, colors=colors, startangle=140)
    plt.title('Dominant Color Distribution in the Dataset')
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    metadata_filename = 'image_metadata.json'  # Update this path
    metadata = load_metadata(metadata_filename)

    # Visualize theme distribution
    themes = [entry['tags'] for entry in metadata if 'tags' in entry]
    visualize_pie_chart(themes, 'Theme Distribution in the Dataset')

    # Visualize format distribution
    formats = [entry['format'] for entry in metadata if 'format' in entry]
    visualize_pie_chart(formats, 'Format Distribution in the Dataset')

    # Visualize color distribution without labels and percentages
    colors = [entry['couleur_dominante'][1] for entry in metadata if 'couleur_dominante' in entry]
    visualize_color_distribution(colors)
