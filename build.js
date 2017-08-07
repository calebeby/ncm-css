#!/usr/bin/env node

const fetch = require('node-fetch')
const fs = require('mz/fs')
const {map} = require('objectfn')

const mdnProperties = 'https://raw.githubusercontent.com/mdn/data/master/css/properties.json'
const mdnSyntaxes = 'https://raw.githubusercontent.com/mdn/data/master/css/syntaxes.json'

const getJSON = url => fetch(url).then(d => d.json())
const getSyntax = obj => map(obj, v => v.syntax)
const writeJSON = path => data => fs.writeFile(path, JSON.stringify(data))

getJSON(mdnProperties)
  .then(getSyntax)
  .then(writeJSON('properties.json'))

getJSON(mdnSyntaxes)
  .then(getSyntax)
  .then(writeJSON('syntaxes.json'))

