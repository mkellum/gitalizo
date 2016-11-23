echo deb http://www.analizo.org/download/ ./ >> /etc/apt/sources.list.d/analizo.list
echo deb-src http://www.analizo.org/download/ ./ >> /etc/apt/sources.list.d/analizo.list
apt-get update
yes Y | apt-get install analizo
wget -O - http://www.analizo.org/download/signing-key.asc | apt-key add -
apt-get update
yes Y | apt-get install analizo
