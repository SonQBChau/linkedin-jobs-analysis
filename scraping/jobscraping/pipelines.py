# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from google.cloud import language

# working with google's types:
# https://googleapis.dev/python/language/latest/language_v1/types.html#google.cloud.language_v1.types.Entity
# https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity
# https://cloud.google.com/natural-language/docs/reference/rest/v1/TextSpan
# also see here for more in-depth examples:
# https://cloud.google.com/natural-language/docs/analyzing-entities#language-entities-string-python


def get_google_type_name(t):
    return str(t).split('.')[-1]


def make_serializable_mention(m):
    newm = {
        'text': {
            'content': m.text.content,
            'begin_offset': m.text.begin_offset
        },
        'type_': get_google_type_name(m.type_)
        # ignoring sentiment for now
    }
    return newm


def make_serializable_entity(ent):
    newent = {
        'name': ent.name,
        'type_': get_google_type_name(ent.type_)
        # ignoring salience and sentiment for now,
        # altho i think sentiment is always unpopulated
        # unless you call the sentiment analysis API
    }
    if hasattr(ent, 'metadata'):
        newent['metadata'] = dict(ent.metadata)
    if hasattr(ent, 'mentions'):
        newent['mentions'] = [make_serializable_mention(
            m) for m in ent.mentions]
    return newent


class JobDescriptionEntityAnalysisPipeline:

    def open_spider(self, spider):
        """ 
            before you can create a GCP API client, you must install the SDK:
            https://cloud.google.com/sdk/docs/quickstart

            ...and run:
            $ gcloud auth application-default login

            the first time you try to submit a request to the API, you will be
            prompted to enable the API in your GCP project and given a link.
            however, you are free to enable the API beforehand your project's settings.
        """
        self.client = language.LanguageServiceClient()

    def close_spider(self, spider):
        """ 
            unable to find a way to close the client in its docs:
            https://googleapis.dev/python/language/latest/language_v1/services.html

            presumably this is handled automatically by its python implementation
            (i.e. the API wrapper devs overrode __del__).
        """
        pass

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('description'):
            doc = language.Document(
                content=adapter['description'], type_='PLAIN_TEXT')
            # encoding type allows meaningful entity occurrence offsets
            analysis = self.client.analyze_entities(
                document=doc, encoding_type='UTF32')

            adapter['entities'] = [make_serializable_entity(
                entity) for entity in analysis.entities]

        return item
