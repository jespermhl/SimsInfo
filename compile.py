import os
import shutil
import markdown 
from bs4 import BeautifulSoup

# Define paths
SRC_DIR = 'src'  # Source directory
DIST_DIR = 'dist'  # Output directory
CONTENT_DIR = os.path.join(SRC_DIR, 'content')  # Content directory
TEMPLATE_DIR = os.path.join(SRC_DIR, 'structure', 'templates')  # Template directory
ASSETS_DIR = os.path.join(SRC_DIR, 'assets')  # Assets directory

def markdown_to_html(markdown_text):  # Convert Markdown to HTML
    md = markdown.Markdown(extensions=['meta'])
    html = md.convert(markdown_text)
    return html

def render_template(template_name, context):
    # Read the template file
    with open(os.path.join(TEMPLATE_DIR, template_name), 'r') as file:
        template = file.read()
    
    # Handle template inheritance
    if '{% extends ' in template:
        base_template_name = extract_base_template(template)
        base_template_path = os.path.join(TEMPLATE_DIR, base_template_name)
        with open(base_template_path, 'r') as file:
            base_template = file.read()
        
        # Extract blocks from the base template
        block_content = extract_block_content(base_template, template)
        template = base_template.replace('{{ content }}', block_content)
    
    # Replace placeholders with context values
    for key, value in context.items():
        placeholder = f"{{{{ {key} }}}}"
        template = template.replace(placeholder, value)
    
    return template

def extract_base_template(template):
    start = template.find('{% extends "')
    start += len('{% extends "')
    end = template.find('" %}')
    return template[start:end]

def extract_block_content(base_template, template):
    block_start = template.find('{% block content %}')
    block_end = template.find('{% endblock %}')
    block_content = template[block_start + len('{% block content %}') : block_end]
    return block_content

