from flask import Flask, request, jsonify, render_template
import requests
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# T3 AI API bilgileri
API_URL = "https://inference2.t3ai.org/v1/completions"
API_KEY = os.getenv("T3AI_API_KEY")  # API anahtarınızı ortam değişkeni olarak kullanın
GOOGLE_GEOCODE_API_KEY = "YOUR_API_KEY"  # Google Geocoding API anahtarınızı ortam değişkeni olarak kullanın

USER_LOCATION = None

def convert_to_special_format(json_data):
    output = "<|begin_of_text|>"
    for entry in json_data:
        if entry["role"] == "system":
            output += f'<|start_header_id|>system<|end_header_id|>\n\n{entry["content"]}<|eot_id|>'
        elif entry["role"] == "user":
            output += f'\n<|start_header_id|>{entry["role"]}<|end_header_id|>\n\n{entry["content"]}<|eot_id|>'
        elif entry["role"] == "assistant":
            output += f'\n<|start_header_id|>{entry["role"]}<|end_header_id|>\n\n{entry["content"]}<|eot_id|>'

    output += "\n<|start_header_id|>assistant<|end_header_id|>"
    return output

def get_city_country(lat, lng):
    reverse_geocode_api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'latlng': f"{lat},{lng}",
        'key': GOOGLE_GEOCODE_API_KEY
    }
    response = requests.get(reverse_geocode_api_url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['results']:
            address_components = result['results'][0]['address_components']
            city = ''
            country = ''
            for component in address_components:
                if 'locality' in component['types']:
                    city = component['long_name']
                if 'country' in component['types']:
                    country = component['long_name']
            return f"{city}, {country}"
    return None, None

def get_city_coordinates(city_name):
    geocode_api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': city_name,
        'key': GOOGLE_GEOCODE_API_KEY
    }
    response = requests.get(geocode_api_url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['results']:
            location = result['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# Ana sayfa route - index.html'i yükler
@app.route('/')
def home():
    return render_template('index.html')

# Kullanıcı konumunu kaydetme endpoint'i
@app.route('/save_location', methods=['POST'])
def save_location():
    global USER_LOCATION
    user_lat = request.json.get('lat')
    user_lng = request.json.get('lng')

    if user_lat and user_lng:
        USER_LOCATION = (user_lat, user_lng)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})

@app.route('/map')
def map_page():
    global USER_LOCATION
    destination_lat = request.args.get('destination_lat')
    destination_lng = request.args.get('destination_lng')

    if USER_LOCATION:
        user_lat, user_lng = USER_LOCATION
    else:
        # Default user location (Ankara, Turkey)
        user_lat = 39.924878
        user_lng = 32.837207

    return render_template('map.html',
                           user_lat=user_lat,
                           user_lng=user_lng,
                           destination_lat=destination_lat,
                           destination_lng=destination_lng)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        rating = data.get('rating')
        feedback_text = data.get('feedback_text')
        preferred_response = data.get('preferred_response')
        device = data.get('device')
        session_duration = data.get('session_duration')

        # Use global USER_LOCATION if available
        if USER_LOCATION:
            user_lat, user_lng = USER_LOCATION
            location = get_city_country(user_lat, user_lng)
        else:
            location = None

        # Prepare feedback data
        feedback_data = {
            'interaction_id': str(uuid.uuid4()),
            'user_id': 'anonim',
            'timestamp': datetime.utcnow().isoformat(),
            'user_feedback': {
                'rating': rating,
                'feedback_text': feedback_text,
                'preferred_response': preferred_response
            },
        }

        # Save feedback to JSON file
        write_feedback_to_json(feedback_data)

        return jsonify({'status': 'success', 'message': 'Geri bildirim başarıyla alındı.'})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'status': 'error', 'message': 'Geri bildirim alınırken bir hata oluştu.'}), 500

