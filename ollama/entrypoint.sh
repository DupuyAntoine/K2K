#!/usr/bin/env bash

ollama serve &
sleep 5
ollama pull llama3

wait $!