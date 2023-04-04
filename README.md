# Blockchain
A modern blockchain package presenting the principle of block operation. (includes tests)

## Instalation :
```
git clone https://github.com/Kamwebdev/Blockchain
cd Blockchain
python3 -m venv myvenv
[linux] source myvenv/bin/activate 
[windows] myvenv\Scripts\activate.bat
pip install .
```

## Run tests:
```
C:\Users\Programista\Documents\> pytest .
========================================================================================================= test session starts =========================================================================================================
platform win32 -- Python 3.9.12, pytest-7.1.1, pluggy-1.0.0
rootdir: C:\Users\Programista\Documents\Moje\Blockchain
plugins: anyio-3.5.0, mock-3.10.0
collected 25 items

tests\blockchain_test.py .........................                                                                                                                                                                               [100%]

========================================================================================================= 25 passed in 0.28s ========================================================================================================== 
```

## Code quality:
approved by :)
```
black --line-length 72 --target-version py38 *.py
isort --multi-line 3 --profile black --python-version 38 .
flake8 --ignore=F841 --max-doc-length=72 ./
pytest --cov blockchain  --cov-report annotate
```

## Sample usage:
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blockchain.blockchain import Blockchain

print("---Create Blockchain---")
myBlockchain = Blockchain(difficulty=3)
print(myBlockchain.last_block.hash)

print("\n---Add data to Blockchain---")
for i in range(1, 6, 2):
    myBlockchain.add_new_transaction("part {}".format({i}))
    myBlockchain.add_new_transaction("part {}".format({i + 1}))
    myBlockchain.mine()
    print(myBlockchain.last_block())
    print(myBlockchain.last_block.compute_hash)

print("\n---Print block data---")
myBlockchain.get_full_block()

print("\n---Verify full block history---")
myBlockchain.verify_full_block_history()
```
