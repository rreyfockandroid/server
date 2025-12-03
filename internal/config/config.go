package config

import (
	"flag"
	"sync"
)

var conf Config
var once sync.Once

type Config struct {
	ConfigFlags ConfigFlags
	PprofPort   int
}

type ConfigFlags struct {
	Port int
}

func Cfg() Config {
	once.Do(func() {
		conf = Config{
			PprofPort:   6060,
			ConfigFlags: configFlags(),
		}
	})
	return conf
}

func configFlags() ConfigFlags {
	port := flag.Int("port", 8081, "port to listen on")
	flag.Parse()
	return ConfigFlags{
		Port: *port,
	}
}
