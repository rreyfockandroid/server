make ca-gen
make cert-gen

Firefox -> import certyfikatu - zaufany
about:preferences#privacy
Settings → Privacy & Security → Certificates → View Certificates → Authorities → Import
Wybierz:
./services/nginx/storage/certs/rootCA.crt
zaznacz: Trust this CA to identify websites

yappi
sudo apt install kcachegrind
kcachegrind profile.callgrind

zmiana 
pip install pyprof2calltree
pyprof2calltree -i last_request.pstat -o output.callgrind