ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

#Install snapcastclient

RUN apk upgrade --no-cache --available \
 && apk add --no-cache --repository http://nl.alpinelinux.org/alpine/edge/testing \
        py-pip \
	    python \
	    python-dev \
	    jq \
 && pip install \
        gspread  \
        APScheduler \
        oauth2client  

# Copy data for add-on
COPY run.sh /
COPY index.py /
COPY googleSheetUpload.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
