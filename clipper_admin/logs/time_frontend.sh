x=$(grep "; time" $1| sed 's/^.*: //' | sed 's/ms.*//')

let counter=0
for i in $x
do 
	# echo $i
	if [[ "$i" =~ ^[0-9]+$ ]]
    	then
        	((sum += i))
        	((counter += 1))
	fi 
done
echo "sum of all time: $sum ms" 
echo "number of requests: $counter"
echo "average latency: $(($sum/$counter)) ms" 
