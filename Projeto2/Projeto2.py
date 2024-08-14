# Fundamentos da Programação 2022/23
# Raquel Rodrigues - ist1106322

def cria_gerador(b, s):
    """
    cria_gerador: int x int -> gerador
    devolve o gerador correspondente ao número de bits e à seed introduzidos
    """
    if not(type(b) == int and (b == 32 or b == 64) and \
        type(s) == int and 0 < s <= 2**b - 1):
        raise ValueError('cria_gerador: argumentos invalidos')
    return {'bits': b, 'estado': s}

def cria_copia_gerador(g):
    """
    cria_copia_gerador: gerador -> gerador
    devolve uma cópia nova do gerador
    """
    if not eh_gerador(g):
        raise ValueError('cria_copia_gerador: argumentos invalidos')
    return g.copy()

def obtem_estado(g):
    """
    obtem_estado: gerador -> int
    devolve o estado atual do gerador g
    """
    return g['estado']

def define_estado(g, s):
    """
    define_estado: gerador x int -> int
    define o novo valor do estado de g como sendo s e devolve s
    """
    g['estado'] = s
    return s

def atualiza_estado(g):
    """
    atualiza_estado: gerador -> int
    atualiza o estado de g, de acordo com o algoritmo xorshift de geração
    de números pseudoaleatórios e devolve esse valor
    """
    s = obtem_estado(g)
    if g['bits'] == 32:
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= (s >> 17) & 0xFFFFFFFF
        s ^= (s << 5) & 0xFFFFFFFF
    else:
        s ^= (s << 13) & 0xFFFFFFFFFFFFFFFF
        s ^= (s >> 7) & 0xFFFFFFFFFFFFFFFF
        s ^= (s << 17) & 0xFFFFFFFFFFFFFFFF
    return define_estado(g, s)

def eh_gerador(arg):
    """
    eh_gerador: universal -> bool
    devolve True se o argumento for um TAD gerador, False caso contrário
    """
    return isinstance(arg, dict) and len(arg) == 2 and 'bits' in arg \
        and 'estado' in arg and type(arg['bits']) == int and (arg['bits'] == 32 \
        or arg['bits'] == 64) and type(arg['estado']) == int and \
        0 < arg['estado'] < 2**arg['bits'] - 1

def geradores_iguais(g1, g2):
    """
    geradores_iguais: gerador x gerador -> bool
    devolve True apenas se g1 e g2 forem geradores iguais
    """
    return eh_gerador(g1) and eh_gerador(g2) and g1['bits'] == g2['bits'] \
        and obtem_estado(g1) == obtem_estado(g2)

def gerador_para_str(g):
    """
    gerador_para_str: gerador -> str
    devolve a cadeia de caracteres que representa o seu argumento
    """
    return 'xorshift{}(s={})'.format(g['bits'], obtem_estado(g))

def gera_numero_aleatorio(g, n):
    """
    gera_numero_aleatorio: gerador x int -> int
    atualiza o estado de g e devolve um número aleatório no intervalo [1,n]
    """
    return 1 + atualiza_estado(g) % n

def gera_carater_aleatorio(g, c):
    """
    gera_carater_aleatorio: gerador x str -> str
    atualiza o estado de g e devolve um caráter aleatório no intervalo
    entre 'A' e o caráter maiúsculo c
    """
    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cadeia = abc[:abc.index(c) + 1]
    return cadeia[atualiza_estado(g) % len(cadeia)]

def cria_coordenada(col, lin):
    """
    cria_coordenada: str x int -> coordenada
    devolve a coordenada correspondente à linha e à coluna introduzidas
    """
    if not(type(col) == str and len(col) == 1 and 'A' <= col <= 'Z' and \
        type(lin) == int and 0 < lin < 100):
        raise ValueError('cria_coordenada: argumentos invalidos')
    return col, lin

def obtem_coluna(c):
    """
    obtem_coluna: coordenada -> str
    devolve a coluna da coordenada c
    """
    return c[0]

def obtem_linha(c):
    """
    obtem_linha: coordenada -> int
    devolve a linha da coordenada c
    """
    return c[1]

def eh_coordenada(arg):
    """
    eh_coordenada: universal -> bool
    devolve True se o argumento for um TAD coordenada, False caso contrário
    """
    return isinstance(arg, tuple) and len(arg) == 2 and type(arg[0]) == str \
        and len(arg[0]) == 1 and 'A' <= arg[0] <= 'Z' and \
        type(arg[1]) == int and 0 < arg[1] < 100

