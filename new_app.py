from flask import Flask, render_template, request, session
from googletrans import Translator
import pandas as pd
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-secret-key'

translator = Translator()

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data', 'indian_gov_schemes.csv')

translation_cache = {}

def get_translation_cache_key(text, lang):
    return f"{lang}:{text}"

def cached_translate(text, lang):
    if lang == 'en' or not text:
        return text
    key = get_translation_cache_key(text, lang)
    if key in translation_cache:
        return translation_cache[key]
    try:
        translated = translator.translate(text, dest=lang)
        translation_cache[key] = translated.text
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def save_translation_cache():
    try:
        with open('translation_cache.json', 'w', encoding='utf-8') as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}")

def load_translation_cache():
    global translation_cache
    try:
        with open('translation_cache.json', 'r', encoding='utf-8') as f:
            translation_cache = json.load(f)
    except FileNotFoundError:
        translation_cache = {}

load_translation_cache()

def get_translations(lang):
    translations = {
        'en': {
            'welcome': 'Welcome to Yojana Saathi',
            'select_language': 'Select Language',
            'age': 'Age',
            'gender': 'Gender',
            'male': 'Male',
            'female': 'Female',
            'other': 'Other',
            'caste': 'Caste',
            'sc': 'SC',
            'st': 'ST',
            'obc': 'OBC',
            'general': 'General',
            'income': 'Income',
            'bpl': 'Below Poverty Line (BPL)',
            'apl': 'Above Poverty Line (APL)',
            'location': 'Location',
            'submit': 'Find Schemes',
            'dashboard_heading': 'Yojana Saathi Dashboard',
            'category_text': 'Based on your profile, here are the categories of schemes you may be eligible for.',
            'category_label': 'Category',
            'details': 'Details',
            'benefits': 'Benefits',
            'application': 'Application Process',
            'documents': 'Required Documents',
            'no_schemes': 'No schemes found. Please try different details.',
            'go_back': 'Go Back to Home',
        },
        'hi': {
            'welcome': 'योजना साथी में आपका स्वागत है',
            'select_language': 'भाषा चुनें',
            'age': 'आयु',
            'gender': 'लिंग',
            'male': 'पुरुष',
            'female': 'महिला',
            'other': 'अन्य',
            'caste': 'जाति',
            'sc': 'अतिपिछड़ा वर्ग',
            'st': 'अनुसूचित जनजाति',
            'obc': 'अन्य पिछड़ा वर्ग',
            'general': 'सामान्य',
            'income': 'आय',
            'bpl': 'गरीबी रेखा के नीचे',
            'apl': 'गरीबी रेखा से ऊपर',
            'location': 'स्थान',
            'submit': 'योजनाएं खोजें',
            'dashboard_heading': 'योजना साथी डैशबोर्ड',
            'category_text': 'आपकी प्रोफ़ाइल के अनुसार, ये योजना श्रेणियां आपके लिए उपयुक्त हो सकती हैं।',
            'category_label': 'श्रेणी',
            'details': 'विवरण',
            'benefits': 'लाभ',
            'application': 'आवेदन प्रक्रिया',
            'documents': 'आवश्यक दस्तावेज़',
            'no_schemes': 'कोई योजना नहीं मिली। कृपया अलग विवरण दर्ज करें।',
            'go_back': 'होम पर वापस जाएं',
        },
        'te': {
            'welcome': 'యోజన సహాయం వద్ద మీకు స్వాగతం',
            'select_language': 'భాషను ఎంచుకోండి',
            'age': 'వయస్సు',
            'gender': 'లింగం',
            'male': 'పురుషుడు',
            'female': 'స్త్రీ',
            'other': 'ఇతరం',
            'caste': 'జాతి',
            'sc': 'అతిపరిహార వర్గం',
            'st': 'అనుయాయ జాతి',
            'obc': 'ఇతర వెనుకబడిన వర్గం',
            'general': 'సాధారణ',
            'income': 'ఆదాయం',
            'bpl': 'తక్కువ ఆదాయం',
            'apl': 'అధిక ఆదాయం',
            'location': 'స్థానం',
            'submit': 'యోజనలను కనుగొనండి',
            'dashboard_heading': 'యోజన సహాయం డ్యాష్‌బోర్డ్',
            'category_text': 'మీ ప్రొఫైల్ ఆధారంగా, మీరు అర్హత పొందిన యోజన శ్రేణులు ఇవి.',
            'category_label': 'వర్గం',
            'details': 'వివరాలు',
            'benefits': 'ప్రయోజనాలు',
            'application': 'దరఖాస్తు ప్రక్రియ',
            'documents': 'అవసరమైన పత్రాలు',
            'no_schemes': 'ఏ యోజనలు కనుగొనలేదు. దయచేసి వేరే వివరాలు ప్రయత్నించండి.',
            'go_back': 'హోమ్‌కు తిరిగి వెళ్లండి',
        },
        'kn': {
            'welcome': 'ಯೋಜನೆ ಸಹಾಯಕಕ್ಕೆ ಸುಸ್ವಾಗತ',
            'select_language': 'ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
            'age': 'ವಯಸ್ಸು',
            'gender': 'ಲಿಂಗ',
            'male': 'ಪುರುಷ',
            'female': 'ಸ್ತ್ರೀ',
            'other': 'ಇತರ',
            'caste': 'ಜನಾಂಗ',
            'sc': 'ಅತಿಪिछಡ ವರ್ಗ',
            'st': 'ನಿರ್ಧಿಷ್ಟ ಜನಾಂಗ',
            'obc': 'ಇತರೆ ಹಿಂದುಳಿದ ವರ್ಗ',
            'general': 'ಸಾಮಾನ್ಯ',
            'income': 'ಆದಾಯ',
            'bpl': 'ಬಡವರಿಗೆ ಅನುದಾನ',
            'apl': 'ಮೇಲಿನ ಆದಾಯ',
            'location': 'ಸ್ಥಳ',
            'submit': 'ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ',
            'dashboard_heading': 'ಯೋಜನೆ ಸಹಾಯಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
            'category_text': 'ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಆಧರಿಸಿ, ನೀವು ಅರ್ಹರಾಗಿರುವ ಯೋಜನಾ ವರ್ಗಗಳು ಇಲ್ಲಿವೆ.',
            'category_label': 'ವರ್ಗ',
            'details': 'ವಿವರಗಳು',
            'benefits': 'ಪ್ರಯೋಜನಗಳು',
            'application': 'ಅರ್ಜಿ ಪ್ರಕ್ರಿಯೆ',
            'documents': 'ಅಗತ್ಯ ದಾಖಲೆಗಳು',
            'no_schemes': 'ಯೋಜನೆಗಳು ದೊರೆಯಲಿಲ್ಲ. ದಯವಿಟ್ಟು ವಿಭಿನ್ನ ವಿವರಗಳನ್ನು ಪ್ರಯತ್ನಿಸಿ.',
            'go_back': 'ಹೋಂಗೆ ಹಿಂತಿರುಗಿ',
        },
        'ml': {
            'welcome': 'യോജന സഹായത്തിന് സ്വാഗതം',
            'select_language': 'ഭാഷ തിരഞ്ഞെടുക്കുക',
            'age': 'പ്രായം',
            'gender': 'ലിംഗം',
            'male': 'പുരുഷൻ',
            'female': 'സ്ത്രീ',
            'other': 'മറ്റുള്ളവ',
            'caste': 'ജാതി',
            'sc': 'അത്യന്ത പിറകിലുള്ള വിഭാഗം',
            'st': 'അനുകൂലിച്ച ജാതി',
            'obc': 'ഇതര പിന്നോക്ക വിഭാഗം',
            'general': 'സാധാരണ',
            'income': 'വരുമാനം',
            'bpl': 'പാവപ്പെട്ടവർ',
            'apl': 'ഉയർന്ന വരുമാനം',
            'location': 'പ്രദേശം',
            'submit': 'യോജനകൾ കണ്ടെത്തുക',
            'dashboard_heading': 'യോജന സഹായം ഡാഷ്ബോർഡ്',
            'category_text': 'നിങ്ങളുടെ പ്രൊഫൈലിന്റെ അടിസ്ഥാനത്തിൽ, നിങ്ങൾക്കായി യോഗ്യമായ പദ്ധതികളുടെ വർഗ്ഗങ്ങൾ ഇവയാണ്.',
            'category_label': 'വിഭാഗം',
            'details': 'വിശദാംശങ്ങൾ',
            'benefits': 'ആനുകൂല്യങ്ങൾ',
            'application': 'അപേക്ഷാ പ്രക്രിയ',
            'documents': 'ആവശ്യമായ രേഖകൾ',
            'no_schemes': 'പദ്ധതികൾ കണ്ടെത്തിയില്ല. ദയവായി മറ്റുള്ള വിവരങ്ങൾ പരീക്ഷിക്കുക.',
            'go_back': 'ഹോം പേജിലേക്ക് മടങ്ങി',
        },
        'ta': {
            'welcome': 'யோஜனை உதவிக்கு வரவேற்கிறோம்',
            'select_language': 'மொழியை தேர்ந்தெடுக்கவும்',
            'age': 'வயது',
            'gender': 'பாலினம்',
            'male': 'ஆண்',
            'female': 'பெண்',
            'other': 'மற்றவை',
            'caste': 'ஜாதி',
            'sc': 'தனிச்சிறுபான்மை',
            'st': 'தனி சாதி',
            'obc': 'மற்ற பின்தங்கிய வகுப்பினர்',
            'general': 'பொதுவான',
            'income': 'வருமானம்',
            'bpl': 'கடுமையான வருமானம்',
            'apl': 'அதிக வருமானம்',
            'location': 'இடம்',
            'submit': 'திட்டங்களை கண்டறியவும்',
            'dashboard_heading': 'யோஜனை உதவி தளக்காட்சி',
            'category_text': 'உங்கள் தனிப்பட்ட விபரங்களின் அடிப்படையில், நீங்கள் தகுதியான திட்ட வகைகள் இவை.',
            'category_label': 'வகை',
            'details': 'விவரங்கள்',
            'benefits': 'நன்மைகள்',
            'application': 'விண்ணப்ப செயல்முறை',
            'documents': 'தேவையான ஆவணங்கள்',
            'no_schemes': 'திட்டங்கள் கிடைக்கவில்லை. தயவு செய்து வேறுபட்ட விபரங்களை முயற்சிக்கவும்.',
            'go_back': 'முகப்புப் பக்கத்திற்கு திரும்பவும்',
        }
    }
    return translations.get(lang, translations['en'])

