class ErroMatricula(Exception):
    """Classe base para exceções relacionadas ao sistema de matrículas."""
    pass
    
class ValorInvalidoError(ErroMatricula):
    """Lançado quando um valor numérico está fora do intervalo permitido."""
    pass
    
class TipoInvalidoError(ErroMatricula):
    """Lançado quando o tipo de um dado é inadequado."""
    pass
    
class MaximoItensAtingidoError(ErroMatricula):
    """Lançado ao tentar adicionar um item a uma coleção que já está cheia."""
    pass
    
class MatriculaNaoEncontradaError(ErroMatricula, KeyError):
    """Lançado quando uma matrícula buscada não existe no registro."""
    pass
    
class RegistroDuplicadoError(ErroMatricula, ValueError):
    """Lançado ao tentar inserir uma matrícula que já existe no registro."""
    pass