#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Completion source for nvim-completion-manager."""
import json
import os
import re

from cm import Base, register_source

script_dir = os.path.dirname(__file__)
properties_path = os.path.join(script_dir, '../../properties.json')
syntaxes_path = os.path.join(script_dir, '../../syntaxes.json')

cssProperties = {}
cssSyntaxes = {}

with open(properties_path) as data_file:
    cssProperties = json.load(data_file)

with open(syntaxes_path) as data_file:
    cssSyntaxes = json.load(data_file)

register_source(name='css',
                abbreviation='css',
                scoping=True,
                scopes=['css', 'sugarss', 'sass', 'scss', 'stylus', 'less'],
                word_pattern=r'[\w\-]+\s*:\s+',
                cm_refresh_patterns=[r'[\w\-]+\s*:\s+'],
                priority=8)


def parse(definition, visited=[]):
    """Return list of css keywords from the syntax."""
    values = []
    chunks = ['']
    letters = re.compile('[a-zA-Z-<>()]')
    for c in definition:
        if letters.match(c):
            chunks[-1] += c
        else:
            chunks.append('')
    chunks = list(filter(lambda c: c != '' and c != ')', chunks))
    for chunk in chunks:
        if chunk[0] == '<' and chunk[-1] == '>':
            word = chunk[1:-1]
            if word in cssSyntaxes and word not in visited:
                values.extend(parse(cssSyntaxes[word], visited + [word]))
        else:
            values.append(chunk)
    return values


def get_candidates(prop, rest):
    """Given a css property, return list of valid completion values."""
    values = []
    value_definition = cssProperties[prop]
    values = parse(value_definition)
    return values


class Source(Base):
    """Main fn called by nvim-completion-manager."""

    def cm_refresh(self, info, ctx):
        """Refresh candidates given vim cursor and line context."""
        matches = []
        if ':' in ctx['typed']:
            self.logger.info(ctx['typed'])
            prop, val = ctx['typed'].split(':', 1)
            matches += get_candidates(prop.strip(), val)
        else:
            matches += map(lambda i: i + ':', list(cssProperties.keys()))
        self.complete('css', ctx, ctx['startcol'], matches)
