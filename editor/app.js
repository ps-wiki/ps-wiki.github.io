// JavaScript for PS-Wiki Term Editor
// Handles UI interactions, dynamic form elements, and template loading

// Initialize the editor
document.addEventListener('DOMContentLoaded', () => {
    initializeEditor();
    setupEventListeners();
    addInitialAuthor();
    addInitialSection();
});

function initializeEditor() {
    // Auto-generate term ID when title changes
    const titleInput = document.getElementById('title');
    titleInput.addEventListener('input', () => {
        if (window.pyGenerateTermId) {
            window.pyGenerateTermId();
        }
    });
    
    // Update preview on any input change
    document.querySelectorAll('input, textarea, select').forEach(element => {
        element.addEventListener('input', debounce(updatePreview, 500));
    });
}

function setupEventListeners() {
    // Toolbar buttons
    document.getElementById('loadExistingBtn').addEventListener('click', showLoadModal);
    document.getElementById('loadTemplateBtn').addEventListener('click', showTemplateModal);
    document.getElementById('validateBtn').addEventListener('click', validateTerm);
    document.getElementById('downloadMdBtn').addEventListener('click', downloadMarkdown);
    document.getElementById('downloadJsonBtn').addEventListener('click', downloadJson);
    
    // Add buttons
    document.getElementById('addAuthorBtn').addEventListener('click', () => addAuthor());
    document.getElementById('addSectionBtn').addEventListener('click', () => addSection());
    
    // Preview tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });
    
    // Modal close buttons
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', closeModals);
    });
    
    // Load JSON button
    document.getElementById('loadJsonBtn').addEventListener('click', loadJsonFromInput);
    
    // Template cards
    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', (e) => {
            const template = e.currentTarget.dataset.template;
            loadTemplate(template);
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModals();
        }
    });
}

// Author management
function addAuthor(name = '', url = '') {
    const container = document.getElementById('authorsContainer');
    const authorDiv = document.createElement('div');
    authorDiv.className = 'author-entry';
    authorDiv.innerHTML = `
        <div class="form-row">
            <div class="form-group">
                <input type="text" class="author-name" placeholder="Author Name" value="${name}">
            </div>
            <div class="form-group">
                <input type="url" class="author-url" placeholder="Author URL (optional)" value="${url}">
            </div>
            <button class="btn btn-danger btn-small remove-btn" onclick="removeAuthor(this)">×</button>
        </div>
    `;
    container.appendChild(authorDiv);
    
    // Add event listeners for preview update
    authorDiv.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', debounce(updatePreview, 500));
    });
}

function addInitialAuthor() {
    addAuthor();
}

function removeAuthor(btn) {
    btn.closest('.author-entry').remove();
    updatePreview();
}

// Section management
function addSection(title = '', type = 'definition', body = '', sources = '', page = '') {
    const container = document.getElementById('sectionsContainer');
    const sectionDiv = document.createElement('div');
    sectionDiv.className = 'section-entry';
    sectionDiv.innerHTML = `
        <div class="section-header">
            <h4>Section ${container.children.length + 1}</h4>
            <button class="btn btn-danger btn-small remove-btn" onclick="removeSection(this)">×</button>
        </div>
        <div class="form-group">
            <label>Section Title</label>
            <input type="text" class="section-title" placeholder="e.g., Definition by NERC" value="${title}">
        </div>
        <div class="form-group">
            <label>Section Type</label>
            <select class="section-type">
                <option value="definition" ${type === 'definition' ? 'selected' : ''}>Definition</option>
                <option value="note" ${type === 'note' ? 'selected' : ''}>Note</option>
                <option value="example" ${type === 'example' ? 'selected' : ''}>Example</option>
                <option value="equation" ${type === 'equation' ? 'selected' : ''}>Equation</option>
                <option value="derivation" ${type === 'derivation' ? 'selected' : ''}>Derivation</option>
                <option value="figure-block" ${type === 'figure-block' ? 'selected' : ''}>Figure Block</option>
                <option value="table" ${type === 'table' ? 'selected' : ''}>Table</option>
                <option value="reference" ${type === 'reference' ? 'selected' : ''}>Reference</option>
            </select>
        </div>
        <div class="form-group">
            <label>Body (Markdown)</label>
            <textarea class="section-body" rows="6" placeholder="Enter section content in Markdown format...">${body}</textarea>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Source Keys (Optional)</label>
                <input type="text" class="section-sources" placeholder="Comma-separated citation keys" value="${sources}">
                <small>e.g., nerc2024glossary, ieee2020standard</small>
            </div>
            <div class="form-group">
                <label>Page Reference (Optional)</label>
                <input type="text" class="section-page" placeholder="e.g., p48, pp. 123-145" value="${page}">
            </div>
        </div>
    `;
    container.appendChild(sectionDiv);
    
    // Add event listeners for preview update
    sectionDiv.querySelectorAll('input, textarea, select').forEach(input => {
        input.addEventListener('input', debounce(updatePreview, 500));
    });
}

