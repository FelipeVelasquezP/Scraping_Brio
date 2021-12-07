from bs4 import BeautifulSoup
import csv
import pandas as pd

def getDate(data):
    dates = data.find_all('cbc:IssueDate')
    return dates[0].get_text()

def getTypes(data):
    auxT=[]
    types=data.find_all('cbc:Description')
    for type in types:
    #   iter=type.get_text().split()[0]
    #   if iter=='Bioacem': iter='ACPM'
      auxT.append(type.get_text())
    return auxT

def getSubTotal(data):
    subtotales = data.find_all('cbc:LineExtensionAmount')
    subtotales.pop(0)
    auxS=[]
    for subtotal in subtotales:
      iter=float(subtotal.get_text())
      auxS.append(iter)
    return auxS


def getCantidad(data):
    cantidades = data.find_all('cbc:BaseQuantity')
    auxC=[]
    for cantidad in cantidades:
      iter=float(cantidad.get_text())
      auxC.append(iter)
    return auxC

def getPrecioCompra(data):
    cantidades = data.find_all('cbc:TaxInclusiveAmount')
    return cantidades

def getValores(data):
    valores = data.find_all('cbc:TaxAmount')
    auxI=[]
    for valor in valores:
      iter=float(valor.get_text())
      auxI.append(iter)
    return list(set(auxI))

def organizarValores(valores,tipos):
    tamTipos=len(tipos)
    if tamTipos==1:
        iva=[valores[3]]
        sobretasa=[valores[2]]
        soldicom=[valores[4]]
    elif tamTipos==2:
        iva=[valores[3],valores[14]]
        sobretasa=[valores[2],valores[9]]
        soldicom=[valores[13],valores[6]]
    else:
        pass
    return iva,sobretasa,soldicom


def generateCSV(fecha,proveedor,cantidades,tipos,subtotales,iva,sobretaas,soldicom):
    fields = ['Fecha', 'Proveedor', 'Cantidad','Tipo','Valor Corriente','Iva','Valor Sobretasa','Soldicom']
    rows = []

    for i in range(len(tipos)):
        row = [fecha, proveedor,cantidades[i],tipos[i],subtotales[i],iva[i],sobretaas[i],soldicom[i]]
        rows.append(row)

    with open('prueba.xlsx', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    eliminarFilasVacias()

def eliminarFilasVacias():
    df = pd.read_csv('prueba.xlsx')
    df.to_csv('prueba.xlsx', index=False)


if __name__ == "__main__":
    infile = open("prueba1.xml","r")
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    fecha=getDate(soup)
    proveedor='BIOMAX SA'
    tipos=getTypes(soup) 
    subtotales=getSubTotal(soup)
    cantidades=getCantidad(soup)
    # precioCompra=getPrecioCompra(soup)
    valores=getValores(soup)
    iva,sobretaas,soldicom=organizarValores(valores,tipos)
    generateCSV(fecha,proveedor,cantidades,tipos,subtotales,iva,sobretaas,soldicom)
    print(fecha,proveedor,cantidades,tipos,subtotales,iva,sobretaas,soldicom)