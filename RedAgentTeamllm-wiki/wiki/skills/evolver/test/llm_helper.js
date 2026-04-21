// Zero-dependency Gemini REST API wrapper for vibe testing.
// Uses only Node.js built-in https module.

'use strict';

var https = require('https');

var GEMINI_MODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
var GEMINI_ENDPOINT = 'generativelanguage.googleapis.com';
var GEMINI_TIMEOUT_MS = parseInt(process.env.GEMINI_TIMEOUT_MS || '30000', 10) || 30000;

function getApiKey() {
  return process.env.GEMINI_API_KEY || '';
}

function hasApiKey() {
  return getApiKey().length > 0;
}

// Call Gemini generateContent and return the text response.
// Returns a Promise<string>.
function callGemini(prompt) {
  var apiKey = getApiKey();
  if (!apiKey) return Promise.reject(new Error('GEMINI_API_KEY not set'));

  var body = JSON.stringify({
    contents: [{ parts: [{ text: String(prompt) }] }],
    generationConfig: {
      temperature: 0.2,
      maxOutputTokens: 4096,
    },
  });

  var options = {
    hostname: GEMINI_ENDPOINT,
    path: '/v1beta/models/' + GEMINI_MODEL + ':generateContent',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-goog-api-key': apiKey,
      'Content-Length': Buffer.byteLength(body),
    },
    timeout: GEMINI_TIMEOUT_MS,
  };

  return new Promise(function (resolve, reject) {
    var req = https.request(options, function (res) {
      var chunks = [];
      res.on('data', function (chunk) { chunks.push(chunk); });
      res.on('end', function () {
        var raw = Buffer.concat(chunks).toString('utf8');
        if (res.statusCode < 200 || res.statusCode >= 300) {
          return reject(new Error('Gemini API error ' + res.statusCode + ': ' + raw.slice(0, 500)));
        }
        try {
          var json = JSON.parse(raw);
          var text = '';
          if (json.candidates && json.candidates[0] && json.candidates[0].content) {
            var parts = json.candidates[0].content.parts || [];
            for (var i = 0; i < parts.length; i++) {
              if (parts[i].text) text += parts[i].text;
            }
          }
          resolve(text);
        } catch (e) {
          reject(new Error('Gemini response parse error: ' + e.message));
        }
      });
    });

    req.on('error', function (e) { reject(e); });
    req.on('timeout', function () {
      req.destroy();
      reject(new Error('Gemini API timeout after ' + GEMINI_TIMEOUT_MS + 'ms'));
    });

    req.write(body);
    req.end();
  });
}

// Extract JSON objects from LLM response text.
// Looks for lines containing { ... } patterns and tries to parse them.
function extractJsonObjects(text) {
  var results = [];
  var lines = String(text || '').split('\n');
  var buffer = '';
  var depth = 0;

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    for (var j = 0; j < line.length; j++) {
      var ch = line[j];
      if (ch === '{') {
        if (depth === 0) buffer = '';
        depth++;
        buffer += ch;
      } else if (ch === '}') {
        depth--;
        buffer += ch;
        if (depth === 0 && buffer.length > 2) {
          try {
            var obj = JSON.parse(buffer);
            if (obj && typeof obj === 'object') results.push(obj);
          } catch (e) {}
          buffer = '';
        }
        if (depth < 0) depth = 0;
      } else if (depth > 0) {
        buffer += ch;
      }
    }
    if (depth > 0) buffer += '\n';
  }

  return results;
}

module.exports = {
  callGemini: callGemini,
  hasApiKey: hasApiKey,
  extractJsonObjects: extractJsonObjects,
};