def load_scheme_data_chunks(chunk_size=3000):
    try:
        for chunk in pd.read_csv(data_path, chunksize=chunk_size):
            yield chunk
    except Exception as e:
        print(f"Error loading CSV in chunks: {e}")
        return []

def translate_category_list(category_str, lang):
    if not category_str:
        return ""
    categories = [c.strip() for c in category_str.split(",")]
    translated_cats = [cached_translate(c, lang) for c in categories]
    return ", ".join(translated_cats)

def match_scheme_to_user(user_profile, eligibility_text, scheme_name, scheme_category):
    """STRICT eligibility checking"""
    text = str(eligibility_text).lower()
    name = str(scheme_name).lower()
    category = str(scheme_category).lower()
    
    gender = user_profile.get('gender', '').lower()
    
    if gender == 'male':
        if any(keyword in text or keyword in name or keyword in category for keyword in 
               ['women', 'woman', 'female', 'maternity', 'pregnant', 'mother', 'girl', 'ladies', 'mahila']):
            return False
    
    if gender == 'female':
        if any(keyword in text or keyword in name for keyword in ['male only', 'men only']):
            return False
    
    age = user_profile.get('age', 0)
    
    if 'child' in text or 'children' in text or 'child' in name or 'children' in name:
        if age >= 18:
            return False
    
    if '18 to 25' in text and not (18 <= age <= 25):
        return False
    if 'above 60' in text or 'senior citizen' in text:
        if age < 60:
            return False
    if 'below 18' in text and age >= 18:
        return False
    
    return True

