import bencodepy as ben
import hashlib as hash
import requests
import socket

def decode_bencode(bencoded_value):
    
    try:
        return ben.Bencode(encoding="utf-8").decode(bencoded_value)
    except Exception as e:
        return ben.decode(bencoded_value)

def get_torrent_info(file_path):
    
    with open(file_path, "rb") as file:
        torrent_data = file.read()
        parsed = decode_bencode(torrent_data)
        tracker_url = parsed[b"announce"].decode("utf-8")
        info = parsed[b"info"]
        length = info[b"length"]
        
        # Bencode the info dictionary
        bencoded_info = ben.encode(info)
        
        # Calculate the SHA-1 hash of the bencoded info dictionary
        info_hash = hash.sha1(bencoded_info).digest()
        
        return tracker_url, info_hash, length
    
def get_peers(tracker_url, info_hash, length): #make get request
    
    # Print the info hash 
    print(f"Info Hash (raw): {info_hash}")

    # URL to encode the info hash
    encoded_info_hash = info_hash.hex()
    print(f"Encoded Info Hash: {encoded_info_hash}")

    # Generate a random peer ID 
    peer_id = b'-PC0001-' + hash.md5().digest()[0:12]

    # parameters for the GET request
    params = {
        'info_hash': info_hash,
        'peer_id': peer_id,
        'port': 6881,
        'uploaded': 0,
        'downloaded': 0,
        'left': length,
        'compact': 1,
        'event': 'started'
    }

    # Send GET request to the tracker
    response = requests.get(tracker_url, params=params, timeout=10)
        

    # Decode tracker response
    try:
        decoded_response = decode_bencode(response.content)
    except Exception as e:
        print(f"Error decoding response from tracker: {e}")
        return []

    # Check if the response contains 'peers' or not?
    if b"peers" not in decoded_response:
        print("No peers found in tracker response.")
        return []

    raw_peers = decoded_response[b"peers"]

    # Determine if the peers list is in compact format
    peer_list = []

    if isinstance(raw_peers, bytes):
        
        print("Tracker returned peers in compact format.") #decode as 6-byte chunks
        for i in range(0, len(raw_peers), 6):
            ip = socket.inet_ntoa(raw_peers[i:i + 4])
            port = int.from_bytes(raw_peers[i + 4:i + 6], byteorder='big')
            peer_list.append(f"{ip}:{port}")
    elif isinstance(raw_peers, list):
        # if Not in compact format then decode each peer dictionary
        def decode_string(data):
            return data.decode('utf-8') if isinstance(data, bytes) else data
        
        for peer_dict in raw_peers:
            if isinstance(peer_dict, dict): #each pair informations print
                peer_info = {decode_string(k): decode_string(v) for k, v in peer_dict.items()}
                ip = peer_info.get('ip', '')
                port = peer_info.get('port', '')
                peer_list.append(f"{ip}:{port}")

    print(f"Found peers: {peer_list}")
    return peer_list

def main(file_path):
    
    tracker_url, info_hash,length = get_torrent_info(file_path)
    peers = get_peers(tracker_url, info_hash,length)
    for peer in peers:
        print(peer)

if __name__ == "__main__":
    file_path = "sample.torrent" 
    main(file_path)