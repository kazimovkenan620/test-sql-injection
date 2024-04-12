from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cybertime.db')
    conn.row_factory = sqlite3.Row  # Bu satır, sütun isimleriyle erişime izin verir
    return conn

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()  # Başta ve sonda boşlukları kaldırır
    if not query:  # Eğer query boş ise (hiçbir şey yazılmamışsa)
        return render_template('search_results.html', results=[])  # Boş query ile sonuçları göster

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE first_name LIKE '%{query}%' OR last_name LIKE '%{query}%'")
    
    results = cur.fetchall()
    conn.close()

    return render_template('search_results.html', results=results)

@app.route('/search', methods=['POST'])
def search_post():
    query = request.form.get('query')
    return redirect(f'/search?query={query}')

if __name__ == '__main__':
    app.run(debug=True)
