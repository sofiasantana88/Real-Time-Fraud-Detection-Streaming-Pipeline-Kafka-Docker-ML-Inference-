$root = "C:\kafka-docker"

cd $root
docker compose up -d

Start-Process powershell -ArgumentList "-NoExit", "-Command cd $root; py .\streaming\consumer.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command cd $root; py .\streaming\producer.py"