def coordenadas_iguais(c1, c2):
    """
    coordenadas_iguais: coordenada x coordenada -> bool
    devolve True se c1 e c2 são coordenadas iguais
    """
    return eh_coordenada(c1) and eh_coordenada(c2) and \
        obtem_coluna(c1) == obtem_coluna(c2) and \
        obtem_linha(c1) == obtem_linha(c2)

def coordenada_para_str(c):
    """
    coordenada_para_str: coordenada -> str
    devolve a cadeia de caracteres que representa o seu argumento
    """
    if obtem_linha(c) < 10:
        return obtem_coluna(c) + '0' + str(obtem_linha(c))
    else:
        return obtem_coluna(c) + str(obtem_linha(c))

def str_para_coordenada(s):
    """
    str_para_coordenada: str -> coordenada
    devolve a coordenada representada pelo argumento
    """
    return cria_coordenada(s[0], int(s[1:]))

def obtem_coordenadas_vizinhas(c):
    """
    obtem_coordenadas_vizinhas: coordenada -> tuplo
    devolve um tuplo com as coordenadas vizinhas a c, começando pela
    coordenada na diagonal acima-esquerda e seguindo no sentido horário
    """
    #números a adicionar sucessivamente à coluna e à linha de c para
    #obter as coordenadas vizinhas em sentido horário
    add_num_col = [-1, 0, 1, 1, 1, 0, -1, -1]
    add_num_lin = [-1, -1, -1, 0, 1, 1, 1, 0]

    def aux(c, n_vizinhas, intervalo_col, intervalo_lin):
        vizinhas = ()
        for i in range(n_vizinhas):
            vizinhas += (cria_coordenada(chr(ord(obtem_coluna(c)) + \
                intervalo_col[i]), obtem_linha(c) + intervalo_lin[i]), )
        return vizinhas

    if obtem_coluna(c) == 'A':
        if obtem_linha(c) == 1:
            return aux(c, 3, add_num_col[3:6], add_num_lin[3:6])
        elif obtem_linha(c) == 99:
            return aux(c, 3, add_num_col[1:4], add_num_lin[1:4])
        else:
            return aux(c, 5, add_num_col[1:6], add_num_lin[1:6])

    elif obtem_coluna(c) == 'Z':
        if obtem_linha(c) == 1:
            return aux(c, 3, add_num_col[5:8], add_num_lin[5:8])
        elif obtem_linha(c) == 99:
            return aux(c, 3, add_num_col[0:2] + [add_num_col[-1]], add_num_lin[0:2] + [add_num_lin[-1]])
        else:
            return aux(c, 5, add_num_col[0:2] + add_num_col[5:8], add_num_lin[0:2] + add_num_lin[5:8])
    
    else:
        if obtem_linha(c) == 1:
            return aux(c, 5, add_num_col[3:8], add_num_lin[3:8])
        elif obtem_linha(c) == 99:
            return aux(c, 5, add_num_col[:4] + [add_num_col[-1]], add_num_lin[:4] + [add_num_lin[-1]])
        else:
            return aux(c, 8, add_num_col, add_num_lin)

def obtem_coordenada_aleatoria(c, g):
    """
    obtem_coordenada_aleatoria: coordenada x gerador -> coordernada
    devolve uma coordenada gerada aleatoriamente
    """
    return cria_coordenada(gera_carater_aleatorio(g, obtem_coluna(c)), \
        gera_numero_aleatorio(g, obtem_linha(c)))

def cria_parcela():
    """
    cria_parcela: {} -> parcela
    devolve uma parcela tapada sem mina escondida
    """
    return {'estado': 'tapada', 'c/ mina': 'não'}

def cria_copia_parcela(p):
    """
    cria_copia_parcela: parcela -> parcela
    devolve uma cópia da parcela
    """
    if not eh_parcela(p):
        raise ValueError('cria_copia_parcela: argumentos invalidos')
    return p.copy()

def limpa_parcela(p):
    """
    limpa_parcela: parcela -> parcela
    modifica o estado da parcela para limpa e devolve a própria parcela
    """
    p['estado'] = 'limpa'
    return p

def marca_parcela(p):
    """
    marca_parcela: parcela -> parcela
    modifica o estado da parcela para marcada com uma bandeira e devolve
    a própria parcela
    """
    p['estado'] = 'marcada'
    return p

def desmarca_parcela(p):
    """
    desmarca_parcela: parcela -> parcela
    modifica o estado da parcela para tapada e devolve a própria parcela
    """
    p['estado'] = 'tapada'
    return p

