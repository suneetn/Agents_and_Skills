---
name: youtube
description: Search YouTube, extract video information, download transcripts/subtitles, and analyze video content. Supports video summarization, metadata extraction, and content research.
---

# YouTube Skill

This skill enables Claude to interact with YouTube videos, extract content, download transcripts, and perform video analysis using browser tools and optional command-line utilities.

## When to Use This Skill

Use this skill when:
- Searching for YouTube videos on specific topics
- Extracting video transcripts or subtitles
- Summarizing video content
- Analyzing video metadata (views, likes, comments, description)
- Researching YouTube channels or playlists
- Downloading video text content for analysis
- Comparing multiple videos on the same topic

## Core Capabilities

### 1. Video Search

Navigate to YouTube and search for videos:
1. Use `browser_navigate` to go to `https://www.youtube.com`
2. Use `browser_snapshot` to see the page structure
3. Find the search box and use `browser_type` to enter search terms
4. Use `browser_click` to submit the search
5. Use `browser_snapshot` to see search results

### 2. Extract Video Information

For any YouTube video URL, extract:
- **Title**: Video title
- **Channel**: Channel name and URL
- **Views**: View count
- **Likes/Dislikes**: Engagement metrics
- **Description**: Full video description
- **Comments**: Comment count and sample comments
- **Duration**: Video length
- **Upload Date**: When video was published
- **Tags**: Video tags (if visible)

**Process:**
1. Navigate to the video URL using `browser_navigate`
2. Use `browser_snapshot` to capture the page structure
3. Extract metadata from the accessibility snapshot
4. Use `browser_evaluate` to extract structured data if needed

### 3. Download Transcripts/Subtitles

**Method 1: Using Browser Tools (Primary)**

1. Navigate to the video page
2. Look for the "Show transcript" or "CC" button
3. Click to expand transcript
4. Extract transcript text from the page
5. Save to a file

**Method 2: Using yt-dlp (If Installed)**

If `yt-dlp` is installed, use command-line extraction:
```bash
# List available subtitles
yt-dlp --list-subs "VIDEO_URL"

# Download subtitles in preferred language
yt-dlp --write-subs --write-auto-subs --sub-lang en --skip-download "VIDEO_URL"

# Download subtitles as text file
yt-dlp --write-subs --write-auto-subs --sub-lang en --skip-download --convert-subs srt "VIDEO_URL"

# Extract transcript directly to text
yt-dlp --write-auto-subs --sub-lang en --skip-download --convert-subs txt "VIDEO_URL" -o "%(title)s.%(ext)s"
```

**Method 3: Using YouTube API (If Available)**

Extract transcript from YouTube's internal API:
```javascript
// Use browser_evaluate to access YouTube's internal transcript API
browser_evaluate({
  function: () => {
    // YouTube stores transcript data in window.__INITIAL_DATA__
    const data = window.__INITIAL_DATA__;
    // Extract transcript from data structure
    return data?.contents?.twoColumnWatchNextResults?.results?.results?.contents
      ?.find(c => c.videoSecondaryInfoRenderer)?.videoSecondaryInfoRenderer
      ?.attributedDescription?.content;
  }
});
```

### 4. Video Summarization

**Process:**
1. Extract transcript using methods above
2. Analyze transcript content
3. Identify key topics, main points, and conclusions
4. Create structured summary with:
   - Overview
   - Key Points (bulleted)
   - Main Takeaways
   - Timestamps for important sections (if available)

### 5. Channel Analysis

Extract channel information:
- Channel name and subscriber count
- Total videos
- Channel description
- Recent uploads
- Popular videos

**Process:**
1. Navigate to channel URL (e.g., `https://www.youtube.com/@channelname`)
2. Use `browser_snapshot` to capture channel page
3. Extract channel metadata
4. Navigate to "Videos" tab to see uploads
5. Extract video list and metadata

### 6. Playlist Analysis

Extract playlist information:
- Playlist title and description
- Video count
- List of videos with titles and URLs
- Total duration

**Process:**
1. Navigate to playlist URL
2. Extract playlist metadata
3. Scroll through playlist to load all videos
4. Extract video list

## Recommended Workflow (API-First Approach)

### Standard Video Analysis Workflow (Using APIs)

