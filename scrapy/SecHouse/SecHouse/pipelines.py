# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

from scrapy.conf import settings

import logging

class SechousePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self):
        client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        new_item = [{
            'district'      : item['district'      ],
            'mode'          : item['mode'          ],
            'price'         : item['price'         ],
            'location'      : item['location'      ],
            'area'          : item['area'          ],
            'downpayment'   : item['downpayment'   ],
            'built'         : item['built'         ],
            'orientation'   : item['orientation'   ],
            'payment'       : item['payment'       ],
            'house_type'    : item['house_type'    ],
            'floor'         : item['floor'         ],
            'decorate'      : item['decorate'      ],
            'age'           : item['age'           ],
            'elevator'      : item['elevator'      ],
            'agelimit'      : item['agelimit'      ],
            'property_right': item['property_right'],
            'only'          : item['only'          ],

        }]
        self.collection.insert(new_item)
        logging.debug("Item wrote to MongoDB database %s/%s"%(settings['MONGODB_DB'],settings['MONGODB_COLLECTION']))
        return item