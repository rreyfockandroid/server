package http

import (
	"fmt"
	"net/http"
	"server/internal/config"
	"strconv"
	"strings"
)

var handlers = []string{
	"/health",
	"/",
	"/info",
}

var handlersMap = map[string]func(w http.ResponseWriter, r *http.Request){
	handlers[0]: healtHanlder,
	handlers[1]: rootHandler,
	handlers[2]: infoHander,
}

func infoHander(w http.ResponseWriter, r *http.Request) {
	// for key, values := range r.Header {
	// 	log.Printf("	'%s': %s\n", key, strings.Join(values, ", "))
	// }

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
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
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
