let translations = {};
let currentLanguage = localStorage.getItem('language') || 'fr';

// Load translations from JSON file
async function loadTranslations() {
  try {
    const response = await fetch('/static/js/translations.json');
    translations = await response.json();
    updatePageLanguage();
  } catch (error) {
    console.error('Error loading translations:', error);
  }
}

// Update all elements with data-translate attribute
function updatePageLanguage() {
  document.documentElement.lang = currentLanguage;
  
  // Update all elements with data-translate attribute
  const elements = document.querySelectorAll('[data-translate]');
  elements.forEach(element => {
    const key = element.getAttribute('data-translate');
    if (translations[currentLanguage] && translations[currentLanguage][key]) {
      // Check if it's an input placeholder
      if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
        element.placeholder = translations[currentLanguage][key];
      } else {
        element.textContent = translations[currentLanguage][key];
      }
    }
  });

  // Update page title if present
  const titleElement = document.querySelector('title[data-translate]');
  if (titleElement) {
    const key = titleElement.getAttribute('data-translate');
    if (translations[currentLanguage] && translations[currentLanguage][key]) {
      titleElement.textContent = translations[currentLanguage][key];
    }
  }

  // Update language selector
  updateLanguageSelector();
}

// change lang from dropdown
function changeLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('language', currentLanguage);
  updatePageLanguage();
}

// update dropdown selected value
function updateLanguageSelector() {
  const languageSelector = document.getElementById('language-selector');
  if (languageSelector) {
    languageSelector.value = currentLanguage;
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  loadTranslations();
  
  const languageSelector = document.getElementById('language-selector');
  if (languageSelector) {
    languageSelector.addEventListener('change', (e) => {
      changeLanguage(e.target.value);
    });
    updateLanguageSelector();
  }
});
