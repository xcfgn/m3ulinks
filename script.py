import requests
from bs4 import BeautifulSoup

# URLs
source_url = "https://qatarstreams.vip/channel.php"
m3u_template = "https://faptok.site/streamcast/stream.m3u8?id={}"
output_file = "channels.m3u"

# Function to fetch and parse HTML
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch {url}. Status code: {response.status_code}")

# Function to extract channel names and IDs
def extract_channels(html):
    soup = BeautifulSoup(html, "html.parser")
    channels = []

    # Locate all links in the page
    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Check if the link contains the ID (e.g., "watch.php?watch=")
        if "watch.php?watch=" in href:
            # Extract the channel ID and name
            channel_id = href.split("watch=")[1]
            channel_name = link.text.strip()  # Visible channel name
            if channel_name:  # Only include if a name exists
                channels.append((channel_name, channel_id))

    return channels

# Function to generate M3U content
def generate_m3u(channels):
    m3u_content = "#EXTM3U\n"
    for name, channel_id in channels:
        m3u_content += f"#EXTINF:-1,{name}\n{m3u_template.format(channel_id)}\n"
    return m3u_content

# Main Script
try:
    print("Fetching HTML content...")
    html_content = fetch_html(source_url)
    print("Extracting channels...")
    channel_data = extract_channels(html_content)

    print(f"Found {len(channel_data)} channels. Generating M3U file...")
    m3u_content = generate_m3u(channel_data)

    # Save to file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(m3u_content)

    print(f"Playlist saved to {output_file}. You can now use it with your media player!")
except Exception as e:
    print(f"Error: {e}")
