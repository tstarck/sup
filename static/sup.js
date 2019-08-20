/* sup.js
 * vim: set ts=2 sw=2 sts=2 et :
 * Copyright (c) 2018,2019 Tuomas Starck
 */

function $(id) {
  return document.getElementById(id);
}

function progress(e) {
  var len = e.lengthComputable? Math.round(e.loaded * 100 / e.total): 0;
  $('progress').style.width = len.toString() + '%';
}

function complete(e) {
  $('progress').style.width = '100%';
  switch (e.target.status) {
    case 200:
      $('progress').textContent = 'Success';
      $('progress').style.background = '#32c809';
      $('progress').style.color = 'white';
      break;
    case 403:
      failed(e, e.target.statusText + ': ' + e.target.responseText);
      break;
    case 500:
      failed(e, e.target.statusText);
      break;
    default:
      failed(e, 'Unknown error');
  }
}

function canceled(e) {
  $('progress').textContent = 'Canceled';
  $('progress').style.width = '100%';
}

function failed(e, msg='Failed') {
  if (e.target.status == 0) {
    msg = 'Error: upload too large';
  }
  $('progress').textContent = msg;
  $('progress').style.background = '#de1738';
  $('progress').style.color = 'white';
  $('progress').style.width = '100%';
}

function fileUpload() {
  var form = $('form');
  var fd = new FormData(form);
  var xhr = new XMLHttpRequest();

  $('progress').style.display = 'block';

  xhr.upload.addEventListener('progress', progress, false);
  xhr.addEventListener('load', complete, false);
  xhr.addEventListener('abort', canceled, false);
  xhr.addEventListener('error', failed, false);

  xhr.open('POST', form.getAttribute('action'));
  xhr.send(fd);
}

function fileSelect() {
  var file = document.getElementById('file').files[0];
  if (file) {
    $('infobox').style.display = 'block';
    $('filename').textContent = file.name;
    $('filesize').textContent = file.size;
    $('filetype').textContent = file.type || 'unknown';
  }
}

function init() {
  document.getElementById('file').onchange = fileSelect;
  document.getElementById('upload').onclick = fileUpload;
}

if (document.attachEvent? document.readyState === "complete": document.readyState !== "loading") {
  init();
} else {
  document.addEventListener('DOMContentLoaded', init);
}
