// Prevent browser autofill extensions from processing inputs with dictionary IDs
// This addresses the issue where extensions try to use stringified JSON IDs as CSS selectors

// Override querySelectorAll to catch and prevent errors from autofill extensions
(function() {
    'use strict';
    
    // Helper function to check if selector contains problematic patterns
    function isProblematicSelector(selector) {
        if (!selector || typeof selector !== 'string') return false;
        // Check for JSON-like patterns in attribute selectors
        return selector.includes('{"') || 
               selector.includes('"}') ||
               selector.includes("{'") ||
               /\[for=["'][{]/.test(selector) ||
               /\[id=["'][{]/.test(selector);
    }
    
    // Create empty NodeList helper
    function emptyNodeList() {
        return document.createDocumentFragment().querySelectorAll('*');
    }
    
    // Wrap querySelectorAll to handle errors gracefully
    function wrapQuerySelectorAll(originalFn) {
        return function(selector) {
            try {
                if (isProblematicSelector(selector)) {
                    return emptyNodeList();
                }
                if (typeof originalFn !== 'function') {
                    return emptyNodeList();
                }
                return originalFn.call(this, selector);
            } catch (e) {
                if (e instanceof DOMException && e.name === 'SyntaxError') {
                    return emptyNodeList();
                }
                return emptyNodeList();
            }
        };
    }
    
    // Wrap querySelector to handle errors gracefully
    function wrapQuerySelector(originalFn) {
        return function(selector) {
            try {
                if (isProblematicSelector(selector)) {
                    return null;
                }
                if (typeof originalFn !== 'function') {
                    return null;
                }
                return originalFn.call(this, selector);
            } catch (e) {
                if (e instanceof DOMException && e.name === 'SyntaxError') {
                    return null;
                }
                return null;
            }
        };
    }
    
    // Override on Document.prototype
    Document.prototype.querySelectorAll = wrapQuerySelectorAll(Document.prototype.querySelectorAll);
    Document.prototype.querySelector = wrapQuerySelector(Document.prototype.querySelector);
    
    // Override on Element.prototype (autofill extensions often call on elements too)
    Element.prototype.querySelectorAll = wrapQuerySelectorAll(Element.prototype.querySelectorAll);
    Element.prototype.querySelector = wrapQuerySelector(Element.prototype.querySelector);
    
    // Function to add autofill prevention attributes to inputs with dictionary IDs
    function preventAutofillOnDictInputs() {
        // Find all inputs whose IDs start with '{' (indicating a dictionary ID)
        try {
            const allInputs = Array.from(document.getElementsByTagName('input'));
            const dictInputs = allInputs.filter(input => input.id && input.id.startsWith('{'));
            
            dictInputs.forEach(input => {
                // Add multiple data attributes to prevent various password managers
                input.setAttribute('data-lpignore', 'true');           // LastPass
                input.setAttribute('data-form-type', 'other');         // Generic
                input.setAttribute('data-bwignore', 'true');           // Bitwarden
                input.setAttribute('data-1p-ignore', 'true');          // 1Password
                input.setAttribute('data-dashlane-rid', '');           // Dashlane
                input.setAttribute('autocomplete', 'off');
                input.setAttribute('autocorrect', 'off');
                input.setAttribute('autocapitalize', 'off');
                input.setAttribute('spellcheck', 'false');
                
                // Mark as readonly temporarily on load to prevent autofill, then remove
                if (!input.hasAttribute('data-autofill-prevented')) {
                    input.setAttribute('readonly', 'readonly');
                    input.setAttribute('data-autofill-prevented', 'true');
                    
                    setTimeout(() => {
                        input.removeAttribute('readonly');
                    }, 100);
                }
            });
        } catch (e) {
            console.error('Error in preventAutofillOnDictInputs:', e);
        }
    }
    
    // Run immediately
    preventAutofillOnDictInputs();
    
    // Run after DOM changes (for dynamically added inputs)
    const observer = new MutationObserver((mutations) => {
        preventAutofillOnDictInputs();
    });
    
    // Start observing when DOM is ready
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    } else {
        document.addEventListener('DOMContentLoaded', () => {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
    }
    
    // Also run on Dash callbacks
    if (window.dash_clientside) {
        window.dash_clientside = window.dash_clientside || {};
        window.dash_clientside.preventAutofill = {
            check: function() {
                setTimeout(preventAutofillOnDictInputs, 50);
                return window.dash_clientside.no_update;
            }
        };
    }
    
    console.log('Autofill prevention script loaded - querySelectorAll override active');
})();