def esconde_mina(p):
    """
    esconde_mina: parcela -> parcela
    esconde uma mina na parcela e devolve a própria parcela
    """
    p['c/ mina'] = 'sim'
    return p

def eh_parcela(arg):
    """
    eh_parcela: universal -> bool
    devolve True caso o argumento seja um TAD parcela, False caso contrário
    """
    return isinstance(arg, dict) and len(arg) == 2 and 'estado' in arg \
        and 'c/ mina' in arg and (arg['estado'] == 'tapada' or \
        arg['estado'] == 'limpa' or arg['estado'] == 'marcada') and \
        (arg['c/ mina'] == 'sim' or arg['c/ mina'] == 'não')

def eh_parcela_tapada(p):
    """
    eh_parcela_tapada: parcela -> bool
    devolve True se a parcela estiver tapada, False caso contrário
    """
    return p['estado'] == 'tapada'

def eh_parcela_marcada(p):
    """
    eh_parcela_marcada: parcela -> bool
    devolve True se a parcela estiver marcada com bandeira, 
    False caso contrário
    """
    return p['estado'] == 'marcada'

def eh_parcela_limpa(p):
    """
    eh_parcela_limpa: parcela -> bool
    devolve True se a parcela estiver limpa, False caso contrário
    """
    return p['estado'] == 'limpa'

def eh_parcela_minada(p):
    """
    eh_parcela_minada: parcela -> bool
    devolve True se a parcela esconder uma mina, False caso contrário
    """
    return p['c/ mina'] == 'sim'

def parcelas_iguais(p1, p2):
    """
    parcelas_iguais: parcela x parcela -> bool
    devolve True apenas se p1 e p2 são parcelas iguais
    """
    return eh_parcela(p1) and eh_parcela(p2) and p1['estado'] == p2['estado'] \
        and p1['c/ mina'] == p2['c/ mina']

def parcela_para_str(p):
    """
    parcela_para_str: parcela -> str
    devolve a cadeia de caracteres que representa a parcela em função
    do seu estado
    """
    if p['estado'] == 'tapada':
        return '#'
    elif p['estado'] == 'marcada':
        return '@'
    elif p['c/ mina'] == 'não':
        return '?'
    else:
        return 'X'

def alterna_bandeira(p):
    """
    alterna_bandeira: parcela -> bool
    desmarca a parcela se esta estiver marcada e marca se estiver tapada,
    devolvendo True, caso contrário, devolve False
    """
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    else:
        return False

def cria_campo(c, l):
    """
    cria_campo: str x int -> campo
    recebe a última coluna e última linha e devolve o campo de tamanho
    pretendido formado por parcelas tapadas sem minas
    """
    if not(type(c) == str and len(c) == 1 and type(l) == int and \
        'A' <= c <= 'Z' and 0 < l < 100):
        raise ValueError('cria_campo: argumentos invalidos')
    m = []
    for i in range(l):
        linha = []
        for j in range(ord(c) - ord('A') + 1):
            linha += [cria_parcela()]
        m += [linha]
    return m

def cria_copia_campo(m):
    """
    cria_copia_campo: campo -> campo
    devolve uma cópia do campo
    """
    if not eh_campo(m):
        raise ValueError('cria_copia_campo: argumentos invalidos')
    copia_m = []
    for linha in m:
        copia_linha = []
        for parcela in linha:
            copia_linha += [cria_copia_parcela(parcela)]
        copia_m += [copia_linha]
    return copia_m

def obtem_ultima_coluna(m):
    """
    obtem_ultima_coluna: campo -> str
    devolve a cadeia de caracteres que corresponde à última coluna do campo
    """
    return chr(len(m[0]) + 64)

def obtem_ultima_linha(m):
    """
    obtem_ultima_linha: campo -> int
    devolve o valor inteiro que corresponde à última linha do campo
    """
    return len(m)

def obtem_parcela(m, c): 
    """
    obtem_parcela: campo x coordenada -> parcela
    devolve a parcela do campo m que se encontra na coordenada c
    """
    return m[obtem_linha(c) - 1][ord(obtem_coluna(c)) - 65]

