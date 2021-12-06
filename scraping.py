from bs4 import BeautifulSoup

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


if __name__ == "__main__":
    infile = open("prueba.xml","r")
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    fecha=getDate(soup)
    proveedor='BIOMAX SA'
    tipos=getTypes(soup) 
    subtotales=getSubTotal(soup)