# Despliegue basico de una app FastAPI en Oracle Cloud VM

Guia breve para ejecutar esta aplicacion en una VM Linux (por ejemplo, Ubuntu) en Oracle Cloud.

## 1) Conectarse por SSH

```bash
chmod 600 <RUTA_LLAVE_PRIVADA>
ssh -i <RUTA_LLAVE_PRIVADA> <USUARIO_VM>@<IP_PUBLICA_VM>
```

## 2) Instalar Docker en la VM

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
```

Si deseas ejecutar Docker sin `sudo`, agrega tu usuario al grupo `docker` y vuelve a iniciar sesion:

```bash
sudo usermod -aG docker $USER
```

## 3) Obtener el codigo del proyecto

```bash
git clone <URL_REPOSITORIO>
cd <CARPETA_PROYECTO>
```

## 4) Construir la imagen

```bash
sudo docker build -t <NOMBRE_IMAGEN> .
```

## 5) Definir la IP publica como variable de entorno

```bash
export PUBLIC_IP=$(curl -s ifconfig.me)
source ~/.bashrc
echo $PUBLIC_IP
```

## 6) Ejecutar el contenedor

```bash
sudo docker run -e PUBLIC_IP="$PUBLIC_IP" -p <PUERTO_HOST>:8000 <NOMBRE_IMAGEN>
```

## 7) Verificar la aplicacion

```bash
curl http://<IP_PUBLICA_VM>:<PUERTO_HOST>/
```

Respuesta esperada:

```json
{"message": "Hello World", "public_ip": "<IP_PUBLICA_VM>"}
```

## Nota de red

En Oracle Cloud, habilita `<PUERTO_HOST>` en el Security List o NSG de la subred para permitir acceso externo.