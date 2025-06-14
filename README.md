# Hotel Data Scraper & Visualization System

## Project Overview
An automated web scraping and visualization system that collects hotel data from booking platforms (like Booking.com) and presents it in an interactive knowledge graph. The system extracts key information including prices, ratings, amenities, and locations, then visualizes the relationships in an intuitive hierarchical structure.

## Features
- **Automated Data Collection**: Scrapes hotel data including prices, ratings, stars, and locations
- **Interactive Visualization**: Creates dynamic knowledge graphs with zoom/pan functionality
- **Data Processing**: Cleans and structures raw scraped data for analysis
- **Multiple Output Formats**: Generates CSV files, HTML visualizations, and price distribution charts
- **User-Friendly Interface**: Simple controls for exploring the data relationships

## Technology Stack
| Component          | Technology Used               |
|--------------------|-------------------------------|
| Web Scraping       | Playwright, BeautifulSoup     |
| Data Processing    | Pandas, NumPy                 |
| Visualization      | D3.js, Matplotlib             |
| Automation         | Python Async/Await            |
| Data Storage       | CSV, JSON                     |

## Installation

### Prerequisites
- Python 3.8+
- Chrome or Firefox browser
- Git (optional)

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/yourusername/HotelDataScraper.git
cd HotelDataScraper

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
