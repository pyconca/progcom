""" ETL to convert from Papercall to DB

    This code is based on https://github.com/djangocon/papercall-api-import/blob/master/papercall_import.py.
"""
import argparse
import os
import requests
import subprocess

import logic as l

SUBMISSION_STATES = ('submitted', 'accepted', 'rejected', 'waitlist')

class PapercallAPI(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_many_papers_by(self, state):
        data = self._send_request(
            '/api/v1/submissions',
            {
                'state'    : state,
                'per_page' : 1000,
            }
        )

        return data

    def fetch_event_id(self):
        data = self._send_request(
            '/api/v1/event',
            {
                'state'    : state,
                'per_page' : 1000,
            }
        )

        return data['cfp']['id']

    def _send_request(self, uri, params):
        url = 'https://www.papercall.io{}'.format(uri)

        query = { '_token' : self.api_key, }
        query.update(params)

        response = requests.get(url, query)

        if response.status_code != 200:
            raise RuntimeError(response.status_code, response.text)

        data = response.json()

        # import pprint
        # pprint.pprint(dict(uri=uri, data=data), indent=2)

        return data

def _add_one_proposal(id, description, duration, audience, abstract, author,
                      notes, title, outline = None, recording_release = None):
    l.add_proposal(
        dict(
            id                = id,
            authors           = [author] if author else [],
            description       =u'Author\'s Current Location: {}\n\n{}'.format(author.get('location') or 'Unknown', description),
            duration          = duration,
            audience          = audience,
            abstract          = abstract,
            recording_release = recording_release if recording_release is None else False,
            notes             = notes,
            title             = title,
            outline           = outline or '',
        )
    )

def _transform_paper(raw_data):
    id          = raw_data['id']                     # id
    title       = raw_data['talk']['title']          # title
    abstract    = raw_data['talk']['abstract']       # abstract
    audience    = raw_data['talk']['audience_level'] # audience
    description = raw_data['talk']['description']    # description
    notes       = raw_data['talk']['notes']          # notes
    duration    = raw_data['talk']['talk_format']    # talk_format (string, expected integer)
    author      = dict()

    # Missings: recording_release, outline

    if 'profile' in raw_data:
        profile = raw_data['profile']

        author = dict(
            name     = profile['name'],
            email    = profile['email'],
            bio      = profile['bio'],
            location = profile['location'],
        )

    return dict(
        id          = id,
        title       = title,
        duration    = duration,
        audience    = audience,
        author      = author,
        description = description,
        abstract    = abstract,
        notes       = notes,
    )

def main(api_key):
    assert api_key

    api = PapercallAPI(api_key)

    papers = []

    for state in SUBMISSION_STATES:
        raw_papers = api.fetch_many_papers_by(state = state)

        if not raw_papers:
            print('>>> No submissions in {}. Skipped.'.format(state))

            continue

        import pprint
        print('>>> Sample submission in {}'.format(state))
        pprint.pprint(raw_papers[0], indent=2)
        print('>>> Sample transformation in {}'.format(state))
        pprint.pprint(_transform_paper(raw_papers[0]), indent=2)

        papers.extend([
            _transform_paper(raw_paper)
            for raw_paper in raw_papers
        ])

    for paper in papers:
        _add_one_proposal(**paper)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('api_key')

    main(parser.parse_args().api_key)