**Preferred Method:**
```markdown
1. Extract video ID from URL
   → Parse "https://www.youtube.com/watch?v=VIDEO_ID"

2. Get metadata via YouTube Data API v3
   → curl or Python requests to API

3. Get transcript via youtube-transcript-api
   → Python: YouTubeTranscriptApi.get_transcript(video_id)

4. Save metadata and transcript
   → write() to organized directories

5. Analyze and summarize
   → Process transcript content
```

**Fallback Method (Browser):**
Only use browser tools if:
- API keys not available
- Transcript not available via API
- Need to interact with YouTube UI

### Browser Tool Workflow (Fallback)

```markdown
1. Navigate to video URL
   → browser_navigate("https://www.youtube.com/watch?v=VIDEO_ID")

2. Capture page snapshot
   → browser_snapshot()

3. Extract video metadata
   → Look for title, channel, views, description in snapshot

4. Find and click transcript button
   → browser_click(element="Show transcript button", ref="...")

5. Extract transcript text
   → browser_snapshot() or browser_evaluate()

6. Save transcript to file
   → write(file_path="...", contents=transcript)

7. Analyze and summarize
   → Process transcript content
```

### Search and Extract Workflow

```markdown
1. Navigate to YouTube
   → browser_navigate("https://www.youtube.com")

2. Search for topic
   → browser_type(element="Search box", ref="...", text="search query")
   → browser_press_key(key="Enter")

3. Wait for results
   → browser_wait_for(text="results")

4. Capture search results
   → browser_snapshot()

5. Extract video URLs and titles
   → Parse from snapshot

6. For each video:
   → Navigate and extract information
   → Download transcript if needed
```

## API-Based Methods (Recommended)

**Why use APIs instead of browser automation:**
- ✅ Faster and more reliable
- ✅ No browser overhead
- ✅ Better for batch processing
- ✅ More structured data
- ✅ Rate limits are manageable

### Method 1: YouTube Data API v3 (Official)

**Setup:**
1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Use API key in requests

**Extract Video Metadata:**

```bash
# Get video details
curl "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=VIDEO_ID&key=YOUR_API_KEY"

# Get video in JSON format
curl "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=VIDEO_ID&key=YOUR_API_KEY" | jq '.'
```

**Python Example:**
```python
import requests
import json

API_KEY = "YOUR_API_KEY"
VIDEO_ID = "OdtGN27LchE"

url = f"https://www.googleapis.com/youtube/v3/videos"
params = {
    "part": "snippet,statistics,contentDetails",
    "id": VIDEO_ID,
    "key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

video = data["items"][0]
metadata = {
    "title": video["snippet"]["title"],
    "channel": video["snippet"]["channelTitle"],
    "description": video["snippet"]["description"],
    "views": video["statistics"]["viewCount"],
    "likes": video["statistics"].get("likeCount", "N/A"),
    "duration": video["contentDetails"]["duration"],
    "publishedAt": video["snippet"]["publishedAt"]
}

print(json.dumps(metadata, indent=2))
```

**Note:** YouTube Data API v3 does NOT provide transcripts. Use Method 2 or 3 for transcripts.

### Method 2: youtube-transcript-api (Python)

**Install:**
```bash
pip install youtube-transcript-api
```

**Extract Transcript:**

```python
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "OdtGN27LchE"

try:
    # Get transcript
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Format transcript
    transcript_text = "\n".join([
        f"[{entry['start']:.1f}s] {entry['text']}"
        for entry in transcript_list
    ])
    
    # Save to file
    with open(f"{video_id}_transcript.txt", "w") as f:
        f.write(transcript_text)
    
    print("Transcript saved!")
except Exception as e:
    print(f"Error: {e}")
```

**Get Transcript as JSON:**
```python
from youtube_transcript_api import YouTubeTranscriptApi
import json

video_id = "OdtGN27LchE"
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Save as JSON
with open(f"{video_id}_transcript.json", "w") as f:
    json.dump(transcript, f, indent=2)
```

### Method 3: Combined Approach (Metadata + Transcript)

**Complete Python Script:**

