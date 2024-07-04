# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import os
import requests
from bs4 import BeautifulSoup

def get_markdown(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the title of the page
    title = soup.find('title').text

    # Get all the headings on the page
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Create a dictionary to store the heading level and its content
    heading_dict = {}
    for heading in headings:
        level = int(heading.name[1])
        content = heading.text.strip()
        if content not in heading_dict or level < heading_dict[content]:
            heading_dict[content] = level

    # Get all the paragraphs on the page
    paragraphs = soup.find_all('p')

    # Create a list to store the markdown text
    markdown_list = []

    # Add the title and two empty lines to the markdown list
    markdown_list.append(f'# {title}')
    markdown_list.append('')
    markdown_list.append('')

    # Loop through the paragraphs and add them to the markdown list
    for paragraph in paragraphs:
        text = paragraph.text.strip()
        if text:
            # Check if the current paragraph is a heading
            if text in heading_dict:
                level = heading_dict[text]
                markdown_list.append(f'{"#" * level} {text}')
            else:
                markdown_list.append(text)

            # Add an empty line after each paragraph
            markdown_list.append('')

    # Join the markdown list into a single string and return it
    markdown_text = '\n'.join(markdown_list)
    return markdown_text

def save_markdown(markdown_text, filename):
    # Check if the directory exists, create it if it doesn't
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the markdown text to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_text)

if __name__ == '__main__':
    url = input('Enter the URL of the Wikipedia page: ')
    filename = input('Enter the path and filename to save the Markdown file: ')
    markdown_text = get_markdown(url)
    save_markdown(markdown_text, filename)
    print('Markdown file saved successfully.')
