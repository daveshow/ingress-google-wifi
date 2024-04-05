FROM python:3-alpine AS compile-image

RUN mkdir -p /output/wheels && \
    python -m pip install --no-cache-dir -U pip && \
    python -m pip install --cache-dir=/output/wheels scapy

FROM python:3-alpine
COPY --from=compile-image /output/ /output/
RUN mkdir -p /output/wheels && \
    python -m ensurepip && \
    python -m pip install --no-cache-dir -U pip && \
    python -m pip install --cache-dir=/output/wheels --prefer-binary scapy

RUN mkdir -p /code
WORKDIR /code
ADD arp.py /code/
RUN rm -rf /output/

CMD ["python", "-u", "/code/arp.py"]