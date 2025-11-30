package http

import (
	"fmt"
	"log"
	"net/http"
	"server/internal/config"
	"strconv"
	"strings"
)

var handlers = []string{
	"/health",
	"/",
	"/info",
	"/generate",
}

var handlersMap = map[string]func(w http.ResponseWriter, r *http.Request){
	handlers[0]: healtHanlder,
	handlers[1]: rootHandler,
	handlers[2]: infoHander,
	handlers[3]: generateDataHandler,
}

func generateDataHandler(w http.ResponseWriter, r *http.Request) {
	log.Println(strconv.Itoa(config.Cfg().ConfigFlags.Port), " generate Data Handler called ", r.Header.Get("Server-Name"))

	fail := r.URL.Query().Get("fail")
	if fail != "" {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Simulated failure as requested\n"))
		return
	}

	buffer := strings.Builder{}
	buffer.WriteString(strconv.Itoa(config.Cfg().ConfigFlags.Port))
	buffer.WriteString("\n")

	for i := range 1000 {
		buffer.WriteString(strconv.Itoa(i))
		buffer.WriteString(" some generated data line ")
		buffer.WriteString("\n")
	}

	w.Write([]byte(buffer.String()))
}

func infoHander(w http.ResponseWriter, r *http.Request) {
	log.Println("Info Handler called ", r.Header.Get("Server-Name"))

	port := config.Cfg().ConfigFlags.Port
	buffer := strings.Builder{}

	buffer.WriteString("Server Info: Version 1.0.0")
	buffer.WriteString("\n")
	buffer.WriteString("Listening on port: ")
	buffer.WriteString(strconv.Itoa(port))
	buffer.WriteString("\n")
	for key, values := range r.Header {
		buffer.WriteString(fmt.Sprintf("	'%s': %s\n", key, strings.Join(values, ", ")))
	}
	w.Write([]byte(buffer.String()))
}

func healtHanlder(w http.ResponseWriter, r *http.Request) {
	log.Println("Health Handler called ", r.Header.Get("Server-Name"))

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Root Handler called ", r.Header.Get("Server-Name"))

	buff := strings.Builder{}
	for _, path := range handlers {
		buff.WriteString(path)
		buff.WriteString("\n")
	}
	w.Write([]byte(buff.String()))
}

func RunServer(port int) {
	for path, handler := range handlersMap {
		handleFunc(path, handler)
	}
	startServer(port)
}
