# Blog Yönetim Sistemi

Bu proje benim kişisel blog sitemdir. Blog yazıları yazabileceğim, silebileceğim ve düzenleyebileceğim bir blog yönetim sistemidir. Admin ve kullanıcı rollerine sahiptir. Ben admin olarak blog yazıları ekleyebilir, düzenleyebilir ve silebilirim. Üyeler ise sadece blog yazılarını beğenebilir ve yorum yapabilir. Üye yorumlarını da ben görebilirim.

## İçindekiler

- [Özellikler](#özellikler)
- [İşlemler](#işlemler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [API Endpoint'leri](#api-endpointleri)
- [Veritabanı](#veritabanı)
- [Katkıda Bulunma](#katkıda-bulunma)

## Özellikler

- Kullanıcı kayıt ve giriş sistemi
- Admin ve kullanıcı rolleri
  - **Admin**: Blog yazıları ekleyebilir, düzenleyebilir ve silebilir.
  - **Kullanıcı**: Blog yazılarını görüntüleyebilir, beğenebilir ve yorum yapabilir.
- İletişim formu

## İşlemler

Kodun backend tarafı Python dilinde yazılmıştır ve `islemler.py` dosyasında bulunmaktadır. Frontend içinse HTML ve CSS kullanılmaktadır. Stil dosyası `stil.css` olarak adlandırılmıştır ve HTML dosyalarından çağrılmaktadır.


## Kurulum

1. **Depoyu Klonla**

    ```bash
    git clone https://github.com/kullaniciadi/blog-yonetim-sistemi.git
    cd blog-yonetim-sistemi
    ```

2. **Sanal Ortam Oluştur ve Aktifleştir**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Unix tabanlı sistemler için
    venv\Scripts\activate  # Windows için
    ```

3. **Gerekli Paketleri Yükle**

    ```bash
    pip install -r requirements.txt
    ```

4. **Veritabanını Kur**

    SQLite veritabanını oluşturmak için aşağıdaki komutları kullanın:

    ```bash
    sqlite3 blog.db < schema.sql
    ```

5. **Uygulamayı Başlat**

    ```bash
    flask run
    ```

    Uygulama, [http://127.0.0.1:5000](http://127.0.0.1:5000) adresinde çalışacaktır.

## Kullanım

- **Giriş Sayfası**: Kullanıcı adı ve şifre ile giriş yapabilirsiniz. Admin kullanıcı adı `admin` ve şifresi `admin123` olarak ayarlanmıştır.
- **Kayıt Olma**: Kullanıcılar yeni bir hesap oluşturabilir.
- **Blog Yönetimi**:
  - **Admin**: Blog yazılarını ekleyebilir, düzenleyebilir ve silebilir.
  - **Kullanıcı**: Blog yazılarını görüntüleyebilir, beğenebilir ve yorum yapabilir.

## API Endpoint'leri

- **Giriş Yapma**: `/giris`
- **Anasayfa (Admin)**: `/anasayfa`
- **Anasayfa (Kullanıcı)**: `/uye_ol_anasayfa`
- **Blog Sayfası (Admin)**: `/blog`
- **Blog Sayfası (Kullanıcı)**: `/uye_ol_blog`
- **Hakkımda Sayfası (Admin)**: `/hakkimda`
- **Hakkımda Sayfası (Kullanıcı)**: `/uye_ol_hakkimda`
- **İletişim Sayfası**: `/iletisim`
- **Blog Yazısı Ekleme (Admin)**: `/yazi-ekle`
- **Blog Yazısını Silme (Admin)**: `/sil/<int:id>`
- **Blog Yazısını Düzenleme (Admin)**: `/duzenle/<int:id>`
- **Beğenme İşlemi (Kullanıcı)**: `/begen/<int:blog_id>`
- **Yorum Yapma İşlemi (Kullanıcı)**: `/yorum_yap/<int:blog_id>`
- **Güncel Sayfa Bilgisini Güncelleme**: `/update_current_page`
- **Çıkış Yapma**: `/logout`

## Veritabanı

Veritabanı SQLite kullanılarak oluşturulmuştur. Veritabanı şeması `schema.sql` dosyasında bulunabilir. Temel tablolar şunlardır:

- **uyeler**: Kullanıcı bilgilerini saklar.
- **bloglar**: Blog yazılarını saklar.
- **begenmeler**: Blog yazılarına yapılan beğenmeleri saklar.
- **yorumlar**: Blog yazılarına yapılan yorumları saklar.
- **iletisim**: İletişim formu gönderilerini saklar.

## Katkıda Bulunma

Katkıda bulunmak için lütfen bir pull request gönderin veya bir issue açın. Katkılarınızı memnuniyetle karşılıyoruz!