FROM debian:11

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    neofetch \
    wget \
    python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*    

WORKDIR /SkyzuRobot/

COPY requirements.txt .
RUN pip3 install wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt

COPY . .
CMD ["python3.9", "-m", "SkyzuRobot"]
