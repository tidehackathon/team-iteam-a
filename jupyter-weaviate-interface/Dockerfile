FROM continuumio/anaconda3

RUN apt update

RUN pip install jupyter osint-python-test-bed-adapter==2.1.0 altair weaviate-client jupyter-notebookparams transformers torch

WORKDIR /project

COPY ./notebooks /project/notebooks

VOLUME /project

EXPOSE 8888
CMD [ "jupyter-lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''", "--NotebookApp.tornado_settings={'headers':{'Content-Security-Policy': 'frame-ancestors self *'}}"]