@app.before_request
def set_language():
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
    elif 'lang' not in session:
        session['lang'] = 'en'

@app.route('/', methods=['GET', 'POST'])
def home():
    lang = session.get('lang', 'en')
    t = get_translations(lang)

    if request.method == 'POST':
        user_profile = {
            'age': int(request.form.get('age', 0)),
            'gender': request.form.get('gender', '').lower(),
            'caste': request.form.get('caste', '').lower(),
            'income': request.form.get('income', '').lower(),
            'location': request.form.get('location', '').lower()
        }

        matched_schemes = []
        for chunk in load_scheme_data_chunks():
            for _, row in chunk.iterrows():
                original_category = row.get('schemeCategory', '')
                
                if match_scheme_to_user(user_profile, 
                                       str(row.get('eligibility', '')),
                                       str(row.get('scheme_name', '')),
                                       str(original_category)):
                    matched_schemes.append({
                        'name': cached_translate(row.get('scheme_name', ''), lang),
                        'category': translate_category_list(original_category, lang),
                        'category_original': original_category,
                        'details': cached_translate(str(row.get('details', ''))[:500], lang),  # Limit length
                        'benefits': cached_translate(str(row.get('benefits', ''))[:500], lang),
                        'application': cached_translate(str(row.get('application', ''))[:500], lang),
                        'documents': cached_translate(str(row.get('documents', ''))[:500], lang),
                    })
                    if len(matched_schemes) >= 30:  # Reduced to 30 for faster loading
                        break
            if len(matched_schemes) >= 30:
                break

        save_translation_cache()

        return render_template('new_dashboard.html', matched_schemes=matched_schemes, user_profile=user_profile, t=t, lang=lang)

    return render_template('new_home.html', t=t, lang=lang)

