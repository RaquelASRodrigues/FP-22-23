# Fundamentos da Programação 2022/23
# Raquel Rodrigues - ist1106322

def limpa_texto(cad):
    """devolve a cadeia de caracteres limpa
    limpa_texto: str --> str
    """
    return ' '.join(cad.split())

def corta_texto(txt, l):
    """devolve duas subcadeias limpas
    corta_texto: str x int --> str
    """
    if ' ' not in txt:
        return txt, ''
    else:
        for i in range(l - 1, 0,-1):
            if txt[i] == ' ':
                cad_cortada = txt[:i]
                resto = txt[i:len(txt)].lstrip() #eliminar espaços à esquerda
                return cad_cortada, resto
            elif txt[i+1] == ' ':
                cad_cortada = txt[:i+1]
                resto = txt[i + 1:len(txt)].lstrip()
                return cad_cortada, resto

def insere_espacos(cad,l):
    """Devolve uma cadeia de comprimento igual à largura pretendida
    insere_espacos: str x int --> str
    """
    espacos_extra = l - len(cad)
    palavras = cad.split()

    if len(palavras) == 1: #cadeia com uma palavra
        return cad + ' '*espacos_extra

    if len(palavras) >= 2: #cadeia com duas ou mais palavras
        cad_final = cad
        #inserir espaços entre as palavras uniformemente
        while espacos_extra >= len(palavras) - 1:
            i = 0
            espacos_adicionados = 0
            while espacos_adicionados < len(palavras) -1:
                if cad_final[i] != ' ' and cad_final[i+1] == ' ':
                    cad_final = cad_final[:i+1] + ' ' + cad_final[i+1:len(cad_final)]
                    espacos_extra -= 1
                    espacos_adicionados += 1
                    i += 2
                else:
                    i += 1
    #acrescentar espaços adicionais da esquerda para a direita
    if espacos_extra > 0:
        i = 0
        espacos_adicionados = 0
        while espacos_adicionados < len(palavras) -1:
            if cad_final[i] != ' ' and cad_final[i+1] == ' ':
                cad_final = cad_final[:i+1] + ' ' + cad_final[i+1:len(cad_final)]
                espacos_extra -= 1
                espacos_adicionados += 1
                i += 2
                if espacos_extra == 0:
                    break
            else:
                i += 1
    return cad_final

def justifica_texto(cad,l):
    """devolve um tuplo de cadeias de caracteres justificadas
    justifica_texto: str x int --> tuple
    """
    if not isinstance(cad, str) or cad == "" or not isinstance(l, int) \
        or not l > 0:
        raise ValueError('justifica_texto: argumentos invalidos')
    palavras = cad.split()
    for e in palavras:
        #as palavras não podem ser maiores que a largura da coluna
        if len(e) > l:
            raise ValueError('justifica_texto: argumentos invalidos')

    cad_limpa = limpa_texto(cad)
    txt_cortado = ()
    while len(cad_limpa) > l:
        res = corta_texto(cad_limpa, l)
        txt_cortado += (res[0],)
        cad_limpa = res[1]

    if cad_limpa != '':
        txt_cortado += (cad_limpa,)

    txt_final = ()
    for i in range(len(txt_cortado) - 1):
        txt_final += (insere_espacos(txt_cortado[i],l),)

    #espaços a inserir na linha final
    espacos_extra = l - len(txt_cortado[-1]) 
    txt_final += (txt_cortado[-1] + ' '*espacos_extra,)

    return txt_final


def calcula_quocientes(info_votos, deputados):
    """devolve uma lista com os quocientes calculados usando o método de Hondt
    calcula_quocientes: dict x int --> dict
    """
    res = {}
    for partido in info_votos:
        votos = info_votos[partido]
        res[partido] = []
        for i in range(1, deputados + 1):
            res[partido] += [votos / i]
    return res

def atribui_mandatos(info_votos, deputados):
    """devolve a lista ordenada dos partidos que obtiveram cada mandato
    atribui_mandatos: dict x int --> list
    """
    quocientes = calcula_quocientes(info_votos, deputados)
    res_mandatos = []
    t_partidos = ()
    for partido in quocientes:
        t_partidos += (partido,)

    while len(res_mandatos) < deputados:
        t_quocientes = ()
        for partido in quocientes:
            t_quocientes += (quocientes[partido][0],)

        maximo = max(t_quocientes)
        indice_maximo = t_quocientes.index(maximo)

        #caso hajam partidos com igual quociente
        for i in range(len(t_quocientes)):
            if t_quocientes[i] == maximo and i != indice_maximo:
                if info_votos[t_partidos[i]] < info_votos[t_partidos[indice_maximo]]:
                    indice_maximo = i

        partido_elegido = t_partidos[indice_maximo]
        res_mandatos += [partido_elegido]
        del quocientes[partido_elegido][0]
    return res_mandatos

