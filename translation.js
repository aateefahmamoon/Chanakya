const buttons = document.querySelectorAll('.lang-btn');
const texts = document.querySelectorAll('.translatable');

const LANG_CODES = {
  "en": "en",
  "hi": "hi",
  "te": "te",
  "mr": "mr",
  "kn": "kn",
  "ta": "ta"
};

texts.forEach(el => {
  el.dataset.original = el.textContent.trim();
});

async function translateText(text, targetLang) {
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`;
    const response = await fetch(url);
    const data = await response.json();
    if (data && data[0] && data[0][0] && data[0][0][0]) {
      return data[0][0][0];
    }
    return text;
  } catch (error) {
    console.error('Translation error:', error);
    return text;
  }
}

async function translateAll(targetLang) {
  const translations = [];
  for(let el of texts) {
    const originalText = el.dataset.original;
    const translated = await translateText(originalText, targetLang);
    translations.push(translated);
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  return translations;
}

buttons.forEach(btn => {
  btn.addEventListener('click', async () => {
    const lang = btn.id.split('-')[0];
    if(btn.classList.contains('active')) return;

    buttons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    if(lang === "en") {
      texts.forEach(el => {
        el.textContent = el.dataset.original;
        el.classList.remove('loading');
      });
      return;
    }

    buttons.forEach(b => b.disabled = true);
    texts.forEach(el => el.classList.add('loading'));

    try {
      const targetLang = LANG_CODES[lang];
      const translations = await translateAll(targetLang);
      texts.forEach((el,i) => {
        el.textContent = translations[i];
        el.classList.remove('loading');
      });
    } catch(e) {
      console.error('Translation failed:', e);
      alert('Translation failed. Please try again.');
      texts.forEach(el => {
        el.textContent = el.dataset.original;
        el.classList.remove('loading');
      });
      buttons.forEach(b => b.classList.remove('active'));
      document.getElementById('en-btn').classList.add('active');
    } finally {
      buttons.forEach(b => b.disabled = false);
    }
  });
});