function addInitialSection() {
    addSection('', 'definition', '> Enter your definition here...');
}

function removeSection(btn) {
    btn.closest('.section-entry').remove();
    // Renumber sections
    document.querySelectorAll('.section-entry').forEach((section, idx) => {
        section.querySelector('h4').textContent = `Section ${idx + 1}`;
    });
    updatePreview();
}

// Preview management
function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    document.querySelectorAll('.preview-code').forEach(pre => {
        pre.classList.toggle('active', pre.id === `${tab}Preview`);
    });
}

function updatePreview() {
    if (window.pyUpdatePreview) {
        window.pyUpdatePreview();
    }
}

function validateTerm() {
    if (window.pyValidateTerm) {
        window.pyValidateTerm();
    }
}

function downloadMarkdown() {
    if (window.pyDownloadMarkdown) {
        window.pyDownloadMarkdown();
    }
}

function downloadJson() {
    if (window.pyDownloadJson) {
        window.pyDownloadJson();
    }
}

// Modal management
function showLoadModal() {
    document.getElementById('loadModal').style.display = 'flex';
}

function showTemplateModal() {
    document.getElementById('templateModal').style.display = 'flex';
}

function closeModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

function loadJsonFromInput() {
    const jsonInput = document.getElementById('loadJsonInput').value;
    if (jsonInput.trim() && window.pyLoadTermFromJson) {
        window.pyLoadTermFromJson(jsonInput);
    } else {
        alert('Please paste valid JSON content');
    }
}

// Template loading
function loadTemplate(templateName) {
    const templates = {
        definition: {
            title: 'Sample Definition Term',
            description: 'A term with multiple definitions from various authoritative sources',
            tags: 'definition, standard, glossary',
            related: '',
            authors: [{ name: 'Your Name', url: '' }],
            sections: [
                {
                    title: 'Definition by NERC',
                    type: 'definition',
                    body: '> The ability of an electric system to maintain a state of equilibrium during normal and abnormal conditions or disturbances.',
                    sources: 'nerc2024glossary',
                    page: ''
                },
                {
                    title: 'Definition by IEEE',
                    type: 'definition',
                    body: '> A technical definition from IEEE standards...',
                    sources: 'ieee2020standard',
                    page: 'p. 42'
                }
            ]
        },
        concept: {
            title: 'Sample Concept Term',
            description: 'An explanatory term with notes and practical examples',
            tags: 'concept, explanation, example',
            related: '',
            authors: [{ name: 'Your Name', url: '' }],
            sections: [
                {
                    title: 'Overview',
                    type: 'note',
                    body: 'This section provides an overview of the concept...',
                    sources: '',
                    page: ''
                },
                {
                    title: 'Practical Example',
                    type: 'example',
                    body: 'Here is a practical example demonstrating the concept...',
                    sources: '',
                    page: ''
                }
            ]
        },
        technical: {
            title: 'Sample Technical Term',
            description: 'A technical term with equations and mathematical derivations',
            tags: 'technical, equation, mathematics',
            related: '',
            authors: [{ name: 'Your Name', url: '' }],
            sections: [
                {
                    title: 'Mathematical Definition',
                    type: 'equation',
                    body: 'The fundamental equation is:\n\n$$\nf(x) = \\int_0^\\infty e^{-x^2} dx\n$$',
                    sources: '',
                    page: ''
                },
                {
                    title: 'Derivation',
                    type: 'derivation',
                    body: 'Starting from the basic principles...',
                    sources: '',
                    page: ''
                }
            ]
        }
    };
    
    const template = templates[templateName];
    if (!template) return;
    
    // Load template data
    document.getElementById('title').value = template.title;
    document.getElementById('description').value = template.description;
    document.getElementById('tags').value = template.tags;
    document.getElementById('related').value = template.related;
    
    // Clear and load authors
    document.getElementById('authorsContainer').innerHTML = '';
    template.authors.forEach(author => addAuthor(author.name, author.url));
    
    // Clear and load sections
    document.getElementById('sectionsContainer').innerHTML = '';
    template.sections.forEach(section => {
        addSection(section.title, section.type, section.body, section.sources, section.page);
    });
    
    // Generate term ID and update preview
    if (window.pyGenerateTermId) {
        window.pyGenerateTermId();
    }
    updatePreview();
    
    closeModals();
}

// Utility: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for PyScript
window.addAuthor = addAuthor;
window.addSection = addSection;
window.removeAuthor = removeAuthor;
window.removeSection = removeSection;
