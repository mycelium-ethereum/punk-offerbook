#!/usr/bin/env bash

cd punk-offerbook
python3 -m uvicorn app:app --host 0.0.0.0 --port 3400