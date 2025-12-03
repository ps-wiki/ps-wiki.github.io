# PS-Wiki Term Editor

An online editor for creating and editing PS-Wiki terms with real-time preview and validation.

## Features

- **User-Friendly Interface**: Form-based input for all term metadata and content
- **Real-Time Preview**: See generated Markdown and JSON as you type
- **Validation**: Built-in validation against the PS-Wiki term schema
- **Templates**: Pre-built templates for common term types (Definition, Concept, Technical)
- **Load Existing Terms**: Import existing terms for editing
- **Download**: Generate and download both Markdown and JSON files
- **Modern Design**: Premium dark theme with smooth animations

## Getting Started

### Accessing the Editor

1. Open `index.html` in a modern web browser (Chrome, Firefox, Safari, or Edge)
2. Wait for PyScript to initialize (this may take a few seconds on first load)
3. Start creating your term!

### Creating a New Term

1. **Basic Information**:
   - Enter the term title (required)
   - Add a short description (required)
   - The term ID will be auto-generated from the title (you can customize it)
   - Set the language (default: `en`)
   - Set the version (default: `1.0.0`)

2. **Tags & Related Terms**:
   - Add comma-separated tags for categorization
   - Add related term IDs (optional)
   - Add aliases/alternative names (optional)

3. **Authors**:
   - Click "+ Add Author" to add author information
   - Enter author name (required) and URL (optional)
   - You can add multiple authors

4. **Content Sections**:
   - Click "+ Add Section" to create content sections
   - Each section has:
     - **Title**: Section heading
     - **Type**: Choose from Definition, Note, Example, Equation, etc.
     - **Body**: Markdown content (use `>` for blockquotes in definitions)
     - **Source Keys**: Citation keys (optional, comma-separated)
     - **Page Reference**: Page number or range (optional)

5. **Preview & Validate**:
   - Switch between Markdown and JSON preview tabs
   - Click "✓ Validate" to check for errors
   - Fix any validation errors before downloading

6. **Download**:
   - Click "⬇ Download Markdown" to get the `.md` file
   - Click "⬇ Download JSON" to get the `.json` file

### Using Templates

1. Click "📋 Load Template"
2. Choose from:
   - **Definition Term**: Standard term with multiple definitions
   - **Concept Term**: Explanatory term with notes and examples
   - **Technical Term**: Technical term with equations and derivations
3. Customize the template content as needed

### Loading Existing Terms

1. Click "📂 Load Existing Term"
2. Paste the JSON content of an existing term
3. Click "Load Term"
4. The form will be populated with the term data
5. Make your edits and download the updated files

## Field Descriptions

### Required Fields

- **Title**: The main title of the term
- **Description**: Short description (used in search and summaries)
- **Language**: BCP-47 language tag (e.g., `en`, `en-GB`)
- **Version**: Semantic version (e.g., `1.0.0`)
- **Authors**: At least one author with a name
- **Content Sections**: At least one section with title and body

### Optional Fields

- **Term ID**: Auto-generated from title, but can be customized
- **Tags**: Topic tags for search and categorization
- **Related**: IDs of related terms
- **Aliases**: Alternative names or abbreviations
- **Source Keys**: Citation keys for bibliography references
- **Page Reference**: Page numbers for citations

## Section Types

- **definition**: Formal definitions (typically use blockquotes with `>`)
- **note**: Explanatory notes and general content
- **example**: Practical examples and use cases
- **equation**: Mathematical equations and formulas
- **derivation**: Mathematical derivations and proofs
- **figure-block**: Sections with figures and images
- **table**: Tables and structured data
- **reference**: References and citations

## Markdown Tips

- Use `>` at the start of a line for blockquotes (common in definitions)
- Use `**bold**` for bold text
- Use `*italic*` for italic text
- Use `$$...$$` for LaTeX equations
- Use `\`code\`` for inline code
- Use triple backticks for code blocks

## Adding Files to Repository

After downloading the generated files:

1. **Markdown File**: Place in `_wiki/` directory
   ```bash
   mv ~/Downloads/term-id.md _wiki/
   ```

2. **JSON File**: Place in `database/json/` directory
   ```bash
   mv ~/Downloads/term-id.json database/json/
   ```

3. **Validate** (optional but recommended):
   ```bash
   python database/pyscripts/validate.py database/json/term-id.json
   ```

4. **Process** (optional, to ensure consistency):
   ```bash
   python database/pyscripts/process.py --terms term-id
   ```

5. **Commit and push** to GitHub:
   ```bash
   git add _wiki/term-id.md database/json/term-id.json
   git commit -m "Add new term: term-id"
   git push
   ```

## Browser Compatibility

The editor works best in modern browsers with WebAssembly support:

- ✅ Chrome/Edge (Chromium) 90+
- ✅ Firefox 89+
- ✅ Safari 15+

**Note**: The first load may take 10-20 seconds as PyScript downloads and initializes the Python runtime.

## Troubleshooting

### PyScript Not Loading

- Check browser console for errors
- Ensure you have a stable internet connection (PyScript loads from CDN)
- Try refreshing the page
- Clear browser cache and reload

### Validation Errors

- Read the error messages carefully
- Ensure all required fields are filled
- Check that term ID is in kebab-case (lowercase with hyphens)
- Verify language code is valid BCP-47 format
- Ensure at least one author and one section are present

### Download Not Working

- Check if pop-ups are blocked in your browser
- Try a different browser
- Ensure JavaScript is enabled

## Technical Details

### Architecture

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Python Runtime**: PyScript/Pyodide (Python in WebAssembly)
- **Processing**: Browser-compatible versions of `md2json` and `json2md`
- **Validation**: Basic schema validation (subset of full JSON Schema)

### Files

- `index.html`: Main editor interface
- `style.css`: Premium styling and theme
- `app.js`: UI logic and event handling
- `editor.py`: PyScript logic for term processing
- `term_processor.py`: Core conversion and validation functions

## License

This editor is part of the PS-Wiki project and follows the same license as the main repository.

## Support

For issues or questions:
1. Check this README for common solutions
2. Review the [PS-Wiki documentation](https://ps-wiki.github.io)
3. Open an issue on the GitHub repository
