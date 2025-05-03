{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "d329ed11-afc5-44b0-96dd-c95b0a515741",
   "metadata": {},
   "outputs": [],
   "source": [
    "from fastapi import FastAPI\n",
    "\n",
    "app = FastAPI()\n",
    "\n",
    "@app.get(\"/\")\n",
    "def read_root():\n",
    "    return {\"message\": \"Hello, FastAPI!\"}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": Null,
   "id": "c59733cb-29d7-479d-a1d6-c638a7eb772e",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
