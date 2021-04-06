# Novel scraper
The main objective of this project is to convert web based novel into `.epub` format for easier consumption. 
This tool is intended for personal consumption or educational purposes only. Please do not misuse it. 

## First steps
Before you start using this tool, there are several things to take note. 
1. This will only work for those web novels which does **not** require a login. 
2. The url of the novel must be consistent across all chapters.

## Using the tool 
1. Determine the base URL of the novel.
    > eg. https://www.example.come/novel_base_url/chapter-
2. Determine the first and last chapters of the novel.  
3. Determine the ID of the HTML tag which contain the content of the novel
    > eg. "chapter-content"
4. Name of the novel (optional)
5. Just insert the designated parameters in the lines with `# Change me`

Run the python file and wait for completion. 