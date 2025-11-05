# Instagram Feed - Setup Guide

## Current Status

The Instagram workflow exists but **web scraping is blocked** by Instagram (rate limiting). This is expected and normal - Instagram protects its data.

## Three Options to Display Instagram Posts

### ✅ Option 1: Manual Updates (Current - Works Now)

**Best for:** Simple sites, occasional updates

Your current setup in `data/instagram.yaml` works perfectly. Just manually update it when you want to showcase new posts.

**How to add a new post:**
1. Open `data/instagram.yaml`
2. Add a new entry:
```yaml
instagram:
  username: jujitsusogndal
  image: /images/logo_knot_og.png
  posts:
    - title: "New training session"
      img: /images/your-image.jpg
      url: https://www.instagram.com/p/POST_CODE/
```

**Pros:** Simple, reliable, no API needed
**Cons:** Manual work

---

### 🔧 Option 2: Instagram Basic Display API (Recommended)

**Best for:** Automatic updates, production sites

This is Instagram's official way to access your posts programmatically.

#### Setup Steps:

1. **Create a Facebook Developer Account**
   - Go to https://developers.facebook.com/
   - Sign up/login with your Facebook account

2. **Create an App**
   - Click "My Apps" → "Create App"
   - Choose "Consumer" or "Business" type
   - Fill in app details

3. **Add Instagram Basic Display Product**
   - In your app dashboard, click "+ Add Product"
   - Select "Instagram Basic Display"
   - Click "Set Up"

4. **Configure Instagram Basic Display**
   - Valid OAuth Redirect URIs: `https://jujitsusogndal.no/auth/`
   - Deauthorize Callback URL: `https://jujitsusogndal.no/auth/`
   - Data Deletion Request URL: `https://jujitsusogndal.no/auth/`

5. **Add Instagram Test User**
   - In Basic Display settings
   - Click "Add Instagram Test User"
   - Add your @jujitsusogndal account
   - Accept the invitation in Instagram app (Settings → Apps → Tester Invites)

6. **Generate Access Token**
   - Click "Generate Token" next to the test user
   - Copy the token (it will look like a long string)

7. **Add Token to GitHub Secrets**
   - Go to GitHub: Settings → Secrets → Actions
   - Click "New repository secret"
   - Name: `INSTAGRAM_ACCESS_TOKEN`
   - Value: Paste your token
   - Click "Add secret"

8. **Update the Python Script**
   
   I'll create an improved version that uses the official API when available.

#### Update Script to Use API:

Replace `scripts/update_instagram.py` with the API version (I can help with this).

**Pros:** Official, reliable, automatic
**Cons:** Requires initial setup (~30 minutes)

---

### 🎨 Option 3: Instagram Embed Widget

**Best for:** Quick visual feed without technical setup

Use Instagram's official embed widget.

#### Steps:

1. Go to https://embedsocial.com/products/embedfeed/ or similar service
2. Connect your Instagram account
3. Get embed code
4. Add to your Hugo site

**Example services:**
- EmbedSocial (free tier available)
- SnapWidget
- Juicer
- Flockler

**Pros:** Easy, automatic, visual
**Cons:** Third-party dependency, may have branding

---

## Recommended Approach

### Phase 1: Now (5 minutes)
Keep manual updates in `data/instagram.yaml` - it works great!

### Phase 2: Later (30 minutes when you have time)
Set up Instagram Basic Display API for automation.

### Phase 3: Optional
Consider professional embed widget for richer display.

---

## Quick Fix for GitHub Actions

The workflow won't fail anymore - I've updated it to gracefully handle when Instagram blocks scraping. It will simply keep your existing posts.

To test:
```bash
git add scripts/update_instagram.py
git commit -m "Fix Instagram workflow to handle rate limiting"
git push
```

Then trigger the workflow manually - it should succeed (keeping current posts).

---

## Questions?

The current setup works fine for now. When you're ready to automate, the Instagram Basic Display API is the way to go. I can help with the implementation when you decide to proceed.
