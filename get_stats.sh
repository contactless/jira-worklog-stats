#!/bin/bash
BEGIN=`date +'%Y-%m-01' --date="-1 month"`
END=`date +'%Y-%m-01'`

echo "1 Month from ${BEGIN} to ${END}:"

q  -T -d, -H "SELECT author, SUM(seconds)/3600. FROM - WHERE started > \"${BEGIN}\" AND started < \"${END}\" GROUP BY author " <  $1 


echo "================="

echo "Total:"
q  -T -d, -H "SELECT author, SUM(seconds)/3600. FROM - GROUP BY author " < $1

#q  -T -d, -H "SELECT author, SUM(seconds)/3600. FROM - WHERE created > '2016-11-01' AND created < '2016-12-01' GROUP BY author " <  data/output_20161202.csv 

