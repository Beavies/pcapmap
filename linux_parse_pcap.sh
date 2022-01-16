#!/bin/bash

if [ $# -lt 2 ]
then
    echo "Nº de parametros incorrectos"
    echo "se requiere 2 parametros"
    echo "   Param1 = fichero tcpdump pcap"
    echo "   Param2 = fichero de salida"
    exit 1
fi

## PARAMS
pcapfile="$1"
outputfile="$2"
temp1=$(mktemp -p .)
temp2=$(mktemp -p .)

## Pillamos ip origen y destino de pcap (tcp y udp)
tcpdump -p ip and tcp -nnr "$pcapfile" | cut -d \  -f 3,4,5 | sort -u | tr -d : | tr \> , | sed -e 's/\./,/4' -e 's/\./,/7' | tr -d \   > $temp1

tcpdump -p ip and udp -nnr "$pcapfile" | cut -d \  -f 3,4,5 | sort -u | tr -d : | tr \> , | sed -e 's/\./,/4' -e 's/\./,/7' | tr -d \   >> $temp1

## eliminamos los puertos tcp o udp
cat $temp1 | cut -d \, -f 1,3 | sort -u | sed -e 's/\,/"\ --\ "/' -e 's/^/"/' -e 's/$/";/' > $temp2

## creamos el archivo DOT
echo "graph grafico {" > "$outputfile".dot
    cat $temp2 >> "$outputfile".dot
echo "}" >> "$outputfile".dot

rm -f $temp1 
rm -f $temp2

## creamos el grafico
cat "$outputfile".dot | circo -Tpng -o "$outputfile"_circo.png
cat "$outputfile".dot | dot -Tpng -o "$outputfile"_tree.png
