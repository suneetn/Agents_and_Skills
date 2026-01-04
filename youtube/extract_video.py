#!/usr/bin/env python3
"""
YouTube Video Extractor using APIs
Extracts metadata and transcripts from YouTube videos using official and unofficial APIs
"""

import requests
import json
import sys
import re
from datetime import datetime
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    TRANSCRIPT_API_AVAILABLE = False
    print("Warning: youtube-transcript-api not installed. Install with: pip install youtube-transcript-api")


def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'  # Direct video ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_metadata_api(video_id, api_key=None):
    """Get video metadata using YouTube Data API v3"""
    if not api_key:
        return None, "API key not provided"
    
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": video_id,
            "key": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("items"):
            return None, "Video not found"
        
        video = data["items"][0]
        metadata = {
            "title": video["snippet"]["title"],
            "channel": video["snippet"]["channelTitle"],
            "channelId": video["snippet"]["channelId"],
            "description": video["snippet"]["description"],
            "views": int(video["statistics"]["viewCount"]),
            "likes": int(video["statistics"].get("likeCount", 0)),
            "commentCount": int(video["statistics"].get("commentCount", 0)),
            "duration": video["contentDetails"]["duration"],
            "publishedAt": video["snippet"]["publishedAt"],
            "tags": video["snippet"].get("tags", []),
            "categoryId": video["snippet"].get("categoryId"),
            "thumbnail": video["snippet"]["thumbnails"]["high"]["url"]
        }
        
        return metadata, None
    except Exception as e:
        return None, str(e)


def get_transcript_api(video_id, languages=['en']):
    """Get video transcript using youtube-transcript-api"""
    if not TRANSCRIPT_API_AVAILABLE:
        return None, "youtube-transcript-api not installed"
    
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=languages)
        # Convert FetchedTranscriptSnippet objects to dicts
        transcript_dicts = [
            {
                "text": entry.text,
                "start": entry.start,
                "duration": entry.duration
            }
            for entry in transcript
        ]
        return transcript_dicts, None
    except Exception as e:
        return None, str(e)


def format_transcript(transcript_data, format='text'):
    """Format transcript data"""
    if format == 'text':
        return "\n".join([
            f"[{entry['start']:.1f}s] {entry['text']}"
            for entry in transcript_data
        ])
    elif format == 'plain':
        return "\n".join([entry['text'] for entry in transcript_data])
    else:
        return transcript_data


def extract_video(video_url_or_id, api_key=None, output_dir=None):
    """Extract complete video information"""
    
    # Extract video ID
    video_id = extract_video_id(video_url_or_id)
    if not video_id:
        return {"error": "Invalid YouTube URL or video ID"}
    
    # Setup output directory
    if output_dir is None:
        output_dir = Path.home() / "personal" / "youtube"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    transcripts_dir = output_dir / "transcripts"
    summaries_dir = output_dir / "summaries"
    metadata_dir = output_dir / "metadata"
    
    transcripts_dir.mkdir(exist_ok=True)
    summaries_dir.mkdir(exist_ok=True)
    metadata_dir.mkdir(exist_ok=True)
    
    result = {
        "videoId": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "extractedAt": datetime.now().isoformat(),
        "methods": []
    }
    
    # Get metadata
    if api_key:
        metadata, error = get_metadata_api(video_id, api_key)
        if metadata:
            result["metadata"] = metadata
            result["methods"].append("YouTube Data API v3")
        else:
            result["metadataError"] = error
    else:
        result["metadataNote"] = "API key not provided. Only transcript will be extracted."
    
    # Get transcript
    transcript, error = get_transcript_api(video_id)
    if transcript:
        result["transcript"] = transcript
        result["transcriptText"] = format_transcript(transcript, 'plain')
        result["transcriptFormatted"] = format_transcript(transcript, 'text')
        result["methods"].append("youtube-transcript-api")
    else:
        result["transcriptError"] = error
    
    # Save files
    safe_title = result.get("metadata", {}).get("title", video_id)
    safe_title = "".join(c for c in safe_title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
    
    # Save metadata
    metadata_file = metadata_dir / f"{video_id}.json"
    with open(metadata_file, 'w') as f:
        json.dump(result, f, indent=2)
    result["metadataFile"] = str(metadata_file)
    
    # Save transcript if available
    if transcript:
        transcript_file = transcripts_dir / f"{safe_title}_{video_id}.txt"
        with open(transcript_file, 'w') as f:
            f.write(result["transcriptFormatted"])
        result["transcriptFile"] = str(transcript_file)
        
        # Save plain transcript
        transcript_plain_file = transcripts_dir / f"{safe_title}_{video_id}_plain.txt"
        with open(transcript_plain_file, 'w') as f:
            f.write(result["transcriptText"])
    
    # Create summary
    if result.get("metadata") and result.get("transcriptText"):
        summary_file = summaries_dir / f"{safe_title}_{video_id}-summary.md"
        summary = create_summary(result)
        with open(summary_file, 'w') as f:
            f.write(summary)
        result["summaryFile"] = str(summary_file)
    
    return result


def create_summary(result):
    """Create markdown summary"""
    metadata = result.get("metadata", {})
    transcript = result.get("transcriptText", "")
    
    summary = f"""# {metadata.get('title', 'Video')}

**Channel:** {metadata.get('channel', 'Unknown')}  
**Views:** {metadata.get('views', 'N/A'):,} | **Likes:** {metadata.get('likes', 'N/A'):,} | **Uploaded:** {metadata.get('publishedAt', 'N/A')}  
**Duration:** {metadata.get('duration', 'N/A')}  
**URL:** {result['url']}

---

## Overview

{metadata.get('description', '')[:500]}...

## Transcript

{transcript[:2000]}...

*Full transcript available in: {result.get('transcriptFile', 'N/A')}*

## Metadata

- **Video ID:** {result['videoId']}
- **Channel ID:** {metadata.get('channelId', 'N/A')}
- **Comments:** {metadata.get('commentCount', 'N/A'):,}
- **Tags:** {', '.join(metadata.get('tags', [])[:10])}

## Extraction Info

- **Extracted At:** {result['extractedAt']}
- **Methods Used:** {', '.join(result.get('methods', []))}
"""
    return summary


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python extract_video.py <youtube_url_or_id> [api_key]")
        print("\nExample:")
        print("  python extract_video.py https://www.youtube.com/watch?v=OdtGN27LchE")
        print("  python extract_video.py OdtGN27LchE YOUR_API_KEY")
        sys.exit(1)
    
    video_url_or_id = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Extracting video: {video_url_or_id}")
    if api_key:
        print("Using YouTube Data API v3 for metadata")
    else:
        print("Note: No API key provided. Only transcript will be extracted.")
    
    result = extract_video(video_url_or_id, api_key)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    print("\n✅ Extraction complete!")
    print(f"\nVideo ID: {result['videoId']}")
    
    if result.get("metadata"):
        print(f"Title: {result['metadata']['title']}")
        print(f"Channel: {result['metadata']['channel']}")
        print(f"Views: {result['metadata']['views']:,}")
    
    if result.get("transcript"):
        print(f"Transcript: {len(result['transcript'])} entries")
    
    print(f"\nFiles saved:")
    if result.get("metadataFile"):
        print(f"  - Metadata: {result['metadataFile']}")
    if result.get("transcriptFile"):
        print(f"  - Transcript: {result['transcriptFile']}")
    if result.get("summaryFile"):
        print(f"  - Summary: {result['summaryFile']}")


if __name__ == "__main__":
    main()

