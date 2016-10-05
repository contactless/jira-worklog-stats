#!/bin/bash

q  -T -d, -H "SELECT author, SUM(seconds)/3600. FROM - GROUP BY author " < $1