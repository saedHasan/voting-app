FROM node:10-slim
# add curl for healthcheck
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Add Tini for proper init of signals
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

WORKDIR /app

RUN npm install -g nodemon

RUN useradd -u 1001 -r -g 0 -d /app -s /sbin/nologin \
    -c "Default Application User" default && \
    chown -R 1001:0 /app && \
    chmod -R g+rw /app

USER 1001

COPY src/package*.json ./

# Install cors package
RUN npm install cors

RUN npm ci \
 && npm cache clean --force

COPY src/. .

ENV PORT 8080
# Disable source map generation (adjust as needed for your build tool)
ENV GENERATE_SOURCEMAP=true
EXPOSE 8080

CMD ["/tini", "--", "node", "server.js"]
