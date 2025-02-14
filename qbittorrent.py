import qbittorrentapi
import json
from datetime import datetime

def check_active_downloads():
    # Initialize qBittorrent client
    qbt_client = qbittorrentapi.Client(
        host='localhost',
        port=8085,
        username='admin',
        password='adminadmin'
    )

    try:
        # Connect to qBittorrent
        qbt_client.auth_log_in()
        
        # Get list of all torrents
        torrents = qbt_client.torrents_info()
        
        # Filter for torrents that aren't completed (progress < 100%)
        downloading_torrents = []
        for torrent in torrents:
            if torrent.progress < 1.0:  # progress is between 0 and 1
                torrent_info = {
                    'name': torrent.name,
                    'state': torrent.state,
                    'progress': f"{torrent.progress * 100:.2f}%",
                    'size': f"{torrent.size / (1024*1024*1024):.2f} GB",
                    'download_speed': f"{torrent.dlspeed / (1024*1024):.2f} MB/s",
                    'eta': torrent.eta // 60  # Convert seconds to minutes
                }
                downloading_torrents.append(torrent_info)
        
        # Create output data with timestamp
        output_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'active_downloads': downloading_torrents
        }
        
        # Save to file
        filename = 'active_downloads.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully saved {len(downloading_torrents)} active downloads to {filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        
    finally:
        # Logout
        qbt_client.auth_log_out()

if __name__ == "__main__":
    check_active_downloads()