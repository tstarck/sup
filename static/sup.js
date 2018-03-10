/* sup.js */

function complete(e) {
  var finish = document.getElementById('ires');
  finish.textContent = 'Success';
  finish.style.display = 'block';
  finish.style.backgroundColor = '#4bb543';
}

function canceled(e) {
  console.log(e);
  var finish = document.getElementById('ires');
  finish.textContent = 'Upload canceled';
  finish.style.display = 'block';
  finish.style.backgroundColor = '#111111';
}

function failed(e) {
  console.log(e);
  var finish = document.getElementById('ires');
  finish.textContent = 'Upload failed';
  finish.style.display = 'block';
  finish.style.backgroundColor = '#ff0033';
}

function progress(e) {
  var state = e.lengthComputable? Math.round(e.loaded * 100 / e.total): 'N/A';
  document.getElementById('iprog').textContent = state;
}

function fileUpload() {
  var xhr = new XMLHttpRequest();
  var fd = new FormData(document.getElementById('form'));

  document.getElementById('rprog').style.display = 'block';

  xhr.upload.addEventListener('progress', progress, false);
  xhr.addEventListener('load', complete, false);
  xhr.addEventListener('abort', canceled, false);
  xhr.addEventListener('error', failed, false);

  /* FIXME We need to support other path than / only */
  xhr.open('POST', '/');
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
    document.getElementById('itype').textContent = file.type;
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
