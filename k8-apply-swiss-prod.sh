#!/bin/bash
DEPLOYMENT="https://gist.githubusercontent.com/AlexanderDefuria/7953ab9419805af74ffb931ef45f20b3/raw"
NGINX="https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/do/deploy.yaml"
APP_SERVICE="https://gist.github.com/AlexanderDefuria/e67c6dc930a924902177386783600c49/raw"
INGRESS="https://gist.github.com/AlexanderDefuria/5235815e69ba701d77ffd32bcac8cbd8/raw"
CERT_MANAGER="https://github.com/cert-manager/cert-manager/releases/download/v1.7.1/cert-manager.yaml"
STAGING_ISSUER="https://gist.github.com/AlexanderDefuria/985312a34d9d15cd81d52aa8dc8577c3/raw"
PROD_ISSUER="https://gist.github.com/AlexanderDefuria/edbc182cd2e37c2ebf347a8419903ee0/raw"

docker login

kubectl create secret generic regcred     --from-file=.dockerconfigjson=.docker/config.json     --type=kubernetes.io/dockerconfigjson

COUNT=0
LIST=($NGINX $DEPLOYMENT $APP_SERVICE $INGRESS $CERT_MANAGER $PROD_ISSUER $STAGING_ISSUER)
for INDEX in ${LIST[@]}
do
	COUNT=$((COUNT+1))
	$(curl -L ${INDEX%raw:} -o ./$COUNT.txt)
	kubectl apply -f ./$COUNT.txt
done