```python
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import json
from datetime import datetime

def extract_youtube_video(video_id, api_key=None):
    """Extract complete video information using APIs"""
    
    result = {
        "videoId": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "extractedAt": datetime.now().isoformat()
    }
    
    # Get metadata from YouTube Data API
    if api_key:
        try:
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                "part": "snippet,statistics,contentDetails",
                "id": video_id,
                "key": api_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get("items"):
                video = data["items"][0]
                result["metadata"] = {
                    "title": video["snippet"]["title"],
                    "channel": video["snippet"]["channelTitle"],
                    "description": video["snippet"]["description"],
                    "views": video["statistics"]["viewCount"],
                    "likes": video["statistics"].get("likeCount", "N/A"),
                    "duration": video["contentDetails"]["duration"],
                    "publishedAt": video["snippet"]["publishedAt"],
                    "tags": video["snippet"].get("tags", [])
                }
        except Exception as e:
            result["metadataError"] = str(e)
    
    # Get transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        result["transcript"] = transcript
        result["transcriptText"] = "\n".join([
            entry["text"] for entry in transcript
        ])
    except Exception as e:
        result["transcriptError"] = str(e)
    
    return result

# Usage
video_id = "OdtGN27LchE"
api_key = "YOUR_API_KEY"  # Optional

result = extract_youtube_video(video_id, api_key)

# Save results
with open(f"{video_id}_complete.json", "w") as f:
    json.dump(result, f, indent=2)

print("Extraction complete!")
```

### Method 4: Third-Party APIs

**Scrappey YouTube Transcript API:**
```bash
curl "https://api.scrappey.com/api/v1?key=YOUR_API_KEY" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "type": "youtube-transcript"
  }'
```

**YouTube-Transcript.io API:**
```bash
curl "https://api.youtube-transcript.io/api/v1/transcript?videoId=VIDEO_ID" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### Method 5: Node.js Implementation

**Install:**
```bash
npm install youtube-transcript
```

**Usage:**
```javascript
const { YoutubeTranscript } = require('youtube-transcript');

YoutubeTranscript.fetchTranscript('VIDEO_ID')
  .then(transcript => {
    console.log(transcript);
    // Save to file
    const fs = require('fs');
    fs.writeFileSync('transcript.json', JSON.stringify(transcript, null, 2));
  })
  .catch(err => console.error(err));
```

## Command-Line Utilities (Alternative)

### Installing yt-dlp

```bash
# macOS
brew install yt-dlp

# Verify installation
yt-dlp --version
```

### yt-dlp Commands (API-like Interface)

```bash
# Get video info as JSON
yt-dlp --dump-json "VIDEO_URL" > video_info.json

# Download video metadata only
yt-dlp --write-info-json --skip-download "VIDEO_URL"

# Download subtitles in multiple languages
yt-dlp --write-subs --write-auto-subs --sub-lang en,es,fr --skip-download "VIDEO_URL"

# Extract transcript to text file
yt-dlp --write-auto-subs --sub-lang en --skip-download --convert-subs txt "VIDEO_URL" -o "%(title)s_transcript.txt"

# Download video description
yt-dlp --get-description "VIDEO_URL" > description.txt

# Get video title
yt-dlp --get-title "VIDEO_URL"

# Get video duration
yt-dlp --get-duration "VIDEO_URL"
```

## Output Formats

### Video Summary Template

```markdown
# [Video Title]

**Channel:** [Channel Name]  
**Views:** [View Count] | **Likes:** [Like Count] | **Uploaded:** [Date]  
**Duration:** [Length]  
**URL:** [Video URL]

---

## Overview

