def GetData():

    #organizando dados para import posterior
    confs = []
    data = []

    #fronteira1
    conf1 = str(input(f"A fronteira Norte tem contato com fluido externo (y/n)? "))
    confs.append(conf1)
    if(conf1 == 'y'):
        h1 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
        T_1 = int(input("Digite a temperatura do fluido: "))
        data.append( (T_1, h1) )
    elif(conf1 == 'n'):
        h1 = 0
        T_1 = int(input("Digite a temperatura da fronteira: "))
        data.append( (T_1, h1) )

    #fronteira2
    conf2 = str(input(f"A fronteira Leste tem contato com fluido externo (y/n)? "))
    confs.append(conf2)
    if(conf2 == 'y'):
        h2 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
        T_2 = int(input("Digite a temperatura do fluido: "))
        data.append( (T_2, h2) )
    elif(conf2  == 'n'):
        h2 = 0
        T_2 = int(input("Digite a temperatura da fronteira: "))
        data.append( (T_2, h2) )

    #fronteira3
    conf3 = str(input(f"A fronteira Sul tem contato com fluido externo (y/n)? "))
    confs.append(conf3)
    if(conf3 == 'y'):
        h3 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
        T_3 = int(input("Digite a temperatura do fluido: "))
        data.append( (T_3, h3) )
    elif(conf3 == 'n'):
        h3 = 0
        T_3 = int(input("Digite a temperatura da fronteira: "))
        data.append( (T_3, h3) )

    #fronteira4
    conf4 = str(input(f"A fronteira Oeste tem contato com fluido externo (y/n)? "))
    confs.append(conf4)
    if(conf4 == 'y'):
        h4 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
        T_4 = int(input("Digite a temperatura do fluido: "))
        data.append( (T_4, h4) )
    elif(conf4 == 'n'):
        h4 = 0
        T_4 = int(input("Digite a temperatura da fronteira: "))
        data.append( (T_4, h4) )

    #Dimensões do condutor
    lx = int(input('Digite o comprimento do condutor analisado: '))
    ly = int(input('Digite a largura do condutor analisado: '))

    #Propriedades do condutor
    k = float(input('Digite a condutividade térmica do condutor: '))

    #Número de nodos a ser utilizado
    nx = int(input('Digite o número de nós na direção x: '))
    ny = int(input('Digite o número de nós na direção y: '))

    return confs, data, lx, ly, nx, ny, k
