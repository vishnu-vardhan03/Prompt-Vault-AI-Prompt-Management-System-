from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage for prompts with images
prompts_db = [
    {
        'id': 1,
        'title': 'Cyberpunk Cityscape',
        'prompt': 'A futuristic cyberpunk city at night, neon lights reflecting on wet streets, flying cars, towering skyscrapers, detailed architecture, cinematic lighting, 8k, ultra realistic',
        'category': 'Landscape',
        'tags': ['cyberpunk', 'city', 'futuristic', 'neon'],
        'likes': 245,
        'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&h=600&fit=crop',
        'created_at': '2025-01-15'
    },
    {
        'id': 2,
        'title': 'Fantasy Dragon Portrait',
        'prompt': 'Majestic dragon portrait, scales glistening, wise eyes, mystical atmosphere, fantasy art style, detailed textures, dramatic lighting, epic composition',
        'category': 'Character',
        'tags': ['dragon', 'fantasy', 'portrait', 'mystical'],
        'likes': 189,
        'image_url': 'https://images.unsplash.com/photo-1618336753974-aae8e04506aa?w=800&h=600&fit=crop',
        'created_at': '2025-01-14'
    },
    {
        'id': 3,
        'title': 'Minimalist Product Shot',
        'prompt': 'Professional product photography, minimalist white background, soft shadows, studio lighting, clean composition, commercial photography, high resolution',
        'category': 'Product',
        'tags': ['minimalist', 'product', 'commercial', 'clean'],
        'likes': 156,
        'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=600&fit=crop',
        'created_at': '2025-01-13'
    },
    {
        'id': 4,
        'title': 'Ethereal Forest Spirit',
        'prompt': 'Mystical forest spirit surrounded by glowing particles, ethereal atmosphere, magical realism, soft bokeh, enchanted woods, fantasy character design, luminescent details',
        'category': 'Character',
        'tags': ['fantasy', 'spirit', 'magical', 'forest'],
        'likes': 312,
        'image_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&h=600&fit=crop',
        'created_at': '2025-01-12'
    },
    {
        'id': 5,
        'title': 'Abstract Liquid Art',
        'prompt': 'Fluid abstract art, swirling colors, liquid paint texture, vibrant gradients, modern digital art, high contrast, dynamic composition, 4k resolution',
        'category': 'Abstract',
        'tags': ['abstract', 'fluid', 'colorful', 'modern'],
        'likes': 198,
        'image_url': 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=800&h=600&fit=crop',
        'created_at': '2025-01-11'
    },
    {
        'id': 6,
        'title': 'Victorian Portrait',
        'prompt': 'Victorian era portrait, elegant clothing, classical painting style, oil painting texture, dramatic lighting, historical accuracy, museum quality, detailed fabric rendering',
        'category': 'Portrait',
        'tags': ['victorian', 'classical', 'elegant', 'historical'],
        'likes': 267,
        'image_url': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800&h=600&fit=crop',
        'created_at': '2025-01-10'
    }
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PromptVault - AI Image Generation Prompts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            border-color: #667eea;
        }
        
        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
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
            background: #667eea;
            color: white;
            border: none;
            font-weight: bold;
        }
        
        button:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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
        }
        
        .prompt-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
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
            background: #667eea;
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
            max-height: 80px;
            overflow: hidden;
            position: relative;
        }
        
        .prompt-text.expanded {
            max-height: none;
        }
        
        .expand-btn {
            color: #667eea;
            cursor: pointer;
            font-size: 0.9em;
            margin-top: 5px;
            display: inline-block;
        }
        
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .tag {
            padding: 5px 10px;
            background: #e8eaf6;
            color: #667eea;
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
            padding: 8px 16px;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s;
        }
        
        .copy-btn {
            background: #4caf50;
        }
        
        .copy-btn:hover {
            background: #45a049;
        }
        
        .view-btn {
            background: #2196F3;
        }
        
        .view-btn:hover {
            background: #0b7dda;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 900px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        .modal-content h2 {
            margin-bottom: 20px;
            color: #333;
        }
        
        .modal-image {
            width: 100%;
            max-height: 400px;
            object-fit: contain;
            border-radius: 10px;
            margin-bottom: 20px;
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
            min-height: 100px;
        }
        
        .close-modal {
            float: right;
            font-size: 28px;
            cursor: pointer;
            color: #999;
            line-height: 1;
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
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            
            .prompts-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎨 PromptVault</h1>
            <p class="tagline">Your Library of AI Image Generation Prompts</p>
        </header>
        
        <div class="controls">
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search prompts...">
                <button onclick="searchPrompts()">Search</button>
            </div>
            <div class="filters">
                <select id="categoryFilter" onchange="filterPrompts()">
                    <option value="">All Categories</option>
                    <option value="Landscape">Landscape</option>
                    <option value="Character">Character</option>
                    <option value="Product">Product</option>
                    <option value="Abstract">Abstract</option>
                    <option value="Portrait">Portrait</option>
                </select>
                <button onclick="openAddModal()">+ Add New Prompt</button>
            </div>
        </div>
        
        <div class="prompts-grid" id="promptsGrid">
            {% for prompt in prompts %}
            <div class="prompt-card" data-category="{{ prompt.category }}">
                <img src="{{ prompt.image_url }}" alt="{{ prompt.title }}" class="prompt-image" onclick="viewPrompt({{ prompt.id }})">
                <div class="prompt-content">
                    <div class="prompt-header">
                        <div class="prompt-title">{{ prompt.title }}</div>
                        <div class="category-badge">{{ prompt.category }}</div>
                    </div>
                    <div class="prompt-text" id="prompt-text-{{ prompt.id }}">{{ prompt.prompt }}</div>
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
                            <button class="view-btn" onclick="viewPrompt({{ prompt.id }})">View</button>
                            <button class="copy-btn" onclick="copyPrompt('{{ prompt.prompt|replace("'", "\\'") }}')">Copy</button>
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
            <h2>Add New Prompt</h2>
            <form onsubmit="addPrompt(event)">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" id="promptTitle" required>
                </div>
                <div class="form-group">
                    <label>Prompt</label>
                    <textarea id="promptText" required></textarea>
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <select id="promptCategory" required>
                        <option value="Landscape">Landscape</option>
                        <option value="Character">Character</option>
                        <option value="Product">Product</option>
                        <option value="Abstract">Abstract</option>
                        <option value="Portrait">Portrait</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Image URL</label>
                    <input type="url" id="promptImageUrl" placeholder="https://example.com/image.jpg" required onchange="previewImage()">
                    <img id="imagePreview" class="image-preview">
                </div>
                <div class="form-group">
                    <label>Tags (comma separated)</label>
                    <input type="text" id="promptTags" placeholder="tag1, tag2, tag3">
                </div>
                <button type="submit" style="width: 100%;">Add Prompt</button>
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
                alert('✅ Prompt copied to clipboard!');
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
            const imageUrl = document.getElementById('promptImageUrl').value;
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
            
            const content = `
                <h2>${prompt.title}</h2>
                <img src="${prompt.image_url}" class="modal-image" alt="${prompt.title}">
                <div style="margin-bottom: 15px;">
                    <span class="category-badge">${prompt.category}</span>
                </div>
                <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <strong style="display: block; margin-bottom: 10px; color: #333;">Prompt:</strong>
                    <p style="line-height: 1.8; color: #555;">${prompt.prompt}</p>
                </div>
                <div style="margin-bottom: 15px;">
                    ${prompt.tags.map(tag => `<span class="tag">#${tag}</span>`).join(' ')}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 15px; border-top: 1px solid #e0e0e0;">
                    <div style="color: #666;">❤️ ${prompt.likes} likes</div>
                    <button class="copy-btn" onclick="copyPrompt('${prompt.prompt.replace(/'/g, "\\'")}')">Copy Prompt</button>
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
                }
            });
        }
        
        function filterPrompts() {
            const category = document.getElementById('categoryFilter').value;
            const cards = document.querySelectorAll('.prompt-card');
            
            cards.forEach(card => {
                if(!category || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
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
