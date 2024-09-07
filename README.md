# TourMate Chatbot

TourMate, sesli komutlar ve GPS verileri kullanarak turistlere kişiselleştirilmiş rota önerileri sunan yenilikçi bir chatbot uygulamasıdır. Bu uygulama, turistlerin anlık bilgi ihtiyaçlarını karşılamak ve seyahat deneyimlerini zenginleştirmek amacıyla tasarlanmıştır.

## Özellikler

1. **Sesli Komut Algılama**: Kullanıcılar tarafından verilen sesli komutlar doğrultusunda etkileşim sağlar.
2. **GPS Bağlantılı Rota Önerileri**: Kullanıcıların mevcut konumlarına bağlı olarak turistik yer önerilerinde bulunur.
3. **Dinamik Rota Planlama**: GPS verilerini kullanarak kullanıcının ilgisine uygun dinamik rotalar oluşturur.
4. **Anlık Bilgi Sağlama**: Kullanıcıların sorularına anında, doğru ve güncel bilgilerle yanıt verir.

## Kullanılan Teknolojiler

1. **T3 AI Yapay Zeka Modeli**: T3 AI tarafından geliştirilen yapay zeka altyapısını kullanır.
2. **Google Geocoding API**: Kullanıcıların konum bilgilerini doğru bir şekilde işlemek için kullanılır.
3. **Flask Framework**: Sunucu tarafı uygulama geliştirmede kullanılır.
4. **SpeechRecognition Kütüphanesi**: Kullanıcıların sesli komutlarını algılar ve işleyerek yanıt verir.
5. **OpenWeather API**: Hava durumu bilgilerini kullanıcıya sağlamak için kullanılır.

## Takım Adı: Takım ID
- 👤 Bengisu ATLI
- 👤 Deniz TAŞ

## Uygulamadan Ekran Görüntüleri

![WhatsApp Image 2024-09-07 at 11 23 57](https://github.com/user-attachments/assets/88420906-5f16-42f3-9512-3e1bbf1fe02f)

![WhatsApp Image 2024-09-07 at 11 23 57 (1)](https://github.com/user-attachments/assets/439a142d-30ef-42f7-bb89-c5cc1dace26a)

## Uygulamayı Lokalde Çalıştırma

Bu adımlar, Flask uygulamanızı lokal ortamda nasıl çalıştıracağınızı açıklar.

### Gereksinimler

- Python 3.x
- Flask
- requests
- Google Geocoding API Key (isteğe bağlı, coğrafi sorgular için)

### Kurulum Adımları

1. **Depoyu Klonlayın:**

   ```bash
   git clone https://github.com/kullanıcı_adı/proje_adı.git
   cd proje_adı

2. **Gerekli Kütüphaneleri Yükleyin:**
Gerekli Python kütüphanelerini yüklemek için bir virtualenv oluşturup ardından bağımlılıkları yükleyin:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows kullanıyorsanız: venv\Scripts\activate
   pip install -r requirements.txt

3. **Ortam Değişkenlerini Ayarlayın:**
 T3 AI API anahtarınızı ve Google Geocoding API anahtarınızı ortam değişkeni olarak ayarlayın:

   ```bash
   export T3AI_API_KEY='YOUR_T3AI_API_KEY'
   export GOOGLE_GEOCODE_API_KEY='YOUR_GOOGLE_GEOCODE_API_KEY'
   
   
Windows için:

   ```bash
   set T3AI_API_KEY='YOUR_T3AI_API_KEY'
   set GOOGLE_GEOCODE_API_KEY='YOUR_GOOGLE_GEOCODE_API_KEY'


4. **Uygulamayı Çalıştırın:**
Flask uygulamanızı başlatın:

   ```bash
    python app.py


5. Uygulamayı Tarayıcıda Açın:
Uygulama çalıştığında, tarayıcınızdan aşağıdaki URL'yi açabilirsiniz:

    ```bash
http://127.0.0.1:5000


