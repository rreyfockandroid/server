package main

import (
	"fmt"
	"log"
	"net/http"
	_ "net/http/pprof"
	"server/internal/config"
	shttp "server/internal/server/http"
)

func main() {
	log.Println("starting...")
	cfg := config.Cfg()

	go func() {
		log.Printf("pprof listen on %d", cfg.PprofPort)
		if err := http.ListenAndServe(fmt.Sprintf(":%d", cfg.PprofPort), nil); err != nil {
			log.Fatalf("error when try start pprof server; %v", err)
		}
	}()

	log.Printf("listening on port: %d", cfg.ConfigFlags.Port)

	shttp.RunServer(cfg.ConfigFlags.Port)
}
