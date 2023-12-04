import re

programming_languages_lowercase = {
    'python': '.py',
    'javascript': '.js',
    'java': '.java',
    'c++': '.cpp',
    'c': '.c',
    'html': '.html',
    'css': '.css',
    'ruby': '.rb',
    'swift': '.swift',
    'php': '.php',
    'sql': '.sql',
    'typescript': '.ts',
    'shell scripting': '.sh',
    'go': '.go',
    'rust': '.rs',
    'kotlin': '.kt',
    'objective-c': '.m',
    'markdown': '.md',
    'perl': '.pl',
    'scala': '.scala',
    'dart': '.dart',
    'yaml': '.yaml',
    'xml': '.xml',
    'batch script': '.bat',
    'powershell': '.ps1',
    'r': '.r',
    'vue.js': '.vue',
    'jupyter notebooks': '.ipynb',
}

def flnm(ip):
    def generate_filename(sentence):
        words = re.findall(r'\b\w+\b', sentence.lower())
        language_found = set(programming_languages_lowercase.keys()).intersection(words)
        
        if language_found:
            primary_language = language_found.pop()
            extension = programming_languages_lowercase[primary_language]
            filename = "sample_code" + extension
        else:
            filename = "sample_code.txt"
        
        return filename

    def save_file(content, filename):
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' saved successfully.")
    
    generated_filename = generate_filename(ip)
    save_file("# Your file content here.", generated_filename)
    return generated_filename
