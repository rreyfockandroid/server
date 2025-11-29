package http

import (
	"fmt"
	"net/http"
)

func handleFunc(path string, handler func(w http.ResponseWriter, r *http.Request)) {
	http.HandleFunc(path, handler)
}

func startServer(port int) {
	http.ListenAndServe(fmt.Sprintf(":%d", port), nil)
}
