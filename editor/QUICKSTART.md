# Quick Start Guide - PS-Wiki Term Editor

## 🚀 Getting Started in 3 Steps

### Step 1: Open the Editor

Open this file in your web browser:
```
file:///Users/jinningwang/work/pswiki/editor/index.html
```

Or simply double-click `index.html` in the `/editor/` folder.

**⏱️ First Load**: PyScript will take 10-20 seconds to initialize. You'll see the interface appear when ready.

---

### Step 2: Create Your Term

#### Option A: Use a Template (Recommended for First Time)

1. Click **"📋 Load Template"**
2. Choose a template type:
   - **Definition Term**: For standard definitions from authoritative sources
   - **Concept Term**: For explanatory content with examples
   - **Technical Term**: For equations and mathematical content
3. Customize the pre-filled content
4. Click **"✓ Validate"** to check for errors
5. Click **"⬇ Download Markdown"** and **"⬇ Download JSON"**

#### Option B: Start from Scratch

1. Fill in **Basic Information**:
   - Title (e.g., "Frequency Stability")
   - Description (short summary)
   - Language: `en` (default)
   - Version: `1.0.0` (default)

2. Add **Tags** (comma-separated):
   - Example: `stability, frequency, control`

3. Add **Authors**:
   - Click "+ Add Author"
   - Enter name and optional URL

4. Add **Content Sections**:
   - Click "+ Add Section"
   - Enter section title
   - Choose section type (Definition, Note, Example, etc.)
   - Write content in Markdown
   - Add source keys if citing references

5. **Preview** your work:
   - Switch between Markdown and JSON tabs
   - Check the generated output

6. **Validate** before downloading:
   - Click "✓ Validate"
   - Fix any errors shown

7. **Download** both files:
   - Click "⬇ Download Markdown"
   - Click "⬇ Download JSON"

---

### Step 3: Add to Repository

Move the downloaded files to the correct locations:

```bash
# Navigate to your ps-wiki directory
cd /Users/jinningwang/work/pswiki

# Move the markdown file
mv ~/Downloads/your-term-id.md _wiki/

# Move the JSON file
mv ~/Downloads/your-term-id.json database/json/

# Optional: Validate the JSON
python database/pyscripts/validate.py database/json/your-term-id.json

# Optional: Process to ensure consistency
python database/pyscripts/process.py --terms your-term-id

# Commit and push
git add _wiki/your-term-id.md database/json/your-term-id.json
git commit -m "Add new term: your-term-id"
git push
```

---

## 💡 Pro Tips

### Writing Definitions
Use `>` for blockquotes (standard for definitions):
```markdown
> This is the official definition from the standard.
```

### Adding Citations
In the "Source Keys" field, enter citation keys separated by commas:
```
nerc2024glossary, ieee2020standard
```

### Multiple Sections
Click "+ Add Section" multiple times to add:
- Multiple definitions from different sources
- Examples after definitions
- Technical details
- Related concepts

### Loading Existing Terms
1. Find the JSON file in `database/json/`
2. Copy its contents
3. Click "📂 Load Existing Term"
4. Paste and click "Load Term"
5. Edit and re-download

---

## ✅ Checklist Before Download

- [ ] Title is descriptive and clear
- [ ] Description is concise (1-2 sentences)
- [ ] At least one author is added
- [ ] At least one content section is added
- [ ] Tags are relevant and lowercase
- [ ] Validation shows no errors
- [ ] Preview looks correct

---

## 🔧 Troubleshooting

**PyScript not loading?**
- Wait 20-30 seconds on first load
- Check browser console for errors (F12)
- Try refreshing the page
- Ensure internet connection (PyScript loads from CDN)

**Download not working?**
- Check if browser is blocking downloads
- Try a different browser
- Check browser console for errors

**Validation errors?**
- Read error messages carefully
- Ensure all required fields are filled
- Check term ID is kebab-case (lowercase-with-hyphens)
- Verify at least one author and section exist

---

## 📚 Need More Help?

- **Full Documentation**: See [README.md](file:///Users/jinningwang/work/pswiki/editor/README.md)
- **Walkthrough**: See [walkthrough.md](file:///Users/jinningwang/.gemini/antigravity/brain/0cd73e05-f394-45d7-8f81-f0d329ebbd6d/walkthrough.md)
- **Test Example**: See [test_output.md](file:///Users/jinningwang/work/pswiki/editor/test_output.md) and [test_output.json](file:///Users/jinningwang/work/pswiki/editor/test_output.json)

---

**Happy Editing! 🎉**
