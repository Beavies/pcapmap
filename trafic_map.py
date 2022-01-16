###############################################################################
## python3 trafic_map <fichero1> <fichero2>
##
## Parametro 1 = fichero csv exportado de wireshark-conversations
## Parametro 2 = fichero csv mapa de nombres de IP sacado de BBDD inventario
## Output = Fichero PNG 
###############################################################################

import ipaddress
import sys
import os


class Conversacion:
    def __init__(self, a, b, q):
        self.orig = a
        self.dest = b
        self.byte = q
    
    def __eq__(self, other):
        if not isinstance(other, Conversacion):
            return NotImplemented
        else:
            return self.orig==other.orig and self.dest==other.dest
    
    def __hash__(self):
        return hash((self.orig, self.dest))
    
    def isBroadcast(self):
        orig = ipaddress.ip_address(self.orig)
        dest = ipaddress.ip_address(self.dest)
        orign = ipaddress.IPv4Network(self.orig+"/24", False)
        destn = ipaddress.IPv4Network(self.dest+"/24", False)
        
        return (orign.broadcast_address == orig) or (destn.broadcast_address == dest) or orig.is_multicast or dest.is_multicast
    
    def isValid(self):
        try:
            testorig = ipaddress.ip_address(self.orig)
            testdest = ipaddress.ip_address(self.dest)
            return True
        except ValueError:
            print (self.orig+ " or "+self.dest+" no son IPs validas")
            return False
            
conversations = set()
mapaip = dict()

if len(sys.argv) < 3:
    print("Error, falta arxiu csv d'entrada o el arxiu mapa de IP's")
    sys.exit(-1)

# Lectura archivo CSV de conversaciones
with open(sys.argv[1]) as f:
    for line in f:
        words = line.split(';', 3)       #cada linia = IP orig, IP Dest, Bytes
        conv = Conversacion(words[0], words[1], words[2][:-1])
        
        if conv.isValid() and not conv.isBroadcast():
            conversations.add(conv)
            

# Lectura archivo mapa ips
with open(sys.argv[2]) as f:
    for line in f:
        (nom,ip) = line.split(';', 2)
        
        try:
            test = ipaddress.ip_address(ip[:-1])
            mapaip[ip[:-1]] = nom
        except ValueError:
            print (ip[:-1]+" no es una IP valida")


# Creamos fichero de salida
outputfile = sys.argv[1]+".dot"
with open(outputfile, 'w') as f:
    # cabecera
    f.write("graph {\n")
    f.write("\toverlap = false;\n")
    f.write("\tsplines = false;\n")
    f.write("\tmindist = 0.8;\n")
    f.write("\n")
    
    # nodos
    for conv in conversations:
        orig = conv.orig
        dest = conv.dest

        if (orig in mapaip):
            f.write("\t\"{}\" [label=\"{}\\n{}\"]\n".format(mapaip[orig], mapaip[orig],orig))

        if (dest in mapaip):
            f.write("\t\"{}\" [label=\"{}\\n{}\"]\n".format(mapaip[dest], mapaip[dest],dest))

    # conexiones
    for conv in conversations:
        orig = conv.orig
        dest = conv.dest
        iporig = ipaddress.ip_address(orig)
        ipdest = ipaddress.ip_address(dest)
        
        if (iporig.is_private):
            if (orig in mapaip):
                orig = mapaip[orig]
        else:
            orig = "INTERNET"

        if (ipdest.is_private):
            if (dest in mapaip):
                dest = mapaip[dest]
        else:
            dest = "INTERNET"
        
        f.write("\t\"{}\" -- \"{}\"\n".format(orig, dest))
    
    # fin
    f.write("}\n")
    
os.system("neato -Tpng {} > {}".format(outputfile, outputfile+".png"))
#os.system("rm -f {}".format(outputfile))
    
