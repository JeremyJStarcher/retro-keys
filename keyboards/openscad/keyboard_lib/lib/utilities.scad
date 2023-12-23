function reverse(list) = len(list) > 0 ? [for (i = [1:len(list)]) list[len(list)-i]] : [];
function pop(list) = len(list) > 0 ? [for (i = [0:len(list)-1]) if (i != 0) list[i]] : [];
