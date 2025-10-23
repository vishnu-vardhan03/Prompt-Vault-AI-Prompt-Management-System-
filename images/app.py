from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage for prompts with Ghibli-style images
prompts_db = [
    {
        'id': 1,
        'title': 'Peaceful Village Scene',
        'prompt': 'Studio Ghibli style, peaceful countryside village, rolling green hills, traditional Japanese houses with tiled roofs, flower gardens, blue sky with fluffy clouds, warm sunlight, hand-drawn animation style, watercolor aesthetic, nostalgic atmosphere, highly detailed',
        'category': 'Landscape',
        'tags': ['ghibli', 'village', 'countryside', 'peaceful'],
        'likes': 542,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1528164344705-47542687000d?w=800&h=600&fit=crop',
        'created_at': '2025-10-08'
    },
    {
        'id': 2,
        'title': 'Magical Forest Path',
        'prompt': 'Studio Ghibli art style, enchanted forest path, ancient trees with twisted branches, dappled sunlight filtering through leaves, moss-covered stones, glowing fireflies, mystical atmosphere, vibrant greens, anime style, soft lighting, whimsical and dreamy',
        'category': 'Landscape',
        'tags': ['ghibli', 'forest', 'magical', 'nature'],
        'likes': 689,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1511497584788-876760111969?w=800&h=600&fit=crop',
        'created_at': '2025-10-09'
    },
    {
        'id': 3,
        'title': 'Cozy Bakery Interior',
        'prompt': 'Studio Ghibli inspired cozy bakery interior, wooden counters filled with fresh bread and pastries, warm lighting from hanging lamps, large windows with afternoon sunlight, potted plants, vintage furniture, hand-drawn anime style, inviting atmosphere, detailed textures',
        'category': 'Interior',
        'tags': ['ghibli', 'bakery', 'cozy', 'interior'],
        'likes': 823,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=800&h=600&fit=crop',
        'created_at': '2025-10-10'
    },
        {
    'id': 4,
    'title': 'Rugged Man with Motorcycle',
    'prompt': 'A black and white, full-length portrait featuring a rugged man with a beard and short, tousled hair, leaning against a classic-style motorcycle. He is wearing a dark, short-sleeved, collared shirt with a strong and confident pose, cinematic photography aesthetic, moody contrast, detailed textures, timeless atmosphere.',
    'category': 'charcter',
    'tags': ['man', 'motorcycle', 'rugged', 'black-and-white', 'character'],
    'likes': 327,
    'trending': False,
    'image_url': 'https://atomguygg.github.io/atomguy/ai/boys/7.jpg',
    'created_at': '2025-10-10'
    },
    {
        'id': 5,
        'title': 'Floating Castle in Sky',
        'prompt': 'Studio Ghibli style floating castle, surrounded by fluffy white clouds, blue sky, intricate architecture with towers and bridges, lush gardens on floating islands, magical atmosphere, anime aesthetic, dreamlike scene, vibrant colors, epic scale, detailed background art',
        'category': 'Fantasy',
        'tags': ['ghibli', 'castle', 'sky', 'fantasy'],
        'likes': 1456,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&h=600&fit=crop',
        'created_at': '2025-10-10'
    },
    {
        'id': 6,
        'title': 'Seaside Town View',
        'prompt': 'Studio Ghibli style seaside town, colorful houses on hillside, blue ocean with gentle waves, fishing boats in harbor, seagulls flying, clear summer day, hand-painted look, warm color palette, anime background art, peaceful coastal atmosphere, highly detailed',
        'category': 'Landscape',
        'tags': ['ghibli', 'ocean', 'town', 'coastal'],
        'likes': 934,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=600&fit=crop',
        'created_at': '2025-10-08'
    },
    {
        'id': 7,
        'title': 'Train Station Platform',
        'prompt': 'Studio Ghibli anime style, old Japanese train station platform at sunset, wooden benches, hanging lanterns starting to glow, train tracks extending into distance, cherry blossom petals falling, nostalgic mood, warm orange and pink sky, detailed background illustration',
        'category': 'Urban',
        'tags': ['ghibli', 'train', 'station', 'sunset'],
        'likes': 1089,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1464037866556-6812c9d1c72e?w=800&h=600&fit=crop',
        'created_at': '2025-10-09'
    },
    {
        'id': 8,
        'title': 'Spirited Bath House',
        'prompt': 'Studio Ghibli inspired traditional bath house, multi-story wooden structure with red bridges, lanterns glowing at night, steam rising, reflection in water, Japanese architecture, magical atmosphere, rich colors, anime art style, intricate details, mystical setting',
        'category': 'Fantasy',
        'tags': ['ghibli', 'bathhouse', 'traditional', 'night'],
        'likes': 1678,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1480796927426-f609979314bd?w=800&h=600&fit=crop',
        'created_at': '2025-10-10'
    },
    {
        'id': 9,
        'title': 'Flying Machine Adventure',
        'prompt': 'Studio Ghibli style retro flying machine, propeller aircraft with wings, pilot visible in cockpit, soaring through clouds, blue sky, adventure atmosphere, hand-drawn animation aesthetic, whimsical design, anime art style, sense of freedom and wonder',
        'category': 'Fantasy',
        'tags': ['ghibli', 'flying', 'adventure', 'aircraft'],
        'likes': 1523,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=600&fit=crop',
        'created_at': '2025-10-09'
    },
    {
        'id': 10,
        'title': 'Garden Greenhouse',
        'prompt': 'Studio Ghibli style greenhouse interior, lush plants and flowers, glass panels with sunlight streaming through, wooden shelves with potted plants, watering cans, gardening tools, peaceful atmosphere, warm colors, anime aesthetic, detailed botanical illustration, cozy and inviting',
        'category': 'Interior',
        'tags': ['ghibli', 'greenhouse', 'plants', 'garden'],
        'likes': 756,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1466781783364-36c955e42a7f?w=800&h=600&fit=crop',
        'created_at': '2025-10-08'
    },
    {
        'id': 11,
        'title': 'Rainy Day Window View',
        'prompt': 'Studio Ghibli anime style, view from inside looking out rain-covered window, raindrops on glass, blurred colorful lights outside, cozy interior with warm lamp, cup of tea on windowsill, nostalgic rainy day mood, soft focus, peaceful atmosphere, hand-drawn style',
        'category': 'Interior',
        'tags': ['ghibli', 'rain', 'window', 'cozy'],
        'likes': 1892,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800&h=600&fit=crop',
        'created_at': '2025-10-10'
    },
    {
        'id': 12,
        'title': 'Wise Old Wizard',
        'prompt': 'Studio Ghibli character design, elderly wizard with long white beard, pointy hat, round glasses, warm smile, holding wooden staff, colorful robes, anime art style, expressive face, kind eyes, detailed character illustration, magical aura, whimsical appearance',
        'category': 'Character',
        'tags': ['ghibli', 'wizard', 'character', 'magical'],
        'likes': 1345,
        'trending': True,
        'image_url': 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800&h=600&fit=crop',
        'created_at': '2025-10-09'
    }
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PromptVault - Ghibli AI Image Prompts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #a8e6cf 0%, #88d8b0 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .tagline {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .info-banner {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        
        .info-banner h3 {
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        
        .info-banner p {
            line-height: 1.6;
            opacity: 0.95;
        }
        
        .controls {
            background: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .search-bar {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #88d8b0;
        }
        
        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        select, button {
            padding: 10px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            cursor: pointer;
            background: white;
            transition: all 0.3s;
        }
        
        button {
            background: #88d8b0;
            color: white;
            border: none;
            font-weight: bold;
        }
        
        button:hover {
            background: #6ec59a;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(136, 216, 176, 0.4);
        }
        
        .trending-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 12px;
            background: #ff6b6b;
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .prompts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .prompt-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
            position: relative;
        }
        
        .prompt-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }
        
        .trending-indicator {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #ff6b6b;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            z-index: 10;
            display: flex;
            align-items: center;
            gap: 5px;
            box-shadow: 0 2px 10px rgba(255, 107, 107, 0.4);
        }
        
        .prompt-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            display: block;
        }
        
        .prompt-content {
            padding: 25px;
        }
        
        .prompt-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }
        
        .prompt-title {
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
            flex: 1;
        }
        
        .category-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            background: #88d8b0;
            color: white;
            white-space: nowrap;
            margin-left: 10px;
        }
        
        .prompt-text {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            font-size: 0.95em;
            line-height: 1.6;
            color: #555;
            max-height: 100px;
            overflow: hidden;
            position: relative;
        }
        
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .tag {
            padding: 5px 10px;
            background: #e8f5e9;
            color: #4caf50;
            border-radius: 15px;
            font-size: 0.85em;
        }
        
        .prompt-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }
        
        .likes {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #666;
            cursor: pointer;
            transition: color 0.3s;
        }
        
        .likes:hover {
            color: #e74c3c;
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
        }
        
        .copy-btn, .view-btn {
            padding: 10px 18px;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .copy-btn {
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        }
        
        .copy-btn:hover {
            background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
            transform: scale(1.05);
        }
        
        .view-btn {
            background: linear-gradient(135deg, #2196F3 0%, #0b7dda 100%);
        }
        
        .view-btn:hover {
            background: linear-gradient(135deg, #0b7dda 0%, #0960a5 100%);
            transform: scale(1.05);
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .modal-content {
            background: white;
            padding: 35px;
            border-radius: 20px;
            max-width: 900px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        .modal-content h2 {
            margin-bottom: 20px;
            color: #333;
            font-size: 2em;
        }
        
        .modal-image {
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .prompt-display {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            border-left: 5px solid #88d8b0;
        }
        
        .prompt-display strong {
            display: block;
            margin-bottom: 12px;
            color: #333;
            font-size: 1.1em;
        }
        
        .prompt-display p {
            line-height: 1.8;
            color: #444;
            font-size: 1.05em;
        }
        
        .modal-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        
        .copy-full-btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .copy-full-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(76, 175, 80, 0.4);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        
        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 120px;
        }
        
        .close-modal {
            float: right;
            font-size: 32px;
            cursor: pointer;
            color: #999;
            line-height: 1;
            transition: color 0.3s;
        }
        
        .close-modal:hover {
            color: #333;
        }
        
        .image-preview {
            width: 100%;
            max-height: 200px;
            object-fit: cover;
            border-radius: 10px;
            margin-top: 10px;
            display: none;
        }
        
        .stats-bar {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            flex: 1;
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #88d8b0;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            
            .prompts-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-bar {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎨 PromptVault - Ghibli Style</h1>
            <p class="tagline">Trending Studio Ghibli AI Image Generation Prompts</p>
        </header>
        
        <div class="info-banner">
            <h3>✨ How to Use These Prompts</h3>
            <p>Browse our curated collection of Studio Ghibli-inspired prompts. Click on any prompt card to view the full details, then copy the prompt text. Paste it into your favorite AI image generator (like Midjourney, DALL-E, Stable Diffusion, or Leonardo.ai) to create your own beautiful Ghibli-style artwork!</p>
        </div>
        
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number">{{ prompts|length }}</div>
                <div class="stat-label">Total Prompts</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ prompts|selectattr('trending', 'equalto', True)|list|length }}</div>
                <div class="stat-label">Trending Now</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">12K+</div>
                <div class="stat-label">Total Copies</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search Ghibli prompts...">
                <button onclick="searchPrompts()">🔍 Search</button>
            </div>
            <div class="filters">
                <select id="categoryFilter" onchange="filterPrompts()">
                    <option value="">All Categories</option>
                    <option value="Landscape">Landscape</option>
                    <option value="Character">Character</option>
                    <option value="Interior">Interior</option>
                    <option value="Fantasy">Fantasy</option>
                    <option value="Urban">Urban</option>
                </select>
                <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;">
                    <input type="checkbox" id="trendingOnly" onchange="filterPrompts()">
                    <span>🔥 Trending Only</span>
                </label>
                <button onclick="openAddModal()">+ Add Your Prompt</button>
            </div>
        </div>
        
        <div class="prompts-grid" id="promptsGrid">
            {% for prompt in prompts %}
            <div class="prompt-card" data-category="{{ prompt.category }}" data-trending="{{ prompt.trending }}">
                {% if prompt.trending %}
                <div class="trending-indicator">🔥 Trending</div>
                {% endif %}
                <img src="{{ prompt.image_url }}" alt="{{ prompt.title }}" class="prompt-image" onclick="viewPrompt({{ prompt.id }})">
                <div class="prompt-content">
                    <div class="prompt-header">
                        <div class="prompt-title">{{ prompt.title }}</div>
                        <div class="category-badge">{{ prompt.category }}</div>
                    </div>
                    <div class="prompt-text">{{ prompt.prompt }}</div>
                    <div class="tags">
                        {% for tag in prompt.tags %}
                        <span class="tag">#{{ tag }}</span>
                        {% endfor %}
                    </div>
                    <div class="prompt-footer">
                        <div class="likes" onclick="likePrompt({{ prompt.id }})">
                            <span>❤️</span>
                            <span id="likes-{{ prompt.id }}">{{ prompt.likes }}</span>
                        </div>
                        <div class="action-buttons">
                            <button class="view-btn" onclick="viewPrompt({{ prompt.id }})">👁️ View</button>
                            <button class="copy-btn" onclick="copyPrompt('{{ prompt.prompt|replace("'", "\\'") }}')">📋 Copy</button>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <!-- Add Prompt Modal -->
    <div class="modal" id="addModal">
        <div class="modal-content">
            <span class="close-modal" onclick="closeAddModal()">&times;</span>
            <h2>Add Your Ghibli Prompt</h2>
            <form onsubmit="addPrompt(event)">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" id="promptTitle" required placeholder="e.g., Magical Garden Scene">
                </div>
                <div class="form-group">
                    <label>Ghibli-Style Prompt</label>
                    <textarea id="promptText" required placeholder="Studio Ghibli style, ..."></textarea>
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <select id="promptCategory" required>
                        <option value="Landscape">Landscape</option>
                        <option value="Character">Character</option>
                        <option value="Interior">Interior</option>
                        <option value="Fantasy">Fantasy</option>
                        <option value="Urban">Urban</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Image URL (optional)</label>
                    <input type="url" id="promptImageUrl" placeholder="https://example.com/image.jpg" onchange="previewImage()">
                    <img id="imagePreview" class="image-preview">
                </div>
                <div class="form-group">
                    <label>Tags (comma separated)</label>
                    <input type="text" id="promptTags" placeholder="ghibli, nature, peaceful">
                </div>
                <button type="submit" style="width: 100%;">✨ Add Prompt</button>
            </form>
        </div>
    </div>
    
    <!-- View Prompt Modal -->
    <div class="modal" id="viewModal">
        <div class="modal-content">
            <span class="close-modal" onclick="closeViewModal()">&times;</span>
            <div id="viewModalContent"></div>
        </div>
    </div>
    
    <script>
        let promptsData = {{ prompts|tojson }};
        
        function copyPrompt(text) {
            navigator.clipboard.writeText(text).then(() => {
                const notification = document.createElement('div');
                notification.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #4caf50; color: white; padding: 15px 25px; border-radius: 10px; z-index: 10000; box-shadow: 0 5px 20px rgba(0,0,0,0.3); animation: slideIn 0.3s;';
                notification.innerHTML = '✅ Prompt copied! Paste it in your AI image generator.';
                document.body.appendChild(notification);
                setTimeout(() => notification.remove(), 3000);
            });
        }
        
        function openAddModal() {
            document.getElementById('addModal').style.display = 'flex';
        }
        
        function closeAddModal() {
            document.getElementById('addModal').style.display = 'none';
            document.getElementById('imagePreview').style.display = 'none';
        }
        
        function previewImage() {
            const url = document.getElementById('promptImageUrl').value;
            const preview = document.getElementById('imagePreview');
            if(url) {
                preview.src = url;
                preview.style.display = 'block';
            }
        }
        
        function addPrompt(event) {
            event.preventDefault();
            const title = document.getElementById('promptTitle').value;
            const prompt = document.getElementById('promptText').value;
            const category = document.getElementById('promptCategory').value;
            const imageUrl = document.getElementById('promptImageUrl').value || 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&h=600&fit=crop';
            const tags = document.getElementById('promptTags').value.split(',').map(t => t.trim());
            
            fetch('/api/add_prompt', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, prompt, category, imageUrl, tags})
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    location.reload();
                }
            });
        }
        
        function viewPrompt(id) {
            const prompt = promptsData.find(p => p.id === id);
            if(!prompt) return;
            
            const trendingBadge = prompt.trending ? '<span class="trending-badge">🔥 Trending</span>' : '';
            
            const content = `
                <h2>${prompt.title} ${trendingBadge}</h2>
                <img src="${prompt.image_url}" class="modal-image" alt="${prompt.title}">
                <div style="margin-bottom: 15px;">
                    <span class="category-badge">${prompt.category}</span>
                </div>
                <div class="prompt-display">
                    <strong>📝 Full Prompt (Copy this to your AI generator):</strong>
                    <p id="fullPromptText">${prompt.prompt}</p>
                </div>
                <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #ffc107;">
                    <strong style="color: #856404;">💡 Pro Tip:</strong>
                    <p style="color: #856404; margin-top: 8px;">Copy this prompt and paste it into Midjourney, DALL-E 3, Stable Diffusion, or Leonardo.ai. You can also add specific details like "4K resolution", "trending on ArtStation", or adjust the lighting/mood to your preference!</p>
                </div>
                <div style="margin-bottom: 20px;">
                    ${prompt.tags.map(tag => `<span class="tag">#${tag}</span>`).join(' ')}
                </div>
                <div class="modal-actions">
                    <div style="color: #666; font-size: 1.1em;">❤️ ${prompt.likes} likes</div>
                    <button class="copy-full-btn" onclick="copyPrompt(\`${prompt.prompt.replace(/`/g, '\\`')}\`)">
                        📋 Copy Full Prompt
                    </button>
                </div>
            `;
            
            document.getElementById('viewModalContent').innerHTML = content;
            document.getElementById('viewModal').style.display = 'flex';
        }
        
        function closeViewModal() {
            document.getElementById('viewModal').style.display = 'none';
        }
        
        function likePrompt(id) {
            fetch('/api/like_prompt', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id})
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    document.getElementById('likes-' + id).textContent = data.likes;
                    const prompt = promptsData.find(p => p.id === id);
                    if(prompt) prompt.likes = data.likes;
                    
                    const heart = document.getElementById('likes-' + id).previousElementSibling;
                    heart.style.animation = 'heartbeat 0.3s';
                    setTimeout(() => heart.style.animation = '', 300);
                }
            });
        }
        
        function filterPrompts() {
            const category = document.getElementById('categoryFilter').value;
            const trendingOnly = document.getElementById('trendingOnly').checked;
            const cards = document.querySelectorAll('.prompt-card');
            
            cards.forEach(card => {
                const cardCategory = card.dataset.category;
                const cardTrending = card.dataset.trending === 'True';
                
                let showCard = true;
                
                if(category && cardCategory !== category) {
                    showCard = false;
                }
                
                if(trendingOnly && !cardTrending) {
                    showCard = false;
                }
                
                card.style.display = showCard ? 'block' : 'none';
            });
        }
        
        function searchPrompts() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.prompt-card');
            
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if(text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // Close modals when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        }
        
        // Add heartbeat animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes heartbeat {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.3); }
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, prompts=prompts_db)

@app.route('/api/add_prompt', methods=['POST'])
def add_prompt():
    data = request.json
    new_prompt = {
        'id': len(prompts_db) + 1,
        'title': data['title'],
        'prompt': data['prompt'],
        'category': data['category'],
        'image_url': data['imageUrl'],
        'tags': data['tags'],
        'likes': 0,
        'trending': False,
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    prompts_db.append(new_prompt)
    return jsonify({'success': True})

@app.route('/api/like_prompt', methods=['POST'])
def like_prompt():
    data = request.json
    prompt_id = data['id']
    
    for prompt in prompts_db:
        if prompt['id'] == prompt_id:
            prompt['likes'] += 1
            return jsonify({'success': True, 'likes': prompt['likes']})
    
    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)