# Dynamic Instagram Integration - Implementation Guide

## ✅ What's Been Implemented

I've created a complete dynamic Instagram integration system with three implementation options:

### Option 1: Manual Update (Current - Simplest)
Keep your current hardcoded posts and update them manually when needed.

### Option 2: Automated GitHub Actions (Recommended)
Automatically fetch and update Instagram posts every 6 hours using GitHub Actions.

### Option 3: Client-Side Dynamic (Future Enhancement)
Load Instagram posts dynamically in the browser using JavaScript.

## 📁 Files Created/Modified

### New Files:
1. **`layouts/partials/instagram-feed.html`** - New Instagram gallery template
2. **`static/js/instagram-feed.js`** - JavaScript for dynamic loading
3. **`scripts/update_instagram.py`** - Python script to fetch latest posts
4. **`.github/workflows/update-instagram.yml`** - GitHub Action for automation

### Modified Files:
1. **`layouts/_default/home.html`** - Uses new instagram-feed partial
2. **`layouts/_default/baseof.html`** - Includes instagram-feed.js
3. **`data/instagram.yaml`** - Added `use_dynamic_feed` flag

## 🚀 Quick Start - Choose Your Method

### Method 1: Keep Current (No Changes Needed)

Everything works as before. Your hardcoded posts will display perfectly.

**To update posts:**
1. Edit `data/instagram.yaml`
2. Update the `posts` array with new URLs and images
3. Commit and deploy

### Method 2: Enable GitHub Actions Automation (Recommended)

This will automatically fetch your latest 9 Instagram posts every 6 hours.

**Setup Steps:**

1. **Push the new workflow file to GitHub:**
   ```bash
   git add .github/workflows/update-instagram.yml
   git add scripts/update_instagram.py
   git commit -m "Add Instagram auto-update workflow"
   git push
   ```

2. **Enable GitHub Actions:**
   - Go to your repository on GitHub
   - Click "Actions" tab
   - If prompted, enable workflows

3. **Manual trigger (optional):**
   - Go to Actions → "Update Instagram Feed"
   - Click "Run workflow"

4. **That's it!** The feed will auto-update every 6 hours

**Note:** This method currently uses Instagram's public API which may be unreliable. For production, consider using Instagram Basic Display API (requires app registration).

### Method 3: Client-Side Dynamic Loading

Enable JavaScript-based dynamic loading:

1. Edit `data/instagram.yaml`:
   ```yaml
   use_dynamic_feed: true
   ```

2. The JavaScript will load posts dynamically from your configured URLs

## 📝 Configuration Options

### Instagram YAML Structure

```yaml
instagram:
  username: jujitsusogndal
  image: /images/logo_knot_og.png
  use_dynamic_feed: false  # Set to true for client-side dynamic loading
  posts:
    - title: Post 1
      img: /images/bakkekontroll.png
      url: https://www.instagram.com/p/DMQRiL5K9Dr/
    - title: Post 2
      img: /images/slag.png
      url: https://www.instagram.com/p/DMQQ7p6KYGi/
```

### Fields Explained:

- **`username`**: Your Instagram handle (without @)
- **`image`**: Profile image shown in each post card
- **`use_dynamic_feed`**: Enable client-side dynamic loading
- **`posts`**: Array of Instagram posts
  - **`title`**: Description/alt text
  - **`img`**: Local image path (for cached images)
  - **`img_external`**: External image URL (alternative)
  - **`url`**: Full Instagram post URL

## 🔧 Advanced Configuration

### Change Update Frequency (GitHub Actions)

Edit `.github/workflows/update-instagram.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # Examples:
  # - cron: '0 */3 * * *'  # Every 3 hours
  # - cron: '0 0 * * *'    # Daily at midnight
  # - cron: '0 */12 * * *' # Twice daily
```

### Download Images Locally

Edit `scripts/update_instagram.py`:

```python
DOWNLOAD_IMAGES = True  # Downloads and hosts images locally
```

Benefits:
- Faster loading
- Works even if Instagram changes their URLs
- Better privacy (no external tracking)

