from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# SQLite veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('blog.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# Üye olma fonksiyonu
def uye_kaydet(adi, soyadi, kullanici_adi, sifre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO uyeler (uye_adi, uye_soyad, kullanici_adi, sifre) VALUES (?, ?, ?, ?)', (adi, soyadi, kullanici_adi, sifre))
    conn.commit()
    conn.close()

# Kullanıcı girişi kontrolü
def kullanici_giris(kullanici_adi, sifre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM uyeler WHERE kullanici_adi = ? AND sifre = ?', (kullanici_adi, sifre))
    user = cur.fetchone()
    conn.close()
    return user

# Giriş sayfasını render eder
@app.route('/')
def giris():
    return render_template('giris.html')

# Giriş yapma işlemi
@app.route('/giris', methods=['POST'])
def giris_yap():
    if request.method == 'POST':
        kullanici_adi = request.form['username']
        sifre = request.form['password']

        user = kullanici_giris(kullanici_adi, sifre)

        if user:
            session['is_admin'] = False
            session['logged_in'] = True
            session['kullanici_adi'] = kullanici_adi
            return redirect('/uye_ol_anasayfa')

        elif kullanici_adi == 'admin' and sifre == 'admin123':
            session['is_admin'] = True
            session['logged_in'] = True
            return redirect('/anasayfa')

        else:
            return render_template('giris.html', error_message="Hatalı kullanıcı adı veya şifre!")

# Admin anasayfa sayfasını render eder
@app.route('/anasayfa')
def anasayfa():
    if 'logged_in' in session and session['is_admin']:
        conn = get_db_connection()
        son_yazilar = conn.execute('SELECT * FROM bloglar ORDER BY rowid DESC LIMIT 3').fetchall()
        conn.close()
        return render_template('anasayfa.html', son_yazilar=son_yazilar)
    else:
        return redirect('/uye_ol_anasayfa')

# Üye anasayfa sayfasını render eder
@app.route('/uye_ol_anasayfa')
def uye_ol_anasayfa():
    if 'logged_in' in session and not session['is_admin']:
        conn = get_db_connection()
        son_yazilar = conn.execute('SELECT * FROM bloglar ORDER BY rowid DESC LIMIT 3').fetchall()
        conn.close()
        return render_template('uye_ol_anasayfa.html', son_yazilar=son_yazilar)
    else:
        return redirect('/anasayfa')

# İletişim sayfasını render eder
@app.route('/iletisim', methods=['GET'])
def get_iletisim():
    if 'logged_in' in session and not session['is_admin']:
        return render_template('iletisim.html')
    else:
        return redirect('/anasayfa')

# Admin hakkımda sayfasını render eder
@app.route('/hakkimda')
def hakkimda():
    if 'logged_in' in session and session['is_admin']:
        return render_template('hakkimda.html')
    else:
        return redirect('/hakkimda')

# Admin blog sayfasını render eder
@app.route('/blog')
def blog():
    if 'logged_in' in session and session['is_admin']:
        conn = get_db_connection()
        bloglar = conn.execute('SELECT * FROM bloglar').fetchall()
        posts = []
        for blog in bloglar:
            post = dict(blog)
            like_count = conn.execute('SELECT COUNT(*) as count FROM begenmeler WHERE blog_id = ?', (blog['id'],)).fetchone()['count']
            comments = conn.execute('SELECT * FROM yorumlar WHERE blog_id = ? ORDER BY tarih DESC', (blog['id'],)).fetchall()
            post['like_count'] = like_count
            post['comments'] = comments
            posts.append(post)
        conn.close()
        return render_template('blog.html', posts=posts)
    else:
        return redirect('/uye_ol_blog')

# Üye blog sayfasını render eder
@app.route('/uye_ol_blog')
def uye_ol_blog():
    if 'logged_in' in session and not session['is_admin']:
        conn = get_db_connection()
        bloglar = conn.execute('SELECT * FROM bloglar').fetchall()
        conn.close()
        return render_template('uye_ol_blog.html', posts=bloglar)
    else:
        return redirect('/blog')

# Üye hakkımda sayfasını render eder
@app.route('/uye_ol_hakkimda')
def uye_ol_hakkimda():
    if 'logged_in' in session and not session['is_admin']:
        return render_template('uye_ol_hakkimda.html')
    else:
        return redirect('/hakkimda')

# Blog yazısı ekleme işlemi
@app.route('/yazi-ekle', methods=['GET', 'POST'])
def yazi_ekle():
    if request.method == 'POST':
        baslik = request.form['title']
        icerik = request.form['content']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO bloglar (baslik, icerik) VALUES (?, ?)', (baslik, icerik))
        conn.commit()
        conn.close()

        return redirect('/blog')
    return render_template('yazi-ekle.html')

# İletişim formunu işler
@app.route('/iletisim', methods=['POST'])
def handle_contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO iletisim (ad, eposta, konu, mesaj) VALUES (?, ?, ?, ?)', (name, email, subject, message))
        conn.commit()
        conn.close()

        return redirect('/iletisim')

# Üye olma işlemi
@app.route('/uye_ol', methods=['GET', 'POST'])
def uye_ol():
    if request.method == 'POST':
        adi = request.form['name']
        soyadi = request.form['surname']
        kullanici_adi = request.form['username']
        sifre = request.form['password']

        uye_kaydet(adi, soyadi, kullanici_adi, sifre)

        return redirect('/')

    return render_template('uye_ol.html')

# Blog yazısını id'sine göre siler
@app.route('/sil/<int:id>', methods=['POST'])
def sil(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM bloglar WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204  # No Content

# Blog yazısını id'sine göre düzenler
@app.route('/duzenle/<int:id>', methods=['GET', 'POST'])
def duzenle(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM bloglar WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        baslik = request.form['title']
        icerik = request.form['content']
        conn.execute('UPDATE bloglar SET baslik = ?, icerik = ? WHERE id = ?', (baslik, icerik, id))
        conn.commit()
        conn.close()
        return redirect('/blog')
    conn.close()
    return render_template('duzenle.html', post=post)

# Güncel sayfa bilgisini günceller
@app.route('/update_current_page', methods=['POST'])
def update_current_page():
    if request.method == 'POST':
        data = request.json
        current_page = data['current_page']
        session['current_page'] = current_page
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 400

# Kullanıcı çıkış yapar ve session'ı temizler
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Blog yazısını beğenme işlemi
@app.route('/begen/<int:blog_id>', methods=['POST'])
def begen(blog_id):
    if 'logged_in' in session:
        kullanici_adi = session['kullanici_adi']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO begenmeler (blog_id, kullanici_adi) VALUES (?, ?)', (blog_id, kullanici_adi))
        conn.commit()
        conn.close()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Lütfen giriş yapınız!'}), 401

# Blog yazısına yorum yapma işlemi
@app.route('/yorum_yap/<int:blog_id>', methods=['POST'])
def yorum_yap(blog_id):
    if 'logged_in' in session:
        kullanici_adi = session['kullanici_adi']
        yorum = request.form['yorum']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO yorumlar (blog_id, kullanici_adi, yorum) VALUES (?, ?, ?)', (blog_id, kullanici_adi, yorum))
        conn.commit()
        conn.close()
        return redirect(url_for('uye_ol_blog'))
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run()
