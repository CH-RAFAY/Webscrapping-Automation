# Hotel Data Scraper & Visualization System

## Project Overview
An automated web scraping and visualization system that collects hotel data from booking platforms (like Booking.com) and presents it in an interactive knowledge graph. The system extracts key information including prices, ratings, amenities, and locations, then visualizes the relationships in an intuitive hierarchical structure.

![S1](https://github.com/user-attachments/assets/2b63cde2-8865-4921-9768-850928b2a9d4)

## Features
- **Automated Data Collection**: Scrapes hotel data including prices, ratings, stars, and locations
- **Interactive Visualization**: Creates dynamic knowledge graphs with zoom/pan functionality
- **Data Processing**: Cleans and structures raw scraped data for analysis
- **Multiple Output Formats**: Generates CSV files, HTML visualizations, and price distribution charts
- **User-Friendly Interface**: Simple controls for exploring the data relationships


![S2](https://github.com/user-attachments/assets/d21660bd-d858-4fca-b75e-1101b6865e21)



## Technology Stack
| Component          | Technology Used               |
|--------------------|-------------------------------|
| Web Scraping       | Playwright, BeautifulSoup     |
| Data Processing    | Pandas, NumPy                 |
| Visualization      | D3.js, Matplotlib             |
| Automation         | Python Async/Await            |
| Data Storage       | CSV, JSON                     |

![S3](https://github.com/user-attachments/assets/66914d95-c850-416d-919f-21d044779613)

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
