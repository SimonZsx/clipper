ids_str="`docker ps -a | grep c1_speechRec | head -n 2 | cut -d " " -f1`"
ids_arr=(${ids_str})
echo ${ids_arr[@]}
#c1_container_id=${ids_arr}[1]
#echo $c1_container_id
