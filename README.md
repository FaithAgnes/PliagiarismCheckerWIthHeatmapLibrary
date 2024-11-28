# PliagiarismCheckerWIthHeatmap

## Overview

This application checks plagiarism between two documents and visualizes the results as a heatmap.

## Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.

### Clone Repository

```bash
git clone https://github.com/FaithAgnes/PliagiarismCheckerWIthHeatmapLibrary.git
```
### Build Docker Image

```bash
docker run -v /path/to/documents:/app/documents -v /path/to/output:/app/output -p 5000:5000 plagiarismvisualizer1.0
```
> Remember to replace the file paths

## Running the Application 

###Run the Docker container:

```bash
docker run -v /path/to/documents:/app/documents -v /path/to/output:/app/output -p 5000:5000 plagiarismvisualizer1.0
```
> Remember to replace the file paths

#### Access the API at http://localhost:5000

## Usage
#### Send a POST request to **/check_plagiarism** with document files to retrieve the plagiarism score and heatmap URL.

### Downloading Heatmap

#### Use the heatmap URL from the response to download the image.

> Or you could also directly use /download_heatmap

## Example Requests

### Using Python requests library for testing

```python
import requests

# Document paths
doc1_path = '/path/to/your/Document1.docx'
doc2_path = '/path/to/your/Document2.txt'

# API endpoint
url = 'http://localhost:5000/check_plagiarism'

# Open and send files
with open(doc1_path, 'rb') as doc1, open(doc2_path, 'rb') as doc2:
    files = {
        'doc1': doc1,
        'doc2': doc2
    }
    response = requests.post(url, files=files)
    response_data = response.json()
    print(response_data)

# Download heatmap if available
heatmap_url = response_data.get('heatmap_url')
if heatmap_url:
    heatmap_response = requests.get('http://localhost:5000' + heatmap_url, stream=True)
    with open('/path/to/save/heatmap.png', 'wb') as f:
        for chunk in heatmap_response.iter_content(chunk_size=8192):
            f.write(chunk)
    print('Heatmap downloaded successfully.')
```

### Recommendations:
- **Remember to replace placeholder parts** (like URLs and paths) with your actual project settings.
- **Ensure all URLs are accurate**, especially if hosting the project somewhere remote (e.g., on GitHub).
- **Extend sections** as needed to include team contacts or advanced usage scenarios as your application evolves.

