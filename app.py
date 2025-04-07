from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# Initial list of videos (title, embed ID, description)
videos = [
    {
        'id': 'zmkWsFg4WlA',
        'title': 'Azure Web Application Firewall (WAF) Tutorial',
        'description': 'Learn how to set up and configure Azure Web Application Firewall.'
    },
    {
        'id': 'dQw4w9WgXcQ',
        'title': 'Sample Video',
        'description': 'This is a sample video to demonstrate the functionality.'
    }
]

def extract_video_id(url):
    """
    Extract the YouTube video ID from various YouTube URL formats
    """
    # Regular expression patterns for different YouTube URL formats
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    match = re.match(youtube_regex, url)
    if match:
        return match.group(6)
    
    # Check if the input is already a video ID (11 characters)
    if re.match(r'^[A-Za-z0-9_-]{11}$', url):
        return url
    
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    global videos
    error = None
    
    if request.method == 'POST':
        video_url = request.form.get('video_url', '')
        video_title = request.form.get('video_title', 'Untitled Video')
        video_description = request.form.get('video_description', 'No description provided.')
        
        # Extract the video ID from the URL
        video_id = extract_video_id(video_url)
        
        if video_id:
            # Check if video already exists
            if not any(video['id'] == video_id for video in videos):
                videos.append({
                    'id': video_id,
                    'title': video_title,
                    'description': video_description
                })
            else:
                error = "This video is already in the list."
        else:
            error = "Invalid YouTube URL or ID. Please try again."
    
    return render_template('index.html', videos=videos, error=error)

@app.route('/remove/<video_id>')
def remove_video(video_id):
    global videos
    videos = [video for video in videos if video['id'] != video_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
