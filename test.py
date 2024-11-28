import requests

# Paths to the documents on the developer's system
doc1_path = '/home/jalvin/Downloads/Document1_AI.docx'
doc2_path = '/home/jalvin/Downloads/Drops/indexsubtitle.txt'

# Base URL for your API
base_url = 'http://172.17.0.2:5000'

# API endpoint for plagiarism checking
url = f'{base_url}/check_plagiarism'

# Open the files in binary mode and send them as part of the POST request
with open(doc1_path, 'rb') as doc1, open(doc2_path, 'rb') as doc2:
    files = {
        'doc1': doc1,
        'doc2': doc2
    }
    response = requests.post(url, files=files)

# Output the API response
response_data = response.json()
print(response_data)

# Obtain the relative heatmap URL from response
relative_heatmap_url = response_data.get('heatmap_url')
if relative_heatmap_url:
    # Construct the full heatmap URL
    full_heatmap_url = f'{base_url}{relative_heatmap_url}'
    # Send a GET request to download the heatmap image
    heatmap_response = requests.get(full_heatmap_url, stream=True)
    heatmap_response.raise_for_status()  # Ensure successful download status
    
    # Save the image locally
    heatmap_path = '/home/jalvin/Downloads/Drops/heatmap.png'
    with open(heatmap_path, 'wb') as f:
        for chunk in heatmap_response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'Heatmap downloaded to: {heatmap_path}')
else:
    print("No heatmap URL found in the response.")