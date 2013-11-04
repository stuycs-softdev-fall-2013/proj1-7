
var closingPunctuation = ['?','.','!'];
var t;
function checkKey(target, key, func) {
	func = (typeof func === "undefined") ? function(c) { return false;} : func;
	var c = String.fromCharCode(key.charCode);
	if(closingPunctuation.indexOf(c) != -1 || func(key)) {
		target.value += c;
		confirmSubmit(target);
	}
	t = target;
}
function resize(target) {
	target.style.height = 84;
	target.scrollHeight = 84;
	target.style.height = target.scrollHeight;
	window.scrollTo(0,document.body.scrollHeight);
	
}
function resizeIfDifferent(target) {
	if(target.scrollHeight > target.clientHeight + 1) {
		resize(target);
	}
}
function readonly(target) {
	console.log(target);
	target.setAttribute("readonly");
}
function upload() {
	document.sentence.submit();
}
function confirmSubmit(data) {
	readonly(data);
	
	target = document.getElementById("confirm");
	target.style.maxWidth = "100%";
	target.style.opacity = "1";
	target.style.height = "auto";
}
function edit() {
	var target = document.sentence.data;
	
	target.removeAttribute("readonly");
	target.value = target.value.substr(0, target.value.length - 1);
	reset = (function (val) {return val})(target.value);
	target.value = "";
	target.focus();
	target.value = reset;
	
	target = document.getElementById("confirm");
	target.style.maxWidth = "0%";
	target.style.opacity = "0";
	target.style.height = "0";		
}