def obtem_coordenadas(m, s):
    """
    obtem_coordenadas: campo x str -> tuplo
    devolve o tuplo formado pelas coordenadas ordenadas das parcelas
    dependendo do valor de s
    """        
    def obtem_coordenadas_aux(m, f_estado):
        coordenadas = ()
        for linha in range(obtem_ultima_linha(m)):
            for coluna in range((ord(obtem_ultima_coluna(m)) - 64)):
                if f_estado(m[linha][coluna]):
                    coordenadas += (cria_coordenada(chr(coluna + 65), \
                        linha + 1),)
        return coordenadas
    if s == 'limpas':
        return obtem_coordenadas_aux(m, eh_parcela_limpa)
    elif s == 'tapadas':
        return obtem_coordenadas_aux(m, eh_parcela_tapada)
    elif s == 'marcadas':
        return obtem_coordenadas_aux(m, eh_parcela_marcada)
    else: 
        return obtem_coordenadas_aux(m, eh_parcela_minada)

def obtem_numero_minas_vizinhas(m, c):
    """
    obtem_numero_minas_vizinhas: campo x coordenada -> int
    devolve o número de parcelas vizinhas da parcela na coordenada c
    que escondem minas
    """
    numero_minas_vizinhas = 0
    for coordenada in obtem_coordenadas_vizinhas(c):
        if coordenada in obtem_coordenadas(m, 'minadas'):
            numero_minas_vizinhas += 1
    return numero_minas_vizinhas 

def eh_campo(arg):
    """
    eh_campo: universal -> bool
    devolve True caso o argumento seja um TAD campo, False caso contrário
    """
    if isinstance(arg, list) and 0 < len(arg) < 100 and 0 < len(arg[0]) <= 26:
        for i in range(len(arg)):
            if isinstance(arg[i], list):
                if len(arg[i]) != len(arg[0]):
                    return False
                for el in arg[i]:
                    if not eh_parcela(el):
                        return False
            else:
                return False
        return True
    return False
                
def eh_coordenada_do_campo(m, c):
    """
    eh_coordenada_do_campo: campo x coordenada -> bool
    devolve True se c é uma coordenada válida dentro do campo m
    """
    return 'A' <= obtem_coluna(c) <= obtem_ultima_coluna(m) and \
        0 < obtem_linha(c) <= obtem_ultima_linha(m)

def campos_iguais(m1, m2):
    """
    campos_iguais: campo x campo -> bool
    devolve True apenas se m1 e m2 forem campos iguais
    """
    if eh_campo(m1) and eh_campo(m2) and \
        obtem_ultima_coluna(m1) == obtem_ultima_coluna(m2) and \
        obtem_ultima_linha(m1) == obtem_ultima_linha(m2):
        for linha in range(len(m1)):
            for parcela in range(len(m1[0])):
                if not parcelas_iguais(m1[linha][parcela], m2[linha][parcela]):
                    return False
        return True
    return False

def campo_para_str(m):
    """
    campo_para_str: campo -> str
    devolve uma cadeia de caracteres que representa o campo de minas
    """
    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    campo = '   ' + abc[:abc.index(obtem_ultima_coluna(m)) + 1] + \
        '\n  +{}+\n'.format('-'*(ord(obtem_ultima_coluna(m)) - 64))
    for linha in range(obtem_ultima_linha(m)):
        campo += coordenada_para_str(('A', linha + 1))[1:] + '|'
        for coluna in range(ord(obtem_ultima_coluna(m)) - 64):
            if parcela_para_str(obtem_parcela(m, \
            cria_coordenada(chr(coluna + 65), linha + 1))) == '?':
                if obtem_numero_minas_vizinhas(m, cria_coordenada(\
                    chr(coluna + 65), linha + 1)) == 0:
                    campo += ' '
                else:
                    campo += str(obtem_numero_minas_vizinhas(m, \
                        cria_coordenada(chr(coluna + 65), linha + 1)))
            else:
                campo += parcela_para_str(obtem_parcela(m, \
                cria_coordenada(chr(coluna + 65), linha + 1)))
        campo += '|\n'
    campo += '  +{}+'.format('-'*(ord(obtem_ultima_coluna(m)) - 64))
    return campo