@app.route('/ask', methods=['POST'])
def ask_t3ai():
    user_input = request.json.get("question")

    # API'ye gönderilecek JSON verisi
    json_data = [
        {"role": "system",
         "content": "Sen yardımcı bir asistansın ve sana verilen talimatlar doğrultusunda en iyi cevabı üretmeye çalışacaksın. Türkçe cevap vereceksin. Türkiye'nin ilk büyük Türkçe dil modeli olarak, T3AI'LE projesi kapsamında Baykar Teknoloji ve T3 Vakfı tarafından geliştirilmiş bir yapay zeka asistanıyım. Kullanıcıların sorularına Türkçe olarak doğru ve etkili yanıtlar vermek için tasarlandım."},
        {"role": "user", "content": "türkiyede kaç il var?"},
        {"role": "assistant", "content": "Türkiye'de 81 il bulunmaktadır."},
        {"role": "user", "content": "en büyüğü hangisidir?"},
        {"role": "user", "content": user_input + " genel ve tarihi hakkında bilgi ver."},
    ]

    json_data2 = [
        {"role": "system",
         "content": "Sen kullanıcıya gezilecek yer adlarını tespit eden bir yapay zeka asistansın. Kullanıcının verdiği cümlede gezilecek yer adlarını (entity) bulacaksın."},
        {"role": "user", "content": "Efes Antik Kenti hakkında bilgi ver."},
        {"role": "assistant", "content": "Efes Antik Kenti"},
        
        {"role": "user", "content": "Pamukkale nerede?"},
        {"role": "assistant", "content": "Pamukkale"},
        
        {"role": "user", "content": "Kapadokya'da gezilecek yerler neler?"},
        {"role": "assistant", "content": "Kapadokya"},
        
        {"role": "user", "content": "Aspendos Antik Tiyatrosu'nu görmek istiyorum."},
        {"role": "assistant", "content": "Aspendos Antik Tiyatrosu"},
        
        {"role": "user", "content": "Troya Antik Kenti nerededir?"},
        {"role": "assistant", "content": "Troya Antik Kenti"},
        
        {"role": "user", "content": "Nemrut Dağı'nın önemi nedir?"},
        {"role": "assistant", "content": "Nemrut Dağı"},
        
        {"role": "user", "content": "Topkapı Sarayı'nda ne tür eserler sergileniyor?"},
        {"role": "assistant", "content": "Topkapı Sarayı"},
        
        {"role": "user", "content": "Sumela Manastırı'nı nasıl ziyaret edebilirim?"},
        {"role": "assistant", "content": "Sumela Manastırı"},
        
        {"role": "user", "content": "Sultanahmet Camii hangi tarihte inşa edilmiştir?"},
        {"role": "assistant", "content": "Sultanahmet Camii"},
        
        {"role": "user", "content": "Ani Harabeleri hangi uygarlıklara ev sahipliği yapmıştır?"},
        {"role": "assistant", "content": "Ani Harabeleri"},
        
        {"role": "user", "content": "Göbeklitepe'nin arkeolojik önemi nedir?"},
        {"role": "assistant", "content": "Göbeklitepe"},
        
        {"role": "user", "content": "Bodrum Kalesi'ni ziyaret etmek istiyorum."},
        {"role": "assistant", "content": "Bodrum Kalesi"},
        
        {"role": "user", "content": "Sümela Manastırı'nın tarihi nedir?"},
        {"role": "assistant", "content": "Sümela Manastırı"},
        
        {"role": "user", "content": "Antalya'da gezilecek yerleri sırala"},
        {"role": "assistant", "content": "Antalya"},
        
        {"role": "user", "content": "İstanbul'da gezilecek yerleri sırala"},
        {"role": "assistant", "content": "İstanbul"},
        
        {"role": "user", "content": "İzmir'de gezilecek yerleri sırala"},
        {"role": "assistant", "content": "İzmir"},
    
        {"role": "user", "content": user_input}
    ]


    # JSON verisini prompt template formatına dönüştür
    special_format_output = convert_to_special_format(json_data)
    special_format_output2 = convert_to_special_format(json_data2)

    payload = json.dumps({
        "model": "/home/ubuntu/hackathon_model_2/",
        "prompt": special_format_output,
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 1024,
        "repetition_penalty": 1.1,
        "stop_token_ids": [128001, 128009],
        "skip_special_tokens": True,
        "presence_penalty": 0.6,
        "frequency_penalty": 0.3,
        "best_of": 5
    })

    payload2 = json.dumps({
        "model": "/home/ubuntu/hackathon_model_2/",
        "prompt": special_format_output2,
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 1024,
        "repetition_penalty": 1.1,
        "stop_token_ids": [128001, 128009],
        "skip_special_tokens": True,
        "presence_penalty": 0.6,
        "frequency_penalty": 0.3,
        "best_of": 5
    })

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # T3 AI API'sine POST isteği gönderiyoruz
    try:
        response = requests.post(API_URL, headers=headers, data=payload)
        response2 = requests.post(API_URL, headers=headers, data=payload2)
        response.raise_for_status()
        response2.raise_for_status()

        api_response = response.json()
        api_response2 = response2.json()
        
        answer = api_response['choices'][0]['text']
        city_name = api_response2['choices'][0]['text'].strip()

        real_city_name = get_city_from_place_name(city_name)

        # Şehir adından koordinatları al
        destination_lat, destination_lng = get_city_coordinates(city_name)
        print(destination_lat, destination_lng)

        if destination_lat and destination_lng:
            maps_url = f"/map?destination_lat={destination_lat}&destination_lng={destination_lng}&city={real_city_name}"
            return jsonify({"answer": answer, "maps_url": maps_url, "city_name": city_name})
        else:
            return jsonify({"error": "Şehir koordinatları alınamadı."})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "API ile iletişim sırasında bir hata oluştu.", "details": str(e)})

# Kullanıcı konumundan şehir bilgisi alma fonksiyonu
def get_city_from_place_name(place_name):
    geocode_api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': place_name,
        'key': GOOGLE_GEOCODE_API_KEY
    }
    response = requests.get(geocode_api_url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['results']:
            address_components = result['results'][0]['address_components']
            city = None
            for component in address_components:
                # Öncelikle en geniş bölgeyi döndürmeye çalışıyoruz (admin_area_level_1)
                if 'administrative_area_level_1' in component['types']:
                    city = component['long_name']
                    break
                # Eğer admin_area_level_1 yoksa, admin_area_level_2'yi kontrol ediyoruz
                elif 'administrative_area_level_2' in component['types']:
                    city = component['long_name']
                # En son çare olarak locality'yi alıyoruz (küçük yerleşim)
                elif 'locality' in component['types'] and not city:
                    city = component['long_name']

            if city:
                return city  # Şehir adı (geniş bölge)
    return "Şehir bilgisi alınamadı."

def write_feedback_to_json(feedback_data):
    filename = 'feedback.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            all_data = json.load(file)
    else:
        all_data = []

    all_data.append(feedback_data)

    with open(filename, 'w') as file:
        json.dump(all_data, file, indent=4)


if __name__ == '__main__':
    app.run(debug=True)