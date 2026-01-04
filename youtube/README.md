# YouTube Video Extractor

Extract metadata and transcripts from YouTube videos using APIs.

## Quick Start

### Install Dependencies

```bash
pip install youtube-transcript-api requests
```

### Basic Usage (Transcript Only)

```bash
python extract_video.py https://www.youtube.com/watch?v=OdtGN27LchE
```

This will extract the transcript without needing an API key.

### Full Extraction (Metadata + Transcript)

1. Get a YouTube Data API v3 key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Run:

```bash
python extract_video.py OdtGN27LchE YOUR_API_KEY
```

## Output

Files are saved to:
- `~/personal/youtube/metadata/[video-id].json` - Complete metadata and transcript data
- `~/personal/youtube/transcripts/[title]_[video-id].txt` - Formatted transcript with timestamps
- `~/personal/youtube/transcripts/[title]_[video-id]_plain.txt` - Plain text transcript
- `~/personal/youtube/summaries/[title]_[video-id]-summary.md` - Markdown summary

## API Methods Used

1. **YouTube Data API v3** (Official) - For metadata
   - Requires API key
   - Free quota: 10,000 units/day
   - Get key: https://console.cloud.google.com/

2. **youtube-transcript-api** (Unofficial) - For transcripts
   - No API key needed
   - Works for most public videos
   - Install: `pip install youtube-transcript-api`

## Examples

```bash
# Extract by URL
python extract_video.py https://www.youtube.com/watch?v=OdtGN27LchE

# Extract by video ID
python extract_video.py OdtGN27LchE

# Extract with metadata
python extract_video.py OdtGN27LchE YOUR_API_KEY
```

## Advantages Over Browser Automation

✅ **Faster** - No browser overhead  
✅ **More Reliable** - Structured API responses  
✅ **Better for Batch Processing** - Can process multiple videos  
✅ **No UI Dependencies** - Works in headless environments  
✅ **Rate Limits** - Predictable and manageable  

## Troubleshooting

**"youtube-transcript-api not installed"**
```bash
pip install youtube-transcript-api
```

**"Video not found"**
- Check that the video ID is correct
- Ensure the video is public

**"No transcript available"**
- Some videos don't have transcripts
- Try auto-generated subtitles (default)

**"API key invalid"**
- Verify API key in Google Cloud Console
- Ensure YouTube Data API v3 is enabled



