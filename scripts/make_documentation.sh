#!/usr/bin/env bash

cd sphinx

rm build -rf

PYTHONPATH=".." make html

cd ..