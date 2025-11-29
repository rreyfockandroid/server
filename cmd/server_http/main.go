package main

import (
	"log"
	"server/internal/config"
	"server/internal/server/http"
)

func main() {
	log.Println("starting...")
	cfg := config.Cfg()
	log.Printf("listening on port: %d", cfg.ConfigFlags.Port)

	http.RunServer(cfg.ConfigFlags.Port)
}
