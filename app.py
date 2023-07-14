# Import the required libraries
import openai
from dotenv import dotenv_values
import json
import spotipy 
import argparse

# Load the environment variables from the .env file
config = dotenv_values(".env")

# Set the OpenAI API key
openai.api_key = config["OPENAI_API_KEY"]

# Setup the command line argument parser
parser = argparse.ArgumentParser(description="Simple command line song utility")
parser.add_argument("-p", type=str, default= "fun songs", help="The prompt to describe the playlist")
parser.add_argument("-n",type=int, default=10, help="The number of songs to add to playlist")
args = parser.parse_args()

# Setup the Spotify API client
sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id= config["SPOTIFY_CLIENT_ID"],
        client_secret= config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:9999",
        scope= "playlist-modify-private"
    )
)

# This function queries the OpenAI API to generate a playlist
def get_playlist(prompt="fun songs", count=10):
    # Example playlist for the assistant to follow
    example_json = """
    [
    {"song": "Hurt", "artist": "Johnny Cash"},
    {"song": "Someone Like You", "artist": "Adele"},
    {"song": "Tears in Heaven", "artist": "Eric Clapton"},
    {"song": "My Immortal", "artist": "Evanescence"},
    {"song": "Nothing Compares 2 U", "artist": "Sinead O'Connor"},
    {"song": "Say Something", "artist": "A Great Big World ft. Christina Aguilera"},
    {"song": "Yesterday", "artist": "The Beatles"},
    {"song": "Welcome to the Black Parade", "artist": "My Chemical Romance"},
    {"song": "All by Myself", "artist": "Celine Dion"},
    {"song": "Everybody Hurts", "artist": "R.E.M."}
    ]
    """
    messages = [
        {"role": "system", "content": """You are a helpful playlist generating assistant.
        You should generate a list of songs and their artists according to a text prompt.
        You should only return a JSON array, where each element follows this format: {"song": <song_title>, "artist": <artist_name>}"""
        },
        {"role": "user", "content": "Generate a playlist of 10 songs based on this prompt: super super sad songs"},
        {"role": "assistant", "content": example_json},
        {"role": "user", "content": f"Generate a playlist of {count} songs based on this prompt: {prompt}"}
    ]

    # Query the OpenAI API
    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=400
    )

    # Parse the response and return it
    playlist = json.loads(response["choices"][0]["message"]["content"])


    return playlist

# Get the playlist based on command line arguments
playlist = get_playlist(args.p, args.n)

# Print playlist to terminal
print(playlist)

# Get the current Spotify user
current_user = sp.current_user()

# Make sure we have a user
assert current_user is not None

# Find all the song IDs for the playlist
track_ids = []
for item in playlist:
    artist, song = item["artist"], item["song"]
    query = f"{song} {artist}"
    search_results = sp.search(q=query, type="track", limit=10)
    track_ids.append(search_results["tracks"]["items"][0]["id"])

# Create a new playlist with the found songs
created_playlist = sp.user_playlist_create(
    current_user["id"],
    public=False,
    name=args.p
)

# Add the songs to the new playlist
sp.user_playlist_add_tracks(current_user["id"], created_playlist["id"], track_ids )