[2-3 sentence summary of the video's main topic and purpose]

## Key Points

1. [Main point 1]
2. [Main point 2]
3. [Main point 3]

## Main Takeaways

- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

## Transcript

[Full transcript or link to transcript file]

## Analysis

[Additional analysis, insights, or connections to other content]
```

### Video Comparison Template

```markdown
# Video Comparison: [Topic]

## Videos Analyzed

1. **[Video 1 Title]** - [Channel] ([Views] views)
2. **[Video 2 Title]** - [Channel] ([Views] views)
3. **[Video 3 Title]** - [Channel] ([Views] views)

## Common Themes

- [Theme 1]
- [Theme 2]

## Different Perspectives

**Video 1:** [Perspective]
**Video 2:** [Perspective]
**Video 3:** [Perspective]

## Recommendations

[Which video to watch for what purpose]
```

## File Organization

Save extracted content to:
- **Transcripts:** `/Users/snandwani2/personal/youtube/transcripts/[video-title].txt`
- **Summaries:** `/Users/snandwani2/personal/youtube/summaries/[video-title]-summary.md`
- **Metadata:** `/Users/snandwani2/personal/youtube/metadata/[video-id].json`

Create directory structure:
```bash
mkdir -p ~/personal/youtube/{transcripts,summaries,metadata}
```

## Best Practices

### Do
- ✅ Always extract video title and channel name for context
- ✅ Save transcripts with descriptive filenames
- ✅ Include video URL in all outputs for reference
- ✅ Extract timestamps when available for better navigation
- ✅ Verify transcript language matches video language
- ✅ Check if auto-generated subtitles are available (often more accurate)
- ✅ Extract video description for additional context
- ✅ Save metadata as JSON for programmatic access

### Don't
- ❌ Don't assume all videos have transcripts available
- ❌ Don't download video files unless explicitly requested
- ❌ Don't extract content without attribution
- ❌ Don't ignore video description (often contains key information)
- ❌ Don't skip checking for multiple language options
- ❌ Don't forget to save URLs for future reference

## Error Handling

### No Transcript Available
- Check if video has closed captions enabled
- Try auto-generated subtitles
- Extract description and comments as alternative content
- Inform user that transcript is not available

### Video Not Found
- Verify URL is correct
- Check if video is private or deleted
- Suggest alternative search terms

### Browser Navigation Issues
- Wait for page to fully load using `browser_wait_for`
- Retry navigation if timeout occurs
- Check network connectivity

## Example Prompts

- "Search YouTube for videos about [topic] and summarize the top 3 results"
- "Extract the transcript from this YouTube video: [URL]"
- "Download and analyze the transcript from [video URL]"
- "Compare these three YouTube videos: [URL1], [URL2], [URL3]"
- "Find YouTube videos about [topic] and extract their key points"
- "Get the transcript and create a summary of [video URL]"
- "Analyze this YouTube channel: [channel URL]"
- "Extract metadata from this playlist: [playlist URL]"

## Advanced Features

### Batch Processing

Process multiple videos:
1. Extract list of video URLs
2. For each URL:
   - Navigate to video
   - Extract transcript
   - Save to file
   - Create summary
3. Generate comparison or aggregate analysis

### Content Research

Research a topic across multiple videos:
1. Search YouTube for topic
2. Extract top N video URLs
3. For each video:
   - Extract transcript
   - Identify key points
4. Synthesize findings across all videos
5. Create comprehensive research document

### Channel Monitoring

Track channel updates:
1. Navigate to channel
2. Extract recent uploads
3. Compare with previous state
4. Identify new content
5. Generate update report

## Ready-to-Use Script

A complete Python script is available at:
`/Users/snandwani2/personal/youtube/extract_video.py`

**Quick Start:**
```bash
# Install dependencies
pip install youtube-transcript-api requests

# Extract video (transcript only, no API key needed)
python extract_video.py https://www.youtube.com/watch?v=OdtGN27LchE

# Extract video with metadata (requires YouTube Data API key)
python extract_video.py OdtGN27LchE YOUR_API_KEY
```

The script automatically:
- Extracts video ID from URL
- Gets metadata via YouTube Data API v3 (if API key provided)
- Gets transcript via youtube-transcript-api
- Saves files to organized directories
- Creates markdown summary

## Integration Notes

This skill works best when combined with:
- **YouTube Data API v3** for metadata (recommended)
- **youtube-transcript-api** for transcripts (recommended)
- **Browser tools** as fallback for UI interaction
- **yt-dlp** (optional) for command-line transcript download
- **File writing tools** for saving extracted content
- **Analysis capabilities** for summarizing and comparing content

## Troubleshooting

**Transcript button not found:**
- Video may not have captions
- Try right-clicking video and selecting "Show transcript"
- Check if video has auto-generated subtitles

**Browser timeout:**
- Increase wait time
- Retry navigation
- Check internet connection

**yt-dlp errors:**
- Update yt-dlp: `brew upgrade yt-dlp`
- Check video availability
- Verify URL format

