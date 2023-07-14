# SpotifyPlaylistGenerator

# AI Playlist Generator

This application uses the OpenAI API to generate a playlist based on a given prompt, and then uses the Spotify API to create this playlist for the user.

## Setup

1. Clone the repository: `git clone https://github.com/yourusername/yourrepository.git`
2. Navigate to the project directory: `cd yourrepository`
3. Install the required dependencies: `pip install -r requirements.txt`

4. You will need developer accounts for both [OpenAI](https://beta.openai.com/signup/) and [Spotify](https://developer.spotify.com/dashboard/).

5. Once you have the accounts, create a `.env` file in the root directory of the project and fill it with your OpenAI API key, Spotify Client ID, and Spotify Client Secret:

```shell
OPENAI_API_KEY=openai_api_key_goes_here
SPOTIFY_CLIENT_ID=spotify_client_id_goes_here
SPOTIFY_CLIENT_SECRET=spotify_client_secret_goes_here
```

Replace openai_api_key_goes_here, spotify_client_id_goes_here, and spotify_client_secret_goes_here with your actual keys.

## Usage

The application can be used with command line arguments:

-p is the prompt describing the playlist. For example, -p "fun songs".
-n is the number of songs to be added to the playlist. For example, -n 10.

For example:

```shell
python app.py -p "songs that are really fun" -n 10
```
