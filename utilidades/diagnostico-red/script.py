"""Comprueba DNS y TCP; no cambia la configuración de red."""
import argparse
import json
import socket
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("servidor", help="Nombre DNS o dirección IP, sin https://")
    parser.add_argument("--puerto", type=int, default=443)
    parser.add_argument("--espera", type=float, default=5, help="Segundos por conexión TCP")
    args = parser.parse_args()
    if not 1 <= args.puerto <= 65535 or not 0 < args.espera <= 60:
        parser.error("Puerto: 1-65535; espera: mayor que 0 y hasta 60 segundos.")
    started = time.monotonic()
    try:
        addresses = sorted({x[4][0] for x in socket.getaddrinfo(
            args.servidor, args.puerto, type=socket.SOCK_STREAM)})
        with socket.create_connection((args.servidor, args.puerto), args.espera):
            pass
        print(json.dumps({"servidor": args.servidor, "direcciones": addresses,
                          "puerto": args.puerto, "tcp": True,
                          "duracion_ms": round((time.monotonic() - started) * 1000)}, indent=2))
    except OSError as exc:
        print(f"Fallo de DNS o TCP: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
