import os
import re

def wrap_sections(content):
    # Mapping of sections to classes
    sections = {
        'Section A': 'log-entry',
        'Section B': 'rigorous-theory',
        'Section C': 'step-walker',
        'Section D': 'protocol-box'
    }
    
    # Split content by headers starting with Section A-D (either ### or ####)
    parts = re.split(r'((?:###|####) Section [A-D]:.*?\n)', content)
    
    new_content = parts[0]
    i = 1
    while i < len(parts):
        header = parts[i]
        body = parts[i+1]
        
        # Find which section it is
        section_key = None
        for key in sections:
            if key in header:
                section_key = key
                break
        
        if section_key:
            # Find where the section ends (any header of same or higher level or Section A-D)
            # Find the level of current header
            header_level = len(re.match(r'#+', header).group())
            
            # Stop at any header with level <= header_level OR any Section header
            # To be simple, we stop at any line starting with #
            match = re.search(r'(?m)^#+ ', body)
            
            # But wait, we want to include the body until the NEXT Section or NEXT higher level header
            # If we stop at the next #, we might stop too early if there's an h5 or h6 inside
            
            # Actually, the most reliable way is to look at the next parts in our split
            # The next part parts[i+2] will be the next header match.
            
            # Let's see if the body contains headers that should be OUTSIDE the div
            # e.g. if header is #### and body contains ###
            match = re.search(r'(?m)^#{1,3} ', body) if header_level == 4 else re.search(r'(?m)^#{1,2} ', body)
            
            if match:
                end_pos = match.start()
                section_body = body[:end_pos]
                rest = body[end_pos:]
                new_content += f'<div class="{sections[section_key]}">\n\n{header}{section_body}\n</div>\n\n{rest}'
            else:
                new_content += f'<div class="{sections[section_key]}">\n\n{header}{body}\n</div>\n\n'
        else:
            new_content += header + body
            
        i += 2
        
    return new_content

directory = 'src/content/modules'
for filename in os.listdir(directory):
    if filename.endswith('.md'):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We can run it multiple times, but let's clear existing wraps first to avoid mess
        content = re.sub(r'<div class="(?:log-entry|rigorous-theory|step-walker|protocol-box)">\n\n', '', content)
        content = re.sub(r'\n</div>\n\n', '\n', content)
            
        updated_content = wrap_sections(content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Processed {filename}")
