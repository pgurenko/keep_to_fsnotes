#!/usr/bin/env python3
import os
import json
import datetime
from marshmallow import Schema, ValidationError, fields


class MSecTimestamp(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return 0
        return datetime.timestamp(value) * 1000000 + value.microsecond

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return datetime.datetime.fromtimestamp(value/1000000) + datetime.timedelta(microseconds=value%1000000)
        except ValueError as error:
            raise ValidationError("Bad timestamp.") from error


class AttachmentsSchema(Schema):
    mimetype = fields.String()
    filePath = fields.String()


class ListItemSchema(Schema):
    text = fields.String()
    isChecked = fields.Bool()


class AnnotationSchema(Schema):
    description = fields.String()
    source = fields.String()
    title = fields.String()
    url = fields.String()


class ShareeSchema(Schema):
    isOwner = fields.Bool()
    type = fields.String()
    email = fields.String()


class KeepNoteSchema(Schema):
    title = fields.String()
    textContent = fields.String(load_default='')
    createdTimestampUsec = MSecTimestamp()
    userEditedTimestampUsec = MSecTimestamp()
    attachments = fields.List(fields.Nested(AttachmentsSchema))
    isTrashed = fields.Bool()
    isArchived = fields.Bool()
    isPinned = fields.Bool()
    color = fields.String()
    annotations = fields.List(fields.Nested(AnnotationSchema))
    listContent = fields.List(fields.Nested(ListItemSchema))
    sharees = fields.List(fields.Nested(ShareeSchema))


class KeepNote:

    def __init__(self, filename):
        with open(filename, 'rt') as f:
            schema = KeepNoteSchema()
            note = schema.load(data=json.load(f))
            print(note)
            

# enum all jsons in Keep
for f in os.listdir('keep'):
    if f.endswith(".json"):
        KeepNote(f'keep/{f}')