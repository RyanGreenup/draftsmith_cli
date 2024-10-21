serve:
    gunicorn -w 4 -b 127.0.0.1:37239 src.server:app
