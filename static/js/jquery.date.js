function month_days(a, b) {
	switch (b) {
	case 2:
		return a % 4 == 0 && a % 100 != 0 || a % 400 == 0 ? 29 : 28;
	case 4:
	case 6:
	case 9:
	case 11:
		return 30;
	default:
		return 31
	}
}
function zfill(a, b) {
	var c = "" + a;
	while (c.length < b) c = "0" + c;
	return c
}
function select_span(a, b, c, d, e, f, g, h) {
	function m(b) {
		return a.find("select[name=" + b + "]")
	}
	function r() {
		var a = p.val(),
			b = n.val() - 0,
			c = o.val() - 0,
			d = month_days(b, c),
			e = [];
		f || e.push(k);
		for (j = g ? g(b, c) : 1; j <= d; ++j) e.push('<option value="' + j + '">' + j + "</option>");
		p.html(e.join("")).val(a > d ? 0 : a)
	}
	function s() {
		var a = o.val(),
			b = p.val();
		q.val(n.val() + (a.length < 2 ? "0" : "") + a + (b.length < 2 ? "0" : "") + b)
	}
	var i = ['<input type="hidden" value="" name="' + b + '">'],
		j, a, k = '<option value="0">- 日 -</option>',
		l = d > e ? -1 : 1;
	if (d != e) {
		j = d, i.push('<select id="' + b + '_year" style="width:100px;" class="' + b + '_year date_year" name="year">'), f || i.push('<option value="0000">- 年 -</option>');
		for (; j != e; j += l) i.push('<option value="' + j + '">' + j + "</option>");
		i.push("</select>")
	}
	i.push('<select id="' + b + '_month" style="width:100px;" class="' + b + '_month date_month" name="month">'), f || i.push('<option value="0">- 月 -</option>');
	for (j = 1; j < 13; ++j) i.push('<option value="' + j + '">' + j + "</option>");
	i.push('</select><select id="' + b + '_day" style="width:100px;" class="' + b + '_day date_day" name="day">' + k + "</select>");
	if (h) {
		i.push('<select id="' + b + '_hour" class="' + b + '_hour date_hour" name="' + b + '_hour">');
		for (j = 0; j < 24; ++j) i.push('<option value="' + j + '">' + zfill(j, 2) + "</option>");
		i.push("</select>:"), i.push('<select id="' + b + '_minute" class="' + b + '_minute date_minute" name="' + b + '_minute">');
		for (j = 0; j < 60; j += 5) i.push('<option value="' + j + '">' + zfill(j, 2) + "</option>");
		i.push("</select>")
	}
	a.html(i.join(""));
	var n = m("year"),
		o = m("month"),
		p = m("day"),
		q = a.find("input");
	o.change(r), n.change(r), a.find("select").change(s), c -= 0, c && (n.val(parseInt(c / 1e4)), o.val(parseInt(c / 100) % 100).change(), p.val(c % 100), q.val(c))
}
function select_date(a, b, c, d, e, f, g) {
	document.write('<span id="' + a + '"></span>'), select_span($("#" + a), a, b, c, d, e, f, g)
}
function select_birthday(a, b) {
	var c = new Date,
		d = c.getFullYear();
	select_date(a, b, d, d - 128)
}
function select_future(a, b) {
	var c = new Date,
		d = c.getFullYear();
	select_date(a, b, d, d + 128)
};