#!/bin/sh
if env | grep -q ^SESSIONID=
then
    echo We are in the prod environment
  export REACT_APP_GUAC_BACKEND_HOSTNAME="wss://${SESSIONID}-8082-guacamole-mashup.${CHALLENGE_DOMAIN}:1337/"
  export REACT_APP_WIN_SERVER_HOSTNAME=localhost
else
  echo Docker Compose deployment
  export REACT_APP_GUAC_BACKEND_HOSTNAME="ws://localhost:8082/"
  export REACT_APP_WIN_SERVER_HOSTNAME=win-server
fi


npm run build
serve -s build