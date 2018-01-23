# -*- coding: utf-8 -*-
import os
import collections
import logging
import os
from copy import copy

import soundcloud

from flask import Flask
from flask_ask import Ask, question, statement, audio, current_stream, logger, session

from queue_manager import QueueManager
from ssml_builder import SSML

## Soundcloud Setup
sc_client_id = "8c63b5c6be310a43a0695f442b90d53d"
sc_client = soundcloud.Client(client_id=sc_client_id)
sc_my_user_id = os.environ.get("AS_USER_ID") or 14530021

sc_access_token = os.environ.get("AS_ACCESS_TOKEN")


## Flask-Ask Setup    
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.INFO)

queue = QueueManager([])

def getStreamUrl(_id):
    '''return stream url for the given id'''
    return "https://api.soundcloud.com/tracks/{_id}/stream?client_id={sc_client_id}".format(_id=_id, sc_client_id=sc_client_id)


@ask.launch
def launch():
    text = SSML().interjection("hey").sentence("Was willst du hören?")
    prompt = 'Du kannst sagen: Spiele meine Lieblingslieder'
    return question(str(text)).reprompt(prompt)


@ask.intent('FavoritesIntent')
def start_playlist():
    speech = SSML().interjection("jo")
    data = sc_client.get('/users/'+str(sc_my_user_id)+'/favorites')
    playlist = [t.fields() for t in data]
    for track in playlist:
        queue.add(track['id'])
    track_id = queue.start()
    stream_url = getStreamUrl(track_id)
    session.attributes["current_track"] = playlist[0]
    session.attributes["data"] = queue.export()
    return audio(str(speech)).play(stream_url)


# QueueManager object is not stepped forward here.
# This allows for Next Intents and on_playback_finished requests to trigger the step
@ask.on_playback_nearly_finished()
def nearly_finished():
    if session.attributes.get("data"):
        queue.load(session.attributes.get("data"))
    if queue.up_next:
        _infodump('Alexa is now ready for a Next or Previous Intent')
        # dump_stream_info()
        next_id = queue.up_next
        #_infodump('Enqueueing {}'.format(getStreamUrl(next_id)))
        return audio().enqueue(getStreamUrl(next_id))
    else:
        pass #_infodump('Nearly finished with last song in playlist')


@ask.on_playback_finished()
def play_back_finished():
    if session.attributes.get("data"):
        queue.load(session.attributes.get("data"))
    if queue.up_next:
        queue.step()
        session.attributes["data"] = queue.export()
        #_infodump('stepped queue forward')
        #dump_stream_info()
    else:
        return statement('You have reached the end of the playlist!')


# NextIntent steps queue forward and clears enqueued streams that were already sent to Alexa
# next_stream will match queue.up_next and enqueue Alexa with the correct subsequent stream.
@ask.intent('AMAZON.NextIntent')
def next_song():
    if session.attributes.get("data"):
        queue.load(session.attributes.get("data"))
    if queue.up_next:
        speech = 'playing next queued song'
        next_stream = getStreamUrl(queue.step())
        #_infodump('Stepped queue forward to {}'.format(next_stream))
        #dump_stream_info()
        session.attributes["data"] = queue.export()
        return audio(speech).play(next_stream)
    else:
        return audio('There are no more songs in the queue')


@ask.intent('AMAZON.PreviousIntent')
def previous_song():
    if session.attributes.get("data"):
        queue.load(session.attributes.get("data"))
    if queue.previous:
        speech = 'playing previously played song'
        prev_stream = getStreamUrl(queue.step_back())
        session.attributes["data"] = queue.export()
        return audio(speech).play(prev_stream)

    else:
        return audio('There are no songs in your playlist history.')


@ask.intent('AMAZON.StartOverIntent')
def restart_track():
    if session.attributes.get("data"):
        queue.load(session.attributes.get("data"))
    if queue.current:
        speech = 'Restarting current track'
        #dump_stream_info()
        return audio(speech).play(queue.current, offset=0)
    else:
        return statement('There is no current song')


@ask.on_playback_started()
def started(offset, token, url):
    #_infodump('Started audio stream for track {}'.format(queue.current_position))
    #dump_stream_info()
    pass

@ask.on_playback_stopped()
def stopped(offset, token):
    pass
    #_infodump('Stopped audio stream for track {}'.format(queue.current_position))


@ask.intent('AMAZON.PauseIntent')
def pause():
    #if session.attributes.get("data"):
    #    queue.load(session.attributes.get("data"))
    #seconds = current_stream.offsetInMilliseconds / 1000
    #msg = 'Paused the Playlist on track {}, offset at {} seconds'.format(
    #    queue.current_position, seconds)
    #_infodump(msg)
    #dump_stream_info()
    return audio('psst').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    #if session.attributes.get("data"):
    #    queue.load(session.attributes.get("data"))
    #seconds = current_stream.offsetInMilliseconds / 1000
    #msg = 'Resuming the Playlist on track {}, offset at {} seconds'.format(queue.current_position, seconds)
    #_infodump(msg)
    #dump_stream_info()
    return audio('').resume()


@ask.session_ended
def session_ended():
    return "{}", 200


def dump_stream_info():
    pass


def _infodump(obj, indent=2):
    msg = json.dumps(obj, indent=indent)
    logger.info(msg)


def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)


if __name__ == '__main__':
    #if 'ASK_VERIFY_REQUESTS' in os.environ:
    #    verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
    #    if verify == 'false':
    #        app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)