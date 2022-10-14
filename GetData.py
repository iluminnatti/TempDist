#fronteira1
conf1 = str(input(f"A fronteira 1 tem contato com fluido externo (y/n)? "))
if(conf1 == 'y'):
    h1 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
    T_c_1 = int(input("Digite a temperatura do fluido: "))
elif(conf1 == 'n'):
    T_1 = int(input("Digite a temperatura da fronteira: "))

#fronteira2
conf2 = str(input(f"A fronteira 2 tem contato com fluido externo (y/n)? "))
if(conf2 == 'y'):
    h2 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
    T_c_2 = int(input("Digite a temperatura do fluido: "))
elif(conf2  == 'n'):
    T_2 = int(input("Digite a temperatura da fronteira: "))

#fronteira3
conf3 = str(input(f"A fronteira 3 tem contato com fluido externo (y/n)? "))
if(conf3 == 'y'):
    h3 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
    T_c_3 = int(input("Digite a temperatura do fluido: "))
elif(conf3 == 'n'):
    T_3 = int(input("Digite a temperatura da fronteira: "))

#fronteira4
conf4 = str(input(f"A fronteira 4 tem contato com fluido externo (y/n)? "))
if(conf4 == 'y'):
    h4 = float(input("Digite o coeficiente de transferência de calor por condução do fluido (h): "))
    T_c_4 = int(input("Digite a temperatura do fluido: "))
elif(conf4 == 'n'):
    T_4 = int(input("Digite a temperatura da fronteira: "))


