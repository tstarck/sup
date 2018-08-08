/* sup.js
 * vim: set ts=2 sw=2 sts=2 et :
 * Copyright (c) 2018 Tuomas Starck
 */

function $(id) {
  return document.getElementById(id);
}

function progress(e) {
  var len = e.lengthComputable? Math.round(e.loaded * 100 / e.total): 0;
  console.log('progress() ' + len.toString() + '%');
  $('progress').style.width = len.toString() + '%';
}

function complete(e) {
  if (e.target.status == 200) {
    console.log('complete() status 200');
    $('progress').textContent = 'Success';
  }
  else {
    console.log(e);
  }
}

function canceled(e) {
  console.log('canceled()');
  $('progress').textContent = 'Canceled';
}

function failed(e) {
  console.log('failed()');
  $('progress').textContent = 'Failed';
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
