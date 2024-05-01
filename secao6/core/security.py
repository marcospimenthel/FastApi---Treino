from passlib.context import CryptContext

# Criptografia de senhas com o algoritmo bcrypt
CRYPT_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash da senha armazenada.
    
    Args:
        senha: A senha em texto plano.
        hash_senha: O hash da senha armazenada.
    
    Returns:
        True se a senha corresponder ao hash_senha, False caso contrário.
    """
    return CRYPT_CONTEXT.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash seguro para a senha fornecida.
    
    Args:
        senha: A senha em texto plano.
    
    Returns:
        O hash seguro da senha.
    """
    return CRYPT_CONTEXT.hash(senha)
