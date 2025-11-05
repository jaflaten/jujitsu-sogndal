#!/usr/bin/env python3
"""
Instagram Feed Updater for Hugo Site

This script fetches the latest posts from an Instagram profile and updates
the data/instagram.yaml file. It uses Instagram's public API (no authentication needed).

Usage:
    python scripts/update_instagram.py

Requirements:
    pip install requests pyyaml pillow

Note: This scrapes Instagram's public page. For production use, consider:
1. Using Instagram Basic Display API (requires app registration)
2. Running this as a GitHub Action on a schedule
3. Caching images locally to avoid external dependencies
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
import requests
import yaml


class InstagramFeedUpdater:
    def __init__(self, username: str, max_posts: int = 9):
        self.username = username
        self.max_posts = max_posts
        self.base_url = f"https://www.instagram.com/{username}/"
        
    def fetch_posts(self) -> Optional[List[Dict]]:
        """
        Fetch latest posts from Instagram profile using public API
        """
        try:
            # Instagram embeds data in the page HTML
            response = requests.get(
                self.base_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                },
                timeout=10
            )
            response.raise_for_status()
            
            # Extract JSON data from the page
            posts_data = self._extract_posts_from_html(response.text)
            
            if not posts_data:
                print("⚠️  Could not extract posts from Instagram page")
                return None
                
            return posts_data[:self.max_posts]
            
        except requests.RequestException as e:
            print(f"❌ Error fetching Instagram data: {e}")
            return None
    
    def _extract_posts_from_html(self, html: str) -> List[Dict]:
        """
        Extract post data from Instagram's HTML
        """
        posts = []
        
        # Try to find the data in script tags
        pattern = r'window\._sharedData\s*=\s*({.*?});'
        match = re.search(pattern, html)
        
        if not match:
            # Try alternative pattern for newer Instagram layouts
            pattern = r'<script type="application/ld\+json">({.*?})</script>'
            matches = re.findall(pattern, html, re.DOTALL)
            
            for match_str in matches:
                try:
                    data = json.loads(match_str)
                    # Process structured data if available
                except json.JSONDecodeError:
                    continue
        else:
            try:
                data = json.loads(match.group(1))
                
                # Navigate to posts in the data structure
                edges = (data.get('entry_data', {})
                        .get('ProfilePage', [{}])[0]
                        .get('graphql', {})
                        .get('user', {})
                        .get('edge_owner_to_timeline_media', {})
                        .get('edges', []))
                
                for edge in edges:
                    node = edge.get('node', {})
                    
                    post = {
                        'title': node.get('accessibility_caption', 'Instagram post'),
                        'url': f"https://www.instagram.com/p/{node.get('shortcode')}/",
                        'img': node.get('display_url'),
                        'thumbnail': node.get('thumbnail_src'),
                        'timestamp': node.get('taken_at_timestamp'),
                        'likes': node.get('edge_liked_by', {}).get('count', 0),
                        'comments': node.get('edge_media_to_comment', {}).get('count', 0),
                    }
                    
                    posts.append(post)
                    
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                print(f"⚠️  Error parsing Instagram data: {e}")
        
        return posts
    
    def download_image(self, url: str, filename: str, output_dir: Path) -> Optional[str]:
        """
        Download an image from Instagram
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            output_path = output_dir / filename
            output_path.write_bytes(response.content)
            
            return f"/images/instagram/{filename}"
            
        except requests.RequestException as e:
            print(f"⚠️  Could not download image {filename}: {e}")
            return None
    
    def update_yaml_file(self, posts: List[Dict], yaml_path: Path, 
                        download_images: bool = False) -> bool:
        """
        Update the instagram.yaml file with new posts
        """
        try:
            # Read existing config
            if yaml_path.exists():
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
            else:
                config = {}
            
            # Ensure structure exists
            if 'instagram' not in config:
                config['instagram'] = {}
            
            # Update username
            config['instagram']['username'] = self.username
            
            # Keep existing profile image or use default
            if 'image' not in config['instagram']:
                config['instagram']['image'] = '/images/logo_knot_og.png'
            
            # Process posts
            updated_posts = []
            
            for i, post in enumerate(posts, 1):
                post_data = {
                    'title': post.get('title', f'Post {i}'),
                    'url': post['url']
                }
                
                # Handle images
                if download_images and post.get('img'):
                    # Download and save image
                    img_dir = Path('static/images/instagram')
                    img_dir.mkdir(parents=True, exist_ok=True)
                    
                    filename = f"post_{i}.jpg"
                    local_path = self.download_image(post['img'], filename, img_dir)
                    
                    if local_path:
                        post_data['img'] = local_path
                    else:
                        # Fallback to external URL
                        post_data['img_external'] = post['img']
                else:
                    # Use external URL
                    post_data['img_external'] = post.get('img') or post.get('thumbnail')
                
                updated_posts.append(post_data)
            
            config['instagram']['posts'] = updated_posts
            
            # Write updated config
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            print(f"✅ Successfully updated {yaml_path} with {len(updated_posts)} posts")
            return True
            
        except Exception as e:
            print(f"❌ Error updating YAML file: {e}")
            return False


def main():
    """
    Main function
    """
    # Configuration
    INSTAGRAM_USERNAME = "jujitsusogndal"
    MAX_POSTS = 9
    DOWNLOAD_IMAGES = False  # Set to True to download images locally
    
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    yaml_path = project_root / "data" / "instagram.yaml"
    
    print(f"🔄 Updating Instagram feed for @{INSTAGRAM_USERNAME}...")
    
    # Create updater
    updater = InstagramFeedUpdater(INSTAGRAM_USERNAME, MAX_POSTS)
    
    # Fetch posts
    posts = updater.fetch_posts()
    
    if not posts:
        print("❌ No posts fetched. Using existing configuration.")
        return 1
    
    print(f"📥 Fetched {len(posts)} posts")
    
    # Update YAML file
    success = updater.update_yaml_file(posts, yaml_path, DOWNLOAD_IMAGES)
    
    if success:
        print("✨ Instagram feed updated successfully!")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