Drawbacks:
- Uses more repository storage
- Images in git history

### Change Number of Posts

Edit `scripts/update_instagram.py`:

```python
MAX_POSTS = 9  # Change to 6, 12, etc.
```

Also update the grid in `layouts/partials/instagram-feed.html` if needed.

## 🎨 Customization

### Change Gallery Layout

Edit `layouts/partials/instagram-feed.html`:

```html
<!-- Current: 3 columns on desktop -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">

<!-- 2 columns: -->
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

<!-- 4 columns: -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
```

### Remove/Customize Icons

Edit the SVG icons in `layouts/partials/instagram-feed.html` (lines 55-58)

### Change Hover Effect

Modify the CSS classes:
```html
<!-- Current -->
<div class="... hover:border-black ... hover:shadow-lg">

<!-- Custom -->
<div class="... hover:border-blue-500 ... hover:shadow-2xl hover:scale-105">
```

## 🔐 Instagram Basic Display API (Production Solution)

For a more reliable solution, use Instagram's official API:

### Setup Steps:

1. **Create Facebook App:**
   - Go to https://developers.facebook.com/
   - Create a new app
   - Add "Instagram Basic Display" product

2. **Get Access Token:**
   - Configure Instagram Basic Display
   - Add test users
   - Generate access token

3. **Update Python Script:**
   ```python
   ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"
   ```

4. **Add to GitHub Secrets:**
   - Repository Settings → Secrets → New secret
   - Name: `INSTAGRAM_ACCESS_TOKEN`
   - Value: Your access token

5. **Update Workflow:**
   ```yaml
   - name: Update Instagram feed
     env:
       INSTAGRAM_ACCESS_TOKEN: ${{ secrets.INSTAGRAM_ACCESS_TOKEN }}
     run: python scripts/update_instagram.py
   ```

## 📊 Comparison of Methods

| Feature | Manual | GitHub Actions | Client-Side |
|---------|--------|----------------|-------------|
| Setup Complexity | ⭐ Simple | ⭐⭐ Medium | ⭐⭐⭐ Advanced |
| Maintenance | Manual updates | Automatic | Automatic |
| Performance | ⭐⭐⭐ Fast | ⭐⭐⭐ Fast | ⭐⭐ Slower |
| Reliability | ⭐⭐⭐ High | ⭐⭐ Medium | ⭐ Low |
| Real-time | ❌ No | ⏰ Every 6 hours | ✅ Live |
| Image Hosting | Local | Local or External | External |
| API Required | ❌ No | ⚠️ Optional | ⚠️ Optional |

## 🐛 Troubleshooting

### GitHub Action Fails

1. Check Actions tab for error logs
2. Verify Instagram profile is public
3. Instagram may have changed their HTML structure (update script)

### Posts Not Updating

1. Check GitHub Actions logs
2. Manually run: `python scripts/update_instagram.py`
3. Verify `data/instagram.yaml` was updated

### Images Not Loading

1. Check if image paths are correct
2. Verify images exist in `static/images/`
3. Check browser console for errors

### JavaScript Not Working

1. Check browser console for errors
2. Verify `instagram-feed.js` is loaded
3. Check if `instagramConfig` is defined

## 💡 Recommendations

**For Your Use Case (jujitsusogndal):**

1. **Start with Manual** - Keep current setup working
2. **Test GitHub Actions** - Enable automation when ready
3. **Consider API** - For production reliability

**Best Practice:**
- Use GitHub Actions with Instagram Basic Display API
- Download images locally for faster loading
- Update every 6-12 hours (not too frequent)

## 🔄 Next Steps

1. ✅ Test current implementation (static posts)
2. 📤 Push workflow files to GitHub
3. 🔧 Enable GitHub Actions
4. ⏱️ Wait for first auto-update (or trigger manually)
5. 🎉 Enjoy automated Instagram feed!

## 📞 Support

If you encounter issues:
1. Check GitHub Actions logs
2. Review Instagram API documentation
3. Test Python script locally: `python scripts/update_instagram.py`

---

*Last updated: 2025-11-05*
