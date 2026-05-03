from app import app

client = app.test_client()
with client.session_transaction() as sess:
    sess['user_id'] = 1
    sess['role'] = 'host'
    sess['username'] = 'dummy'
    sess['full_name'] = 'Dummy Host'
    sess['email'] = 'host@example.com'

resp = client.get('/dashboard', follow_redirects=False)
print('status', resp.status_code)
print('location', resp.headers.get('Location'))
print(resp.data.decode('utf-8')[:400])