@app.route('/results')
def show_results():
    lang = session.get('lang', 'en')
    t = get_translations(lang)

    category = request.args.get('category')
    
    user_profile = {
        'age': int(request.args.get('age', 0)),
        'gender': request.args.get('gender', ''),
        'caste': request.args.get('caste', ''),
        'income': request.args.get('income', ''),
        'location': request.args.get('location', '')
    }

    schemes_in_category = []
    for chunk in load_scheme_data_chunks():
        for _, row in chunk.iterrows():
            original_category = row.get('schemeCategory', '')
            
            if (match_scheme_to_user(user_profile, 
                                    str(row.get('eligibility', '')),
                                    str(row.get('scheme_name', '')),
                                    str(original_category)) and
                str(original_category).lower() == str(category).lower()):
                schemes_in_category.append({
                    'name': cached_translate(row.get('scheme_name', ''), lang),
                    'category': translate_category_list(original_category, lang),
                    'details': cached_translate(str(row.get('details', ''))[:500], lang),
                    'benefits': cached_translate(str(row.get('benefits', ''))[:500], lang),
                    'application': cached_translate(str(row.get('application', ''))[:500], lang),
                    'documents': cached_translate(str(row.get('documents', ''))[:500], lang),
                })
                if len(schemes_in_category) >= 30:
                    break
        if len(schemes_in_category) >= 30:
            break

    save_translation_cache()

    return render_template('new_results.html', schemes=schemes_in_category, selected_category=translate_category_list(category, lang), t=t, lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
