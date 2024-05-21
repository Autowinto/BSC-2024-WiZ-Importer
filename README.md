# Meterpreter Wiz Importer

[![Docker Image Status](https://github.com/Autowinto/BSC-2024-WiZ-Importer/actions/workflows/publish.yml/badge.svg)](https://github.com/Autowinto/BSC-2024-WiZ-Importer/actions/workflows/publish.yml)

A tool for discovering and importing power usage data from WiZ light bulbs

## ENV Variables

When running the docker image, it's possible to set environmental variables.

> **API_URL:** Backend URL target. Defaults to `https://localhost:3000`\
> **MEASUREMENT_DELAY:** The time between measurements (in seconds)\
> **DISCOVER_DELAY:** The time between discovering (in seconds)
