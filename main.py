# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2

import logging

from models import Animal
from google.appengine.ext import ndb


from mapreduce import base_handler
from mapreduce import mapreduce_pipeline
from mapreduce import operation as op
from mapreduce import shuffler


from google.appengine.api import app_identity


bucket_name = app_identity.get_default_gcs_bucket_name()


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

PARENT = ndb.Key("FoodChain", 1)


       
        
class MainPage(webapp2.RequestHandler):
    def get(self):
        animals = [a.as_dict() for a in Animal.query(ancestor=PARENT)]
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({"animals": animals}))


class NewAnimalHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('animal')

        if name:
            animal = Animal(parent=PARENT, name=name)
            animal.put()

        self.redirect('/')


class NewPreyHandler(webapp2.RequestHandler):
    def post(self):
        predator = self.request.get('predator')
        prey = self.request.get('prey')

        animal = Animal.get_by_id(int(predator), parent=PARENT)
        animal.prey.append(ndb.Key("FoodChain", 1, Animal, int(prey)))
        animal.put()

        self.redirect('/')

        
        

"""
def prey_count_map(animal):
    aid = animal.key.id()
    pids = [p.id() for p in animal.prey]
    for pid in pids:
        yield (pid, aid)


def prey_count_reduce(animal_id, predator_ids):
    yield "%s,%i\n" % (animal_id, len(predator_ids))
"""





def prey_count_map(animal):

    for preyAnimal in animal.prey:
        yield (preyAnimal.id(), animal.key.id())


def prey_count_reduce(key, values):
    animal = Animal.get_by_id(int(key), parent=PARENT)
    yield "%s: %d\n" % ( str(animal.name), len(values) )



class PreyCountPipeline(base_handler.PipelineBase):


    def run(self):
        
        output = yield mapreduce_pipeline.MapreducePipeline(
            "prey_count",
            "main.prey_count_map",
            "main.prey_count_reduce",
            "mapreduce.input_readers.DatastoreInputReader",
            "mapreduce.output_writers.GoogleCloudStorageOutputWriter",
            mapper_params={
                "entity_kind": 'models.Animal'
            },
            reducer_params={
                "output_writer": {
                    "bucket_name": bucket_name,
                    "content_type": "text/plain",
                }
            }, shards=1)
 

class MapRecuceHandler(webapp2.RequestHandler):
    
    def post(self):

        pipeline = PreyCountPipeline()
        pipeline.start()

        logging.info("STARTED PIPELINE %s", pipeline.pipeline_id)
        self.redirect("/mr?pipeline=" + pipeline.pipeline_id)


    def get(self):

        pipeline_id = self.request.get("pipeline")
        pipeline = mapreduce_pipeline.MapreducePipeline.from_id(pipeline_id)
        if pipeline.has_finalized:
            logging.info("Valamis")

            self.response.headers['content-type'] = 'text/plain; charset=utf-8'
            self.response.write("Valmis")

        else:

            logging.info("Ei valmis")

            self.response.headers['content-type'] = 'text/plain; charset=utf-8'
            self.response.write("Ei valmis")

        


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newanimal', NewAnimalHandler),
    ('/newprey', NewPreyHandler),
    ('/mr', MapRecuceHandler)], debug=True)





    