def coloca_minas(m, c, g, n):
    """
    coloca_minas: campo x coordenada x gerador x int -> campo
    esconde n minas em parcelas dentro do campo e devolve o campo
    """
    for i in range(n):
        coord_nova = obtem_coordenada_aleatoria(cria_coordenada( \
        obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
        while coordenadas_iguais(coord_nova, c) or coord_nova in \
            obtem_coordenadas_vizinhas(c) or \
            eh_parcela_minada(obtem_parcela(m, coord_nova)):
            coord_nova = obtem_coordenada_aleatoria(cria_coordenada( \
            obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
        esconde_mina(obtem_parcela(m, coord_nova))
    return m

def limpa_campo(m, c):
    """
    limpa_campo: campo x coordenada -> campo
    limpa a parcela na coordenada c e devolve o campo. Se não houver nenhuma
    mina vizinha escondida, limpa todas as parcelas vizinhas tapadas
    """
    def aux(m, lista_coord):
        if len(lista_coord) == 0:
            return m
        else:
            c = lista_coord[0]
            limpa_parcela(obtem_parcela(m, c))
            if obtem_numero_minas_vizinhas(m, c) == 0 and not \
                eh_parcela_minada(obtem_parcela(m, c)):
                for coordenada in obtem_coordenadas_vizinhas(c):
                    if eh_coordenada_do_campo(m, coordenada) and \
                        eh_parcela_tapada(obtem_parcela(m, coordenada)) and \
                        coordenada not in lista_coord:
                        lista_coord += [coordenada]           
            return aux(m, lista_coord[1:])
    if eh_parcela_limpa(obtem_parcela(m, c)):
        return m
    else:
        return aux(m, [c])

def jogo_ganho(m):
    """
    jogo_ganho: campo -> bool
    devolve True se todas as parcelas sem minas se encontram limpas,
    False caso contrário
    """
    nao_limpas = obtem_coordenadas(m, 'tapadas') + obtem_coordenadas(m, 'marcadas')
    for coordenada in nao_limpas:
        if not eh_parcela_minada(obtem_parcela(m, coordenada)):
            return False
    return True

def turno_jogador(m):
    """
    turno_jogador: campo -> bool
    oferece ao jogador a opção de escolher uma ação e uma coordenada,
    executando essa ação. Devolve False caso o jogador tenha limpo uma 
    parcela com mina, True caso contrário.
    """
    acao = ''
    c = ''
    while not (acao == 'L' or acao == 'M'):
        acao = input('Escolha uma ação, [L]impar ou [M]arcar:')

    def cond(c): #garantir que podemos converter c[1:] para int
        try:
            int(c[1:])
        except ValueError:
            return False
        return True

    while not (len(c) == 3 and 'A' <= c[0] <= 'Z' and cond(c) == True and \
        eh_coordenada_do_campo(m, str_para_coordenada(c))):
        c = input('Escolha uma coordenada:')

    c = str_para_coordenada(c)
    if acao == 'L':
        limpa_campo(m, c)
    else:
        alterna_bandeira(obtem_parcela(m, c))
    return not(acao == 'L' and eh_parcela_minada(obtem_parcela(m, c)))

def minas(c, l, n, d, s):
    """
    minas: str x int x int x int x int -> bool
    permite jogar ao jogo das minas. Devolve True se o jogador conseguir
    ganhar o jogo, False caso contrário.
    """
    if not(type(c) == str and len(c) == 1 and type(l) == int and \
        (('A' <= c <= 'Z' and 4 <= l < 100) or ('D' <= c <= 'Z' and \
        1 <= l <= 99))):
        raise ValueError('minas: argumentos invalidos')
    if not(type(d) == int and (d == 32 or d == 64) and type(s) == int \
        and s > 0 and type(n) == int and 0 < n <= (ord(c) - 64)*l - 9):
        raise ValueError('minas: argumentos invalidos')

    m = cria_campo(c, l)
    g = cria_gerador(d, s)
    n_marcadas = 0
    print(f'   [Bandeiras {n_marcadas}/{n}]\n{campo_para_str(m)}')
    c_inicial = ''

    def cond(c): #garantir que podemos converter c[1:] para int
        try:
            int(c[1:])
        except ValueError:
            return False
        return True

    while not (len(c_inicial) == 3 and \
        'A' <= c_inicial[0] <= 'Z' and cond(c_inicial) == True and \
        eh_coordenada_do_campo(m, str_para_coordenada(c_inicial))):
        c_inicial = input('Escolha uma coordenada:')

    #jogada inicial
    c_inicial = str_para_coordenada(c_inicial)
    m = limpa_campo(coloca_minas(m, c_inicial, g, n), c_inicial)
    print(f'   [Bandeiras {n_marcadas}/{n}]\n{campo_para_str(m)}')

    #jogadas restantes
    while not jogo_ganho(m):
        turno = turno_jogador(m)
        n_marcadas = len(obtem_coordenadas(m, 'marcadas'))
        print(f'   [Bandeiras {n_marcadas}/{n}]\n{campo_para_str(m)}')
        if not turno:
            print('BOOOOOOOM!!!')
            return False
    print('VITORIA!!!')
    return True