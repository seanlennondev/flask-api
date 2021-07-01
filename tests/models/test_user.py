from httpx import get

def test_deve_retornar_uma_lista_de_usuarios():
    res = get('http://localhost:5000/api/users')
    assert res.status_code == 200
