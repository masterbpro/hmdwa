FROM python:3.9-slim-bullseye as compile-image
LABEL maintainer="@masterbpro <iserver12345@gmail.com>"
MAINTAINER masterbpro@protonmail.com
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY web/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim-bullseye
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .