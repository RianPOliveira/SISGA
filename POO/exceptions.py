class ErroMatricula(Exception):
    """Classe base para todas as exceções do sistema de matrículas."""
    pass

class ValorInvalidoError(ErroMatricula):
    """Exceção para valores que estão fora de um intervalo permitido (ex: nota negativa)."""
    pass

class TipoInvalidoError(ErroMatricula):
    """Exceção para dados que são de um tipo incorreto (ex: passar um texto onde se espera um número)."""
    pass

class MaximoItensAtingidoError(ErroMatricula):
    """Exceção para quando se tenta adicionar um item a uma coleção cheia (ex: 5ª nota de um aluno)."""
    pass

class MatriculaNaoEncontradaError(ErroMatricula):
    """Exceção para buscas por uma matrícula que não existe no registro."""
    pass

class RegistroDuplicadoError(ErroMatricula):
    """Exceção para quando se tenta inserir uma matrícula que já foi cadastrada."""
    pass