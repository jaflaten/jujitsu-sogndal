# Full-Width Video Section - Implementation Guide

## ✅ What's Been Implemented

A flexible full-width video section has been added to your homepage, positioned right after the "About" section. The implementation supports three video types:

1. **YouTube embed** (easiest - recommended to start)
2. **Instagram video embed** 
3. **Self-hosted video** (best performance)

## 🎬 How to Configure Your Video

### Option 1: YouTube Video (Recommended)

1. Upload your training video to YouTube
2. Open the video and copy the video ID from the URL
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Video ID is: `dQw4w9WgXcQ`
3. Edit `data/video.yaml` and update:
   ```yaml
   type: youtube
   video_id: "YOUR_VIDEO_ID_HERE"
   title: "Sjå oss i aksjon - Ju Jitsu Sogndal"
   caption: "Opplev energien og teknikkane i våre treningar!"
   ```

### Option 2: Instagram Video

1. Find your Instagram post URL (e.g., from @jujitsusogndal)
2. Edit `data/video.yaml`:
   ```yaml
   type: instagram
   url: "https://www.instagram.com/p/DMQRiL5K9Dr/"
   caption: "Følg oss på Instagram for meir!"
   ```
3. Comment out or remove the YouTube settings

### Option 3: Self-Hosted Video (Best Performance)

1. Create a `videos` folder in the `static` directory
2. Add your video file (MP4 format recommended)
3. Optionally create a WebM version for better browser support
4. Create a poster/thumbnail image
5. Edit `data/video.yaml`:
   ```yaml
   type: self-hosted
   video_url: "/videos/training.mp4"
   video_webm: "/videos/training.webm"  # Optional
   poster: "/images/video-thumbnail.jpg"
   autoplay: false
   muted: false
   loop: false
   caption: "Sjå oss i aksjon!"
   ```

## 🎥 Video Content Suggestions

Consider creating/using videos that show:
- **Welcome message**: Instructor introducing the club (30-60 seconds)
- **Training montage**: Various techniques, drills, sparring (1-2 minutes)
- **Beginner-friendly content**: First-timers going through their first class
- **Belt ceremony**: Showing progression and achievement
- **Fun/community**: Lighter moments showing the friendly atmosphere

## 🔧 Customization Options

### Change Video Caption
Edit the `caption` field in `data/video.yaml` to change the text below the video.

### Remove Caption
Delete or comment out the `caption` line in `data/video.yaml`.

### Disable Video Section
To temporarily hide the video section, either:
1. Rename `data/video.yaml` to `data/video.yaml.disabled`, or
2. Comment out all lines in the file with `#`

### Autoplay Video (Self-hosted only)
```yaml
autoplay: true
muted: true  # Required for autoplay to work in browsers
loop: true   # Optional: make it loop continuously
```

## 📱 Mobile Optimization

The video section is fully responsive:
- YouTube/Instagram embeds automatically adjust to screen size
- Self-hosted videos use responsive CSS
- All videos maintain proper aspect ratio on mobile devices

## 🚀 Next Steps

1. **Choose your video source** (YouTube is easiest to start)
2. **Update `data/video.yaml`** with your video details
3. **Uncomment the video section** in `layouts/_default/home.html` (lines 42-48)
4. **Test locally**: Run `hugo server` and view at http://localhost:1313
5. **Deploy**: Commit changes and push to your repository

**Note:** The video section is currently commented out. To enable it, edit `layouts/_default/home.html` and remove the `<!--` and `-->` comment markers around lines 42-48.

## 📂 Files Modified/Created

- ✅ `layouts/partials/video-section.html` - Video section template
- ✅ `data/video.yaml` - Video configuration
- ✅ `layouts/_default/home.html` - Homepage integration

## 💡 Tips

- **Video length**: Keep it under 2 minutes for best engagement
- **YouTube unlisted**: You can use unlisted YouTube videos (not searchable but accessible via link)
- **File size**: If self-hosting, compress video to under 10MB for faster loading
- **Thumbnail**: Use an action shot for the poster image to grab attention

## ❓ Need Help?

If you need to adjust the positioning, styling, or behavior of the video section, all the code is in:
- `layouts/partials/video-section.html` - for styling/structure changes
- `data/video.yaml` - for content/configuration changes
