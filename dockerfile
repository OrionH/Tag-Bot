FROM python:3.9-slim-bullseye AS build
WORKDIR /usr/src/app
COPY . .
RUN apt-get update && \
    apt-cache search g++ && \
    apt-get install -y -V --no-install-recommends \
    g++ && \
    pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3:latest AS runtime
WORKDIR /usr/src/app
COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/dist-packages/
COPY --from=build /usr/src/app /usr/src/app
CMD ["bot.py"]