def obtem_partidos(info):
    """devolve a lista dos partidos participantes por ordem alfabética
    obtem_partidos: dict --> list
    """
    lista_participantes = []
    for circulo in info:
        for partido in info[circulo]['votos']:
            if partido not in lista_participantes:
                lista_participantes += [partido]
    return sorted(lista_participantes)

def obtem_resultado_eleicoes(info):
    """devolve a lista ordenada com o resultado das eleições
    obtem_resultado_eleicoes: dict --> list
    """
    if not type(info) == dict or info == {}:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    for circulo in info:
        if not isinstance(circulo, str) or not isinstance(info[circulo], dict):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        if 'deputados' not in info[circulo] or 'votos' not in info[circulo] \
            or len(info[circulo]) != 2:
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        if not type(info[circulo]['deputados']) == int or \
            not info[circulo]['deputados'] > 0 or \
            not type(info[circulo]['votos']) == dict or \
            info[circulo]['votos'] == {}:
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')

        for partido in info[circulo]['votos']:
            if not type(partido) == str or \
                not type(info[circulo]['votos'][partido]) == int \
                or info[circulo]['votos'][partido] < 0:
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')
            if len(info[circulo]['votos']) == 1 and \
                info[circulo]['votos'][partido] == 0:
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')

    lista_resultado = []
    for partido in obtem_partidos(info):
        soma_deputados = 0
        total_votos = 0
        for circulo in info:
            soma_deputados += atribui_mandatos(info[circulo]['votos'], \
                info[circulo]['deputados']).count(partido)
            if partido in info[circulo]['votos']:
                total_votos += info[circulo]['votos'][partido]

        lista_resultado += [(partido, soma_deputados, total_votos)]

    lista_resultado.sort(key = lambda x: (x[1], x[2]), reverse = True)
    return lista_resultado

def produto_interno(v1, v2):
    """devolve o resultado do produto interno de dois vetores
    produto_interno: tuple x tuple --> float
    """
    res = 0
    for i in range(len(v1)):
        res += v1[i] * v2[i]
    return float(res)

def verifica_convergencia(A, c, sol, e):
    """devolve True se o valor absoluto do erro de todas as equações
    for inferior à precisão, False caso contrário
    verifica_convergencia: tuple x tuple x tuple x float --> bool
    """
    for i in range(len(A)):
        if abs(produto_interno(A[i], sol) - c[i]) >= e:
            return False
    return True

def retira_zeros_diagonal(A, c):
    """devolve uma nova matriz reordenada de forma a não existirem
    valores 0 na diagonal e o vetor com a mesma reordenação
    retira_zero_diagonal: tuple x tuple --> tuple x tuple
    """
    A1 = list(A)
    A = []
    for linha in A1:
        A += [list(linha)] #transformar o tuplo de tuplos numa lista de listas
    c = list(c)
    for i in range(len(A)):
        if A[i][i] == 0:
            for j in range(len(A)):
                if j != i and A[j][i] != 0 and A[i][j] != 0:
                    A[i], A[j] = A[j], A[i]
                    c[i], c[j] = c[j], c[i]
                    break
    A1 = tuple(A)
    A = ()
    for linha in A1:
        A += (tuple(linha),) #transformar a lista de listas num tuplo de tuplos
    c = tuple(c)
    return A, c

def eh_diagonal_dominante(A):
    """devolve True se a matriz for diagonal dominante, False caso contrário
    eh_diagonal_dominante: tuple --> bool
    """
    for i in range(len(A)):
        val_diagonal = abs(A[i][i])
        somatorio = 0
        for e in range(len(A)):
            if e != i:
                somatorio += abs(A[i][e])
        if val_diagonal < somatorio:
            return False      
    return True

def resolve_sistema(A,c,e):
    """devolve um tuplo que é a solução do sistema aplicando o método de Jacobi
    resolve_sistema: tuple x tuple x float --> tuple
    """
    if not type(A) == tuple or not type(c) == tuple or \
        not type(e) == float or not e > 0 or not len(A) == len(c):
        raise ValueError('resolve_sistema: argumentos invalidos')
    for i in range(len(A)):
        if not (isinstance(A[i],tuple) and len(A) == len(A[i])):
            raise ValueError('resolve_sistema: argumentos invalidos')
        for j in range(len(A[i])):
            if not isinstance(A[i][j], (int, float)):
                raise ValueError('resolve_sistema: argumentos invalidos')
    for el in c:
        if not isinstance(el, (int,float)):
            raise ValueError('resolve_sistema: argumentos invalidos')

    A, c = retira_zeros_diagonal(A, c)[0], retira_zeros_diagonal(A, c)[1]
    for i in range(len(A)):
        if A[i][i] == 0:
            raise ValueError('resolve_sistema: argumentos invalidos')

    if not eh_diagonal_dominante(A):
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')

    sol = ()
    for linha in A:
        sol += (0,)

    while not verifica_convergencia(A, c, sol, e):
        sol_nova = ()
        for i in range(len(sol)):
            sol_nova += (sol[i] + (c[i] - produto_interno(A[i], sol)) / A[i][i],)
        sol = sol_nova

    return sol