def save_page(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # Ensure the directory exists
    with open(path, 'w') as file:
        file.write(content)

def copy_assets():
    if os.path.exists(ASSETS_DIR):
        destination = os.path.join(DIST_DIR, 'assets')
        shutil.copytree(ASSETS_DIR, destination, dirs_exist_ok=True)

def enhance_external_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('http'):
            a['class'] = a.get('class', []) + ['icon-link']
            icon = soup.new_tag('i', **{'class': 'bi bi-box-arrow-up-right'})
            a.append(icon)
    return str(soup)

def extract_snippet(html_content, num_words=20):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove heading tags
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        heading.decompose()
    
    text = soup.get_text()
    words = text.split()
    snippet = ' '.join(words[:num_words])
    return snippet + ('...' if len(words) > num_words else '')

def generate_pages():
    pages = {}
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # Read Markdown file
                with open(file_path, 'r') as f:
                    markdown_text = f.read()
                
                # Convert Markdown to HTML
                html_content = markdown_to_html(markdown_text)
                
                # Enhance external links
                html_content = enhance_external_links(html_content)
                
                # Extract metadata from Markdown
                lines = markdown_text.split('\n')
                metadata = {}
                content = []
                
                # Identify the beginning and end of the metadata section
                metadata_start = None
                metadata_end = None
                
                for i, line in enumerate(lines):
                    if line.strip() == '---':
                        if metadata_start is None:
                            metadata_start = i
                        elif metadata_end is None:
                            metadata_end = i
                            break
                
                # Parse the metadata section if found
                if metadata_start is not None and metadata_end is not None:
                    for line in lines[metadata_start + 1:metadata_end]:
                        if ': ' in line:
                            key, value = line.strip().split(': ', 1)
                            metadata[key] = value
                
                # Extract content section
                if metadata_end is not None:
                    content = lines[metadata_end + 1:]
                
                # Determine template based on type
                template_name = 'page.html'
                
                # Create page context
                context = {
                    'title': metadata.get('title', 'Untitled'),
                    'meta-title': metadata.get('meta-title', metadata.get('title', 'No Meta Title')),
                    'meta-description': metadata.get('meta-description', 'No Meta Description'),
                    'content': html_content,
                    'author': metadata.get('author', 'Unknown'),
                    'image': metadata.get('image', '')  # Add image metadata
                }
                
                # Render template
                html_page = render_template(template_name, context)
                
                # Save HTML page
                relative_path = os.path.relpath(root, CONTENT_DIR)
                output_dir = os.path.join(DIST_DIR, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                save_page(html_page, os.path.join(output_dir, file.replace('.md', '.html')))
                
                # Collect page info for homepage
                pages[file] = {
                    'title': metadata.get('title', 'Untitled'),
                    'date': metadata.get('date', 'Unknown'),
                    'path': os.path.join(relative_path, file.replace('.md', '.html')),
                    'author': metadata.get('author', 'Unknown'),
                    'image': metadata.get('image', '')  # Add image info
                }

    return pages

def generate_home_page(pages):
    """
    Generates the homepage HTML with Bootstrap cards for updates, SDX Drops, challenges, and packs.
    """
    def generate_card(title, date, path, author, snippet, image):
        image_html = f'<img src="{image}" class="card-img-top" alt="{title}">' if image else ''
        return f"""
        <div class="card home-card" style="min-width: 300px; margin: 10px;">
            {image_html}
            <div class="card-body">
                <h5 class="card-title">{title}</h5>
                <h6 class="card-subtitle mb-2 text-muted">Posted on {date} by {author}</h6>
                <p class="card-text">{snippet}</p>
                <a href="{path}" class="btn btn-primary">Read more</a>
            </div>
        </div>
        """

    homepage_content = """
    <h1>Sul sul, welcome to the Sims Info Hub!</h1>
    <p>Welcome to my little Sims information site / wiki! Have fun browsing!</p>
    """

    types = {
        'updates': 'Updates',
        'sdx-drops': 'SDX Drops',
        'challenges': 'Challenges',
        'packs/ep': 'Expansion Packs',
        'packs/gp': 'Game Packs',
        'packs/sp': 'Stuff Packs',
        'packs/k': 'Kits'
    }

    for path_key, section_title in types.items():
        homepage_content += f"<h2>{section_title}</h2><div class='card-container mb-3' style='display: flex; flex-wrap: wrap;'>"
        filtered_pages = [info for page, info in sorted(pages.items(), key=lambda x: x[1]['date'], reverse=True) if path_key in info['path']]
        
        for info in filtered_pages[:3]:
            file_path = os.path.join(CONTENT_DIR, info['path'].replace('.html', '.md'))
            with open(file_path, 'r') as f:
                markdown_text = f.read()
            html_content = markdown_to_html(markdown_text)
            snippet = extract_snippet(html_content)
            
            homepage_content += generate_card(info['title'], info['date'], info['path'], info['author'], snippet, info['image'])
        
        if len(filtered_pages) > 3:
            more_page_path = os.path.join('more', f"{path_key}.html")
            homepage_content += f"""
            <div class="card" style="margin: 10px;">
                <div class="card-body d-flex align-items-center justify-content-center">
                    <a href='{more_page_path}' class='btn btn-secondary mx-4'>More {section_title}</a>
                </div>
            </div>"""

        homepage_content += "</div>"

    context = {
        'title': 'Home',
        'meta-title': 'Welcome to the Sims Info Hub',
        'meta-description': 'The latest updates, packs, and more for The Sims 4.',
        'content': homepage_content
    }
    
    homepage_html = render_template('base.html', context)
    save_page(homepage_html, os.path.join(DIST_DIR, 'index.html'))
    
    generate_more_pages(pages, types)

def generate_more_pages(pages, types):
    """
    Generates the 'More' pages for each type, sorted by slug (title).
    """
    def generate_list_item(title, date, path, author, snippet):
        return f"""
        <div class="list-group-item">
            <h5 class="mb-1"><a href="{path}">{title}</a></h5>
            <small class="text-muted">Posted on {date} by {author}</small>
            <p class="mb-1">{snippet}</p>
        </div>
        """

    for path_key, section_title in types.items():
        more_page_content = f"<h1>{section_title}</h1><div class='list-group mb-3'>"
        
        # Filter and sort pages
        filtered_pages = [info for page, info in sorted(pages.items(), key=lambda x: x[1]['date'], reverse=True) if path_key in info['path']]
        sorted_pages = sorted(filtered_pages, reverse=True, key=lambda x: os.path.splitext(os.path.basename(x['path']))[0].lower())  # Sort by file name (slug)
        
        for info in sorted_pages:
            file_path = os.path.join(CONTENT_DIR, info['path'].replace('.html', '.md'))
            with open(file_path, 'r') as f:
                markdown_text = f.read()
            html_content = markdown_to_html(markdown_text)
            snippet = extract_snippet(html_content)
            
            # Fix the path to link correctly
            correct_path = os.path.join('/', info['path'])
            more_page_content += generate_list_item(info['title'], info['date'], correct_path, info['author'], snippet)
        
        more_page_content += "</div>"
        
        context = {
            'title': section_title,
            'meta-title': f"More {section_title}",
            'meta-description': f"All items in the {section_title} category.",
            'content': more_page_content
        }
        
        more_page_html = render_template('base.html', context)
        output_dir = os.path.join(DIST_DIR, 'more')
        os.makedirs(output_dir, exist_ok=True)
        save_page(more_page_html, os.path.join(output_dir, f"{path_key}.html"))

def main():
    """
    Main function to generate all content pages, static pages, and the home page.
    """
    # Generate all content pages
    pages = generate_pages()

    # Copy assets
    copy_assets()

    # Generate the home page
    generate_home_page(pages)

if __name__ == '__main__':
    main()
