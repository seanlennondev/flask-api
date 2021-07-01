import  pytest
from httpx import post, delete, get, put, patch

@pytest.fixture
def get_uri():
    return 'http://localhost:5000/api/users'

@pytest.fixture
def get_token(get_uri):
    res = post(get_uri + '/auth', json={
        'email': 'sean@gmail.com',
        'password': '12345'
    })
    return res.json()['access_token']

@pytest.fixture
def get_header(get_token):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_token}'
    }

@pytest.mark.parametrize(('username', 'name', 'surname', 'email', 'password', 'msg', 'status_code'), (
    (None, 'Carla', 'Eloi', 'carla@gmail.com', '12345', 'O campo nome de usuário é obrigatório', 422),
    ('carla_eloi', None, 'Eloi', 'carla@gmail.com', '12345', 'O campo nome é obrigatório', 422),
    ('carla_eloi', 'Carla', None, 'carla@gmail.com', '12345', 'O campo sobrenome é obrigatório', 422),
    ('carla_eloi', 'Carla', 'Eloi', None, '12345', 'O campo e-mail é obrigatório', 422),
    ('carla_eloi', 'Carla', 'Eloi', 'carla@gmail.com', None, 'O campo senha é obrigatório', 422),
    ('carla_eloi', 'Carla', 'Eloi', 'carla@gmail.com', '12345', 'Admin registrado com sucesso', 200),
))
@pytest.mark.create_admin
def test_um_superusuario_deve_criar_um_admin(
    get_header,
    get_uri,
    username, name, surname, email, password, msg, status_code
):
    res = post(get_uri + '/admin', json={
        'username': username,
        'name': name,
        'surname': surname,
        'email': email,
        'password': password
    }, headers=get_header)
    assert status_code == res.status_code and msg == res.json()['msg']

@pytest.mark.parametrize(('id', 'msg', 'status_code'), (
    (3, 'Admin não encontrado', 404),
    (2, 'Admin encontrado com sucesso', 200)
))
@pytest.mark.get_admin
def test_um_superusuario_deve_obter_um_admin(
    get_header,
    get_uri,
    id, msg, status_code
):
    res = get(f'{get_uri}/admin/{id}', headers=get_header)
    assert status_code == res.status_code and msg == res.json()['msg']

@pytest.mark.parametrize(('id', 'name', 'surname', 'msg', 'status_code'), (
    (3, 'Ana', 'Luiza', 'Admin não encontrado', 404),
    (2, None, 'Luiza', 'O campo nome é obrigatório', 422),
    (2, 'Ana', None, 'O campo sobrenome é obrigatório', 422),
    (2, 'Ana', 'Luiza', 'Admin alterado com sucesso', 200)
))
@pytest.mark.update_admin
def test_deve_alterar_um_admin(
    get_header,
    get_uri,
    id, name, surname, msg, status_code
):
    res = put(f'{get_uri}/admin/{id}', json={
        'name': name,
        'surname': surname
    }, headers=get_header)
    assert status_code == res.status_code and msg == res.json()['msg']

@pytest.mark.parametrize(('id', 'current_password', 'new_password', 'msg', 'status_code'), (
    (3, '12345', '123456', 'Admin não encontrado', 404),
    (2, None, '123', 'O campo senha atual é obrigatório', 422),
    (2, '12345', None, 'O campo nova senha é obrigatório', 422),
    (2, '123', '123', 'Senha atual inválida', 422),
    (2, '12345','1234', 'Senha alterada com sucesso', 200),
))
@pytest.mark.change_password_admin
def test_deve_alterar_a_senha_de_um_admin(
    get_header,
    get_uri,
    id, current_password, new_password, msg, status_code
):
    res = patch(f'{get_uri}/admin/{id}', json={
        'current_password': current_password,
        'new_password': new_password
    }, headers=get_header)
    assert status_code == res.status_code and msg == res.json()['msg']

@pytest.mark.parametrize(('user_id', 'msg', 'status_code'), (
    (3, 'Admin não encontrado', 404),
    (2, 'Admin excluído com sucesso', 200)
))
@pytest.mark.delete_admin
def test_um_superusuario_deve_excluir_um_admin(
    get_header,
    get_uri,
    user_id, msg, status_code
):
    res = delete(f'{get_uri}/admin/{user_id}', headers=get_header)
    assert res.status_code == status_code and res.json()['msg'] == msg
