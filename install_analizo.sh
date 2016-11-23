deb http://www.analizo.org/download/ ./
deb-src http://www.analizo.org/download/ ./
wget -O - http://www.analizo.org/download/signing-key.asc | apt-key add -
apt-get update
apt-get install analizo
