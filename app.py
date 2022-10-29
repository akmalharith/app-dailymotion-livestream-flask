from flask import Flask, request, redirect, abort
import requests

app = Flask(__name__)

DEFAULT_PORT = 5512
DM_METADATA_BASE_URL = "https://www.dailymotion.com/player/metadata/video"
DM_EMBEDDER_MEDIAPRIMA = "https://www.tonton.com.my"

@app.route('/mediaprima')
def mediaprima():
    """
    To access a channel, go to http://<local_ip>:<port_no>/mediaprima?channel_metadata=<channel_metadata>
    """
    channel_metadata = request.args.get("channel_metadata")

    if not channel_metadata:
        abort(400)

    metadata_url = f"{DM_METADATA_BASE_URL}/{channel_metadata}"
    params = {"embedder": DM_EMBEDDER_MEDIAPRIMA}

    try:
        base_response = requests.get(metadata_url, params=params)
    except Exception as e:
        abort(400)

    try:
        base_url = base_response.json()
        [stream] = base_url["qualities"]["auto"]

    except KeyError:
        abort(400)

    else:
        return redirect(stream["url"], 302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=DEFAULT_PORT)
