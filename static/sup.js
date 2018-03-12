/* sup.js
 * vim: set ts=2 sw=2 sts=2 et :
 */

function set_result(text, color) {
  var finish = document.getElementById('ires');
  finish.textContent = text;
  finish.style.display = 'block';
  finish.style.backgroundColor = color;
}

function complete(e) {
  if (e.target.status == 200) {
    set_result('Success', '#4bb543');
  }
  else {
    console.log(e)
    set_result(e.target.statusText, '#ff0033');
  }
}

function canceled(e) {
  console.log(e);
  set_result('Upload canceled', '#111111');
}

function failed(e) {
  console.log(e);
  set_result('Upload failed', '#ff0033');
}

function progress(e) {
  var state = e.lengthComputable? Math.round(e.loaded * 100 / e.total): 'N/A';
  document.getElementById('iprog').textContent = state;
}

function fileUpload() {
  var xhr = new XMLHttpRequest();
  var fm = document.getElementById('form');
  var fd = new FormData(fm);

  document.getElementById('rprog').style.display = 'block';

  xhr.upload.addEventListener('progress', progress, false);
  xhr.addEventListener('load', complete, false);
  xhr.addEventListener('abort', canceled, false);
  xhr.addEventListener('error', failed, false);

  xhr.open('POST', fm.getAttribute('action'));
  xhr.send(fd);
}

function fileSelect() {
  var file = document.getElementById('file').files[0];
  if (file) {
    document.getElementById('rname').style.display = 'block';
    document.getElementById('rdata').style.display = 'block';
    document.getElementById('rprog').style.display = 'none';
    document.getElementById('iname').textContent = file.name;
    document.getElementById('isize').textContent = file.size;
    document.getElementById('itype').textContent = file.type || 'unknown';
    document.getElementById('rupload').style.display = 'block';
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
