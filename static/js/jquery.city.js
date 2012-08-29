g.component.qzone = $("qzone") ? true : false;
g.component.lunar = 1;
g_lang = g.component.areaSearch = 1;
var index = {
	aq_js: "http://zc.qq.com/chs/m.js?v=" + Math.random(),
	aq_object: {},
	initIndexType: 0,
	inited: false,
	nickE: "昵称不可以为空,昵称不可以为空格,请输入昵称,,不能超过24个字母或12个汉字,您不能使用该昵称注册".split(","),
	otherEmailE: '请输入邮箱,帐号已被注册,邮箱格式错误,帐号可用,请输入您常用的电子邮箱<a id="no_email" href="javascript:void(0);" onclick="index.hasNoEmail();">  没有邮箱?</a>,该Email已经绑定QQ号，您可以直接登录或者更换其他Email进行注册,不能使用qq.com的邮箱帐号'.split(","),
	selfEmailE: "请输入邮箱,长度为3-18个字符,必须以a-z的英文字母（不分大小写）开头,必须以a-z的英文字母（不分大小写）开头,请创建邮箱名，由3-18个英文、数字、点、减号、下划线组成,点、减号、下划线不能连续出现两次或两次以上,由英文字母、数字结尾,Email帐号格式不正确,邮箱格式错误,邮箱已被注册".split(","),
	passE: ["您输入的密码过短", "密码不能为9位以下纯数字", "密码不可以为空", "您输入的密码过长"],
	passInfo: ["级别低", "级别高"],
	passAgainE: ["密码不一致", "请再次输入密码"],
	weakpassTips: ["连续字符密码易被破解，请用多组合的密码", "相同字符密码易被破解，请用多组合的密码", "试试字母、数字、标点的组合吧"],
	birthE: ["生日不可为空", "生日不合法"],
	areaE: ["请选择正确的地区", "不支持该地区"],
	termsE: ["请同意条款"],
	birthdayE: ["请选择生日"],
	submitE: ["请先同意服务条款", "立即注册"],
	codeE: ["验证码错误", "请输入图中的字母，不区分大小写", "请输入完整验证码", "请输入验证码"],
	inputSearchTipsArray: "试试直接填写吧！例如1960,试试直接填写吧！例如11,试试直接填写吧！例如15,试试快速搜索吧！例如中国或zg,试试快速搜索吧！例如北京或bj,试试快速搜索吧！例如朝阳或cy".split(","),
	maxPwdLen: 16,
	minPwdLen: 6,
	emailReg: /^[a-z0-9][a-z0-9._-]*@[a-z0-9_-]+(\.[a-z0-9_-]+)+$/i,
	enWordReg: /[a-zA-Z]/,
	alreadyUsedEmails: [],
	type: 0,
	selfEmail: "",
	selfType: 0,
	otherEmail: "",
	nick: "",
	password: "",
	passAgain: "",
	sex: "1",
	birthType: "0",
	isLeap: 1,
	year: "",
	month: "",
	day: "",
	country: "",
	province: "",
	city: "",
	verifycode: "",
	code: "",
	qzone: g.component.qzone,
	agreed: true,
	showing: false,
	host: "http://zc.qq.com/",
	initInfo: null,
	totol: 2,
	errorId: "",
	needShowError: [1, 1, 1],
	location: null,
	showDate: {
		year: 0,
		month: 0,
		day: 0,
		isLeap: false
	},
	maxDate: {
		year: 0,
		month: 0,
		day: 0
	},
	old_birthType: "0",
	number_init: "cgi-bin/chs/numreg/init",
	qqmail_init: "cgi-bin/chs/qqmailreg/init",
	other_init: "cgi-bin/chs/othmailreg/init",
	number_url: "cgi-bin/chs/numreg/get_acc",
	qqmail_url: "cgi-bin/chs/qqmailreg/get_acc",
	othermail_url: "cgi-bin/chs/othmailreg/get_acc",
	codeUrl: "http://captcha.qq.com/getimage?aid=1007901",
	otherChkUrl: "cgi-bin/chs/othmailreg/check_mail",
	selfChkUrl: "cgi-bin/chs/qqmailreg/check_mail",
	fromReportUrl: "/cgi-bin/common/attr",
	nickChkUrl: "/cgi-bin/chs/common/dirty_check",
	areaSearchUrl: "/cgi-bin/chs/common/area",
	email_ok: "email_ok.html",
	decimal_ok: "decimal_ok.html",
	max_selective_rate: 100,
	selective_rate: 5,
	selective_decimal_ok: "selective_decimal_ok.html",
	send_ok: "send_ok.html",
	pwdLvClass: ["empty", "rankLow", "rankMiddle", "rankHigh"],
	pwdLvTips: ["6-16个字符，不可以为9位以下纯数字", "试试字母、数字、标点混搭", "复杂度还行，再加强一下等级？", "密码强度好，请记牢！", "弱：试试加长您的密码"],
	pwdLvWording: ["", "弱", "中等", "强"],
	keyCode: {
		UP: 38,
		DOWN: 40,
		LEFT: 37,
		RIGHT: 39,
		ENTER: 13,
		TAB: 9,
		BACK: 8,
		DEL: 46,
		F5: 116
	},
	listIndex: [0, 21, 0, -1, -1, -1, -1, 0],
	selectListIndex: [0, 21, 0, -1, -1, -1, -1, 0],
	selectListState: [0, 0, 0, 0, 0, 0, 0, 0],
	searchTimeoutId: [0, 0, 0, 0, 0, 0, 0, 0],
	selectHasSelected: [false, false, false, false, false, false, false, false],
	noAreaStr: "0",
	initAddress: "1,中国,11,北京,1,东城".split(","),
	noSelectTip: "该时间不可选",
	fromId: "",
	fromMap: {
		qq: 58029,
		pt: 58588,
		im: 58589,
		music: 58590,
		live: 58591,
		client: 61112,
		other: 58030
	},
	ptlang: "",
	ADUIN: "",
	ADSESSION: "",
	checkNickMap: {},
	yearSearchArr: [],
	monthSearchArr: [],
	daySearchArr: [],
	birthdayTipsShow: false,
	areaTipsShow: false,
	pwd_valid: false,
	safeCode: [0, 0, 0, 0, 0, 0, 0, 0],
	pwdTimeArray: [0, 0, 0, 0],
	pwdNum: 0,
	pwdTime: 0,
	knownEmail: "gmail.com,hotmail.com,yahoo.com,sina.com,163.com,126.com,vip.sina.com,sina.cn,sohu.com,yahoo.cn,yahoo.com.cn,139.com,wo.com.cn,189.cn,live.com,msn.com,live.hk,live.cn,hotmail.com.cn,hinet.net,msa.hinet.net,cm1.hinet.net,umail.hinet.net,xuite.net,yam.com,pchome.com.tw,netvigator.com,seed.net.tw,anet.net.tw".split(","),
	setAq: function(a, b) {
		index.aq_object[a] = b
	},
	setCode: function(a, b) {
		switch (a) {
		case index.keyCode.BACK:
			index.safeCode[b + 1]++, index.safeCode[7]++;
		default:
			index.safeCode[b]++
		}
		index.safeCode[7]++
	},
	setCodeCookie: function() {
		var a = index.safeCode.join("-");
		$.cookie.setSessionCookie("uoc", a, "zc.qq.com", "/")
	},
	setFromId: function() {
		var a = $.bom.query("fromId");
		a || ((a = $.bom.query("from")) || (a = "other"), a = index.fromMap[a]);
		index.fromId = a;
		index.ptlang = $.bom.query("ptlang");
		index.ADUIN = $.bom.query("ADUIN");
		index.ADSESSION = $.bom.query("ADSESSION");
		var a = $.bom.query("regkey"),
			b = $.bom.query("ADTAG");
		a && $.cookie.set("regkey", a, "zc.qq.com", "/", 17520);
		b && $.cookie.set("ADTAG", b, "zc.qq.com", "/", 17520)
	},
	setCloseAppId: function() {
		var a = $.bom.query("app_id"),
			b = $.bom.query("app_param");
		$.winName.set("app_id", a);
		$.winName.set("app_param", b)
	},
	reportSource: function() {
		document.createElement("img").src = index.fromReportUrl + "?id=" + index.fromId + "&timeused=0&seed=" + Math.random()
	},
	pushAlreadyUsedEmails: function(a) {
		for (var b = 0, c = index.alreadyUsedEmails[0]; c; c = index.alreadyUsedEmails[++b]) if (a == c) return;
		index.alreadyUsedEmails.push(a)
	},
	emailHasAlreadyUsed: function(a) {
		for (var b = 0, c = index.alreadyUsedEmails[0]; c; c = index.alreadyUsedEmails[++b]) if (a == c) return true;
		return false
	},
	json2str: function(a) {
		var b = [],
			c;
		for (c in a) b.push('"' + c + '":' + (typeof a[c] == "object" && a[c] != null ? json2str(a[c]) : /^(string|number)$/.test(typeof a[c]) ? '"' + a[c] + '"' : a[c]));
		return "{" + b.join(",") + "}"
	},
	getInitUrl: function() {
		return index.type == 0 ? index.host + index.number_init + "?r=" + Math.random() : index.host + (index.type == 1 ? index.qqmail_init : index.other_init) + "?r=" + Math.random()
	},
	getSubmitUrl: function() {
		return index.type == 0 ? index.host + index.number_url + "?r=" + Math.random() : index.host + (index.type == 1 ? index.qqmail_url : index.othermail_url) + "?r=" + Math.random()
	},
	showCodeByElevel: function(a) {
		switch (a) {
		case "0":
			$("code_box").className = "box box_9 hide";
			break;
		case "1":
		case "2":
			$("code_box").className = "box box_9";
			$("code_img").src = index.codeUrl + "&r=" + Math.random();
			break;
		case "6":
			location.href = "worst.html?ec=21";
			break;
		default:
			$("code_box").className = "box box_9", $("code_img").src = index.codeUrl + "&r=" + Math.random()
		}
	},
	getIndexFromId: function(a) {
		var b = 0;
		try {
			b = parseInt(a.split("_")[1])
		} catch (c) {
			b = 0
		}
		return b
	},
	updateShowdDate: function() {
		if (index.year && index.month) {
			var a = index.day == "" ? 1 : index.day,
				a = calendar.getDate(parseInt(index.year), parseInt(index.month), parseInt(a), parseInt(index.old_birthType), parseInt(index.isLeap)).split("-");
			index.showDate.year = parseInt(a[0]);
			index.showDate.month = parseInt(a[1]);
			index.showDate.day = index.day == "" ? 0 : parseInt(a[2]);
			index.showDate.isLeap = a[3] == "0" ? true : false;
			index.isLeap = index.showDate.isLeap ? 0 : 1
		}
		a = (new Date).getFullYear();
		if (index.showDate.year > a) index.showDate.year = a, index.showDate.month = 1, index.showDate.day = 1, index.showDate.isLeap = false;
		if (index.showDate.year == index.maxDate.year - 120) index.showDate.year = index.maxDate.year - 119, index.showDate.month = 1, index.showDate.day = 1, index.showDate.isLeap = false;
		index.old_birthType = index.birthType
	},
	initMaxDate: function() {
		var a = new Date;
		try {
			var b = index.initInfo.localdate.split("-");
			index.maxDate.year = parseInt(b[0]);
			index.maxDate.month = parseInt(b[1]);
			index.maxDate.day = parseInt(b[2])
		} catch (c) {
			index.maxDate.year = a.getFullYear(), index.maxDate.month = a.getMonth() + 1, index.maxDate.day = a.getDate()
		}
	},
	inMaxDate: function(a, b, c, d, e) {
		var f = new Date(index.maxDate.year, index.maxDate.month, index.maxDate.day),
			h = new Date;
		switch (d + "") {
		case "0":
			h = new Date(a, b, c);
			break;
		case "1":
			h = calendar.getDate(a, b, c, 1, e).split("-"), h = new Date(parseInt(h[0]), parseInt(h[1]), parseInt(h[2]))
		}
		f = f.getTime();
		return h.getTime() <= f ? true : false
	},
	getPwdRank: function(a) {
		var b = 0;
		a.match(/[a-z]/g) && b++;
		a.match(/[A-Z]/g) && b++;
		a.match(/[0-9]/g) && b++;
		a.match(/[^a-zA-Z0-9]/g) && b++;
		b = b > 3 ? 3 : b;
		if (a.length < 6 || /^\d{1,8}$/.test(a)) b = 0;
		a.length < 8 && b > 1 && (b = 1);
		return b
	},
	showPwRank: function() {
		$("pwd_tips").className = "hide";
		var a = $("password").value;
		$("pwd_result");
		$("pwd_result").className = "";
		var b = $("password_info"),
			c = $("password_pic"),
			d = index.getPwdRank(a);
		c.innerHTML = index.pwdLvWording[d];
		c.className = index.pwdLvClass[d];
		if (d > 1) b.innerHTML = index.pwdLvTips[d];
		else if (d == 1) b.innerHTML = index.isLianxuPwd(a) ? index.weakpassTips[0] : index.isSamePwd(a) ? index.weakpassTips[1] : index.weakpassTips[2]
	},
	isLianxuPwd: function(a) {
		if (a.length < 2) return true;
		var b = a.charCodeAt(0) - a.charCodeAt(1);
		if (b == 0) return false;
		for (var c = 1, d = a.length; c < d - 1; c++) if (a.charCodeAt(c) - a.charCodeAt(c + 1) != b) return false;
		return true
	},
	isSamePwd: function(a) {
		for (var b = 0, c = a.length; b < c - 1; b++) if (a.charCodeAt(b) != a.charCodeAt(b + 1)) return false;
		return true
	},
	hidePwRank: function() {
		$("pwd_result").className = "hide";
		$("pwd_tips").className = "pwd_tips"
	},
	updateSelectListIndex: function(a, b) {
		index.selectListIndex[a] = b
	},
	updateListIndex: function(a, b) {
		index.selectListIndex[a] = b;
		index.listIndex[a] = b
	},
	getSelectScrollTop: function(a) {
		var b = index.selectListIndex[a],
			c = 0;
		switch (a) {
		case 0:
			c = 0;
			break;
		case 1:
		case 2:
		case 3:
			c = b > 5 ? (b - 5) * 20 : 0;
			break;
		case 4:
		case 5:
		case 6:
			c = b > 8 ? (b - 8) * 20 : 0
		}
		return c
	},
	getSelectListItem: function(a) {
		var b = index.selectListIndex[a],
			c = null;
		switch (a) {
		case 0:
			c = $("birthday_" + b);
			break;
		case 1:
			c = $("year_" + b);
			break;
		case 2:
			c = $("month_" + b);
			break;
		case 3:
			c = $("day_" + b);
			break;
		case 4:
			c = $("country_" + b);
			break;
		case 5:
			c = $("province_" + b);
			break;
		case 6:
			c = $("city_" + b)
		}
		return c
	},
	moveList: function(a, b, c, d) {
		var e = b.getElementsByTagName("li");
		switch (c.keyCode) {
		case index.keyCode.UP:
			c.stopPropagation();
			c.preventDefault();
			if (index.listIndex[d] > 0) {
				e[index.listIndex[d]].className = "";
				e[index.listIndex[d] - 1].className = "hover";
				if (d < 4 && d > 0) b.scrollTop = index.listIndex[d] > 6 ? (index.listIndex[d] - 6) * 20 : 0;
				if (d >= 4) b.scrollTop = index.listIndex[d] > 9 ? (index.listIndex[d] - 9) * 20 : 0;
				index.listIndex[d]--
			}
			break;
		case index.keyCode.DOWN:
			c.stopPropagation();
			c.preventDefault();
			if (b.className.indexOf("hide") > -1) {
				switch (d) {
				case 0:
					index.switchBirtydayType();
					break;
				case 1:
					index.switchYear();
					break;
				case 2:
					index.switchMonth();
					break;
				case 3:
					index.switchDay();
					break;
				case 4:
					index.switchCountry();
					break;
				case 5:
					index.switchProvince();
					break;
				case 6:
					index.switchCity()
				}
				return
			}
			if (index.listIndex[d] < e.length - 1) {
				if (index.listIndex[d] >= 0) e[index.listIndex[d]].className = "";
				e[index.listIndex[d] + 1].className = "hover";
				if (d < 4 && d > 0) b.scrollTop = index.listIndex[d] > 5 ? (index.listIndex[d] - 5) * 20 : 0;
				if (d >= 4) b.scrollTop = index.listIndex[d] > 8 ? (index.listIndex[d] - 8) * 20 : 0;
				index.listIndex[d]++
			}
			break;
		case index.keyCode.ENTER:
			c.stopPropagation();
			c.preventDefault();
			if (index.listIndex[d] < 0 || !e[index.listIndex[d]]) return;
			c = e[index.listIndex[d]].innerHTML;
			c = $.html.decode(c);
			index.selectHasSelected[d] = true;
			switch (d) {
			case 0:
				a.innerHTML = c;
				a = index.birthType;
				index.birthType = e[index.listIndex[d]].getAttribute("value");
				a != index.birthType && (index.updateShowdDate(), index.changeYear(), index.changeMonth(), index.changeDay(), index.showBirthdayInfo());
				index.updateSelectListIndex(d, index.listIndex[d]);
				index.hideBirtydayType();
				break;
			case 1:
				a.value = c;
				a = index.year;
				index.year = e[index.listIndex[d]].getAttribute("value");
				index.showDate.year = index.year;
				a != index.year && (index.changeMonth(), index.changeDay(), index.showBirthdayInfo());
				index.updateSelectListIndex(d, index.listIndex[d]);
				index.hideYear();
				break;
			case 2:
				a.value = c;
				a = index.month;
				index.month = e[index.listIndex[d]].getAttribute("value");
				index.isLeap = e[index.listIndex[d]].getAttribute("isLeap") ? e[index.listIndex[d]].getAttribute("isLeap") : 1;
				index.showDate.month = index.month;
				index.showDate.isLeap = index.isLeap == 1 ? false : true;
				a != index.month && (index.changeDay(), index.showBirthdayInfo());
				index.updateSelectListIndex(d, index.listIndex[d]);
				index.hideMonth();
				break;
			case 3:
				a.value = c;
				a = index.day;
				index.day = e[index.listIndex[d]].getAttribute("value");
				index.showDate.day = index.day;
				a != index.day && index.showBirthdayInfo();
				index.updateSelectListIndex(d, index.listIndex[d]);
				index.hideDay();
				break;
			case 4:
				a.value = c;
				b = index.country;
				index.country = e[index.listIndex[d]].getAttribute("value");
				b != index.country && (index.changeProvince(), index.changeCity());
				index.updateSelectListIndex(d, index.listIndex[d]);
				c.length > 6 ? (a.title = c, a.value = index.isEnglishWord(c) ? c.substring(0, 12) : c.substring(0, 6)) : a.title = "";
				index.hideCountry();
				break;
			case 5:
				a.value = c;
				b = index.province;
				index.province = e[index.listIndex[d]].getAttribute("value");
				b != index.province && index.changeCity();
				index.updateSelectListIndex(d, index.listIndex[d]);
				c.length > 6 ? (a.title = c, a.value = index.isEnglishWord(c) ? c.substring(0, 12) : c.substring(0, 6)) : a.title = "";
				index.hideProvince();
				break;
			case 6:
				a.value = c;
				index.city = e[index.listIndex[d]].getAttribute("value");
				index.updateSelectListIndex(d, index.listIndex[d]);
				c.length > 6 ? (a.title = c, a.value = index.isEnglishWord(c) ? c.substring(0, 12) : c.substring(0, 6)) : a.title = "";
				index.hideCity();
				break;
			case 7:
				a.value = c, $("nick").focus(), $.css.addClass(b, "hide")
			}
			break;
		case index.keyCode.TAB:
			switch (d) {
			case 0:
				index.hideBirtydayType();
				break;
			case 1:
				index.hideYear();
				break;
			case 2:
				index.hideMonth();
				break;
			case 3:
				index.hideDay();
				break;
			case 4:
				index.hideCountry();
				break;
			case 5:
				index.hideProvince();
				break;
			case 6:
				index.hideCity();
				break;
			case 7:
				$.css.addClass(b, "hide")
			}
		}
		return false
	},
	isChangingTab: function() {
		return $("nav_1").getAttribute("_hover") || $("nav_2").getAttribute("_hover") || $("email_info").getAttribute("_hover")
	},
	iptFocus: function(a) {
		try {
			var b = $(a);
			b.focus();
			b.select()
		} catch (c) {}
	},
	mailRegReport: function() {
		if (index.type == 2) $.report.monitor("otherMailReg"), index.otherMailRegReport = true;
		if (index.type == 1) $.report.monitor("QQMailReg"), index.QQMailRegReport = true
	},
	numRegReport: function() {
		if (!index.numRegFlag) $.report.monitor("numReg"), index.numRegFlag = true
	},
	changeInit: function() {
		$.http.get(index.getInitUrl(), null, function(a) {
			index.showCodeByElevel(a.elevel)
		})
	},
	getSessionMachineCookie: function() {
		$.cookie.get("sessionCookie");
		$.cookie.get("machineCookie")
	},
	init: function() {
		if (!index.inited) {
			index.setFromId();
			index.setCloseAppId();
			$("other_email").value = "";
			$("self_email").value = "";
			$("nick").value = "";
			$("code").value = "";
			var a = $.winName.get("type");
			index.type = a == "" ? index.initIndexType : a;
			index.type = index.type != 0 ? 2 : 0;
			if (a = $.bom.query("type")) index.type = a;
			index.type == 0 ? ($("email_box").className = "hide", index.iptFocus("nick")) : index.type == 2 ? (index.changeMethod(2), $("email_box").className = "", index.iptFocus("other_email"), index.mailRegReport(2)) : (index.changeMethod(1), $("email_box").className = "", index.iptFocus("self_email"), index.mailRegReport(1));
			index.changeTab(index.type);
			$.http.get(index.getInitUrl(), {
				cookieCode: index.getSessionMachineCookie()
			}, function(a) {
				index.initInfo = a;
				index.country = a.countryid ? a.countryid : index.initAddress[0];
				index.province = a.provinceid ? a.provinceid : index.initAddress[2];
				index.city = a.cityid ? a.cityid : index.initAddress[4];
				$("country_value").value = a.country ? a.country : index.initAddress[1];
				$("province_value").value = a.province ? a.province : index.initAddress[3];
				$("city_value").value = a.city ? a.city : index.initAddress[5];
				index.showCodeByElevel(a.elevel);
				$.http.jsonp("http://id1.idqqimg.com/zc/chs/js/10029/location_chs.js");
				$.http.loadScript("http://id1.idqqimg.com/zc/chs/js/10029/calendar.js", function() {
					index.initMaxDate();
					index.initBirthday()
				});
				window.setTimeout(function() {
					$.http.jsonp(index.aq_js)
				}, 3E3);
				$.cookie.get("sessionCookie") || $.report.monitor("no_sessionCookie");
				navigator.cookieEnabled || $.report.monitor("cookie_disable")
			});
			$.e.add($("other_email"), "focus", function() {
				$("other_email_bg").className = "bg_txt bg_focus";
				(this.value != index.otherEmail || this.value == "") && index.showTip("email_info", index.otherEmailE[4])
			});
			$.e.add($("other_email"), "keyup", function(a) {
				var c = this.value,
					a = a.keyCode;
				a != index.keyCode.UP && a != index.keyCode.DOWN && a != index.keyCode.ENTER && a != index.keyCode.TAB && a != index.keyCode.F5 && index.createEmailTips(c);
				/^[^a-z0-9]/i.test(c) ? index.showTip("email_info", index.otherEmailE[2]) : index.showTip("email_info", index.otherEmailE[4])
			});
			$.e.add($("other_email"), "blur", function() {
				$("other_email_bg").className = "bg_txt";
				index.isChangingTab() || index.chkOtherEMail()
			});
			$.e.add($("self_email"), "focus", function() {
				this.className = "txt focus";
				(this.value != index.selfEmail || this.value == "") && index.showTip("email_info", index.selfEmailE[4])
			});
			$.e.add($("self_email"), "keyup", function() {
				var a = this.value;
				/^[^a-z]+/i.test(a) ? index.showTip("email_info", index.selfEmailE[2]) : /[^a-z0-9_.-]/i.test(a) ? index.showTip("email_info", index.selfEmailE[4]) : /[._-]{2,}/.test(a) ? index.showTip("email_info", index.selfEmailE[5]) : /[^a-z0-9]+$/i.test(a) ? index.showTip("email_info", index.selfEmailE[6]) : index.showTip("email_info", index.selfEmailE[4])
			});
			$.e.add($("self_email"), "blur", function() {
				this.className = "txt";
				index.isChangingTab() || index.chkSelfEMail()
			});
			$.e.add($("selfType"), "focus", function() {
				$.css.addClass(this, "focus")
			});
			$.e.add($("selfType"), "blur", function() {
				$.css.removeClass(this, "focus")
			});
			$.e.add($("selfType"), "click", function(a) {
				a.stopPropagation();
				index.switchType()
			});
			$.e.add($("selfType0"), "click", function() {
				index.selfType = 0;
				$("selfType").innerHTML = "@qq.com";
				index.hideType()
			});
			$.e.add($("selfType1"), "click", function() {
				index.selfType = 1;
				$("selfType").innerHTML = "@foxmail.com";
				index.hideType()
			});
			$.e.add($("selfType0"), "mousemove", function(a) {
				this.className = "hover";
				$("selfType1").className = "";
				a.stopPropagation()
			});
			$.e.add($("selfType0"), "mouseout", function(a) {
				this.className = "";
				a.stopPropagation()
			});
			$.e.add($("selfType1"), "mousemove", function(a) {
				this.className = "hover";
				$("selfType0").className = "";
				a.stopPropagation()
			});
			$.e.add($("selfType1"), "mouseout", function(a) {
				this.className = "";
				a.stopPropagation()
			});
			$.e.add("selfType", "keydown", function(a) {
				a.stopPropagation();
				$("selfTypeBox");
				index.moveList(this, $("selfTypeBox"), a)
			});
			$.e.add($("password"), "paste", function(a) {
				a.preventDefault();
				return false
			});
			$.e.add($("password_again"), "paste", function(a) {
				a.preventDefault();
				return false
			});
			$.e.add($("nick"), "focus", function() {
				$("nick_bg").className = "bg_txt bg_focus";
				index.showTip("nick_info", index.nickE[2])
			});
			$.e.add($("nick"), "blur", function() {
				$("nick_bg").className = "bg_txt";
				index.hideInfo("nick_info");
				if (!index.isChangingTab() && index.chkNick()) {
					var a = indexType2RegType(index.type);
					index.ajaxChkNick($("nick").value, a)
				}
			});
			$.e.add($("nick"), "keyup", function(a) {
				var c = this.value;
				c == "" ? index.showTip("nick_info", index.nickE[2]) : c.trim() == "" ? index.showTip("nick_info", index.nickE[1]) : $.str.getBytes(c) > 24 ? ($("nick_info").className = "error", $("nick_info").innerHTML = index.nickE[4]) : index.showTip("nick_info", index.nickE[2]);
				a = a || window.event;
				index.setCode(a.keyCode, 0)
			});
			$.e.add($("password"), "focus", function() {
				index.chkNick();
				$("password_bg").className = "bg_txt bg_focus";
				index.hidePwRank();
				index.pwdTime = new Date
			});
			$.e.add($("password"), "blur", function() {
				index.getPwdTips($("password").value);
				$("password_bg").className = "bg_txt";
				index.pwd_valid ? index.showPwRank() : index.hidePwRank();
				index.pwdTimeArray[0] += new Date - index.pwdTime
			});
			$.e.add($("password"), "keydown", function() {});
			$.e.add($("password"), "keyup", function(a) {
				index.getPwdTips($("password").value);
				a = a || window.event;
				index.setCode(a.keyCode, 2);
				index.pwdNum++
			});
			$.e.add($("password_again"), "focus", function() {
				$("password_again_bg").className = "bg_txt bg_focus";
				index.chkNick();
				index.chkPassword();
				(this.value || this.value !== $("password").value) && index.showTip("password_again_info", index.passAgainE[1])
			});
			$.e.add($("password_again"), "blur", function(a) {
				$("password_again_bg").className = "bg_txt";
				index.chkPasswordAgain();
				a.stopPropagation()
			});
			$.e.add($("password_again"), "keyup", function(a) {
				a = a || window.event;
				index.setCode(a.keyCode, 4);
				!this.value && this.value === $("password").value ? ($("password_again_info").className = "ok", $("password_again_info").innerHTML = "") : $("password").value.indexOf(this.value) === 0 || !this.value ? index.showTip("password_again_info", index.passAgainE[1]) : (index.showTip("password_again_info", index.passAgainE[0]), $("password_again_info").className = "error")
			});
			$.e.add($("sex_1"), "click", function() {
				index.sex = 1;
				$("sex_1").className = "checked_focus";
				$("sex_2").className = "";
				index.chkNick();
				index.chkPassword();
				index.chkPasswordAgain();
				index.chkSex()
			});
			$.e.add($("sex_2"), "click", function() {
				index.sex = 2;
				$("sex_1").className = "";
				$("sex_2").className = "checked_focus";
				index.chkNick();
				index.chkPassword();
				index.chkPasswordAgain();
				index.chkSex()
			});
			$.e.add($("sex_1"), "keydown", function(a) {
				switch (a.keyCode) {
				case index.keyCode.ENTER:
					index.sex = 1, $("sex_1").className = "checked_focus", $("sex_2").className = "", index.chkNick(), index.chkPassword(), index.chkPasswordAgain(), index.chkSex(), a.stopPropagation(), a.preventDefault()
				}
			});
			$.e.add($("sex_2"), "keydown", function(a) {
				switch (a.keyCode) {
				case index.keyCode.ENTER:
					index.sex = 2, $("sex_2").className = "checked_focus", $("sex_1").className = "", index.chkNick(), index.chkPassword(), index.chkPasswordAgain(), index.chkSex(), a.stopPropagation(), a.preventDefault()
				}
			});
			$.e.add($("sex_1"), "focus", function() {
				index.sex == 1 ? $("sex_1").className = "checked_focus" : $("sex_1").className = "unchecked_focus"
			});
			$.e.add($("sex_1"), "blur", function() {
				index.sex == 1 ? $("sex_1").className = "checked" : $("sex_1").className = "unchecked"
			});
			$.e.add($("sex_2"), "focus", function() {
				index.sex == 2 ? $("sex_2").className = "checked_focus" : $("sex_2").className = "unchecked_focus"
			});
			$.e.add($("sex_2"), "blur", function() {
				index.sex == 2 ? $("sex_2").className = "checked" : $("sex_2").className = "unchecked"
			});
			$.e.add($("code"), "focus", function() {
				index.chkNick();
				index.chkPassword();
				index.chkPasswordAgain();
				index.chkSex();
				index.chkBirthday();
				index.chkArea();
				this.className = "code_ipt focus";
				index.hideInfo("code_info_err");
				$("code_info_err").className = "tips";
				$("code_info_err").innerHTML = index.codeE[1]
			});
			$.e.add($("code"), "blur", function() {
				this.className = "code_ipt";
				index.chkCode()
			});
			$.e.add($("code"), "keydown", function() {
				index.hideInfo("code_info_err")
			});
			g.component.qzone && ($.e.add($("qzone"), "click", function() {
				index.qzone = !index.qzone;
				this.className = index.qzone ? "checked_focus" : "unchecked_focus";
				index.qzone ? index.showItem(2) : index.hideItem(2)
			}), $.e.add($("qzone"), "keydown", function(a) {
				if (a.keyCode == index.keyCode.ENTER) index.qzone = !index.qzone, this.className = index.qzone ? "checked_focus" : "unchecked_focus", index.qzone ? index.showItem(2) : index.hideItem(2), a.stopPropagation(), a.preventDefault()
			}), $.e.add($("qzone"), "focus", function() {
				this.className = index.qzone ? "checked_focus" : "unchecked_focus"
			}), $.e.add($("qzone"), "blur", function() {
				this.className = index.qzone ? "checked" : "unchecked"
			}));
			$.e.add($("nav_1"), "click", function() {
				index.needShowError[2] = 0;
				index.changeTab(0);
				index.changeInit();
				index.numRegReport()
			});
			$.e.add($("nav_2"), "click", function() {
				index.needShowError[0] = 0;
				index.changeTab(2);
				index.changeInit();
				index.mailRegReport(2)
			});
			$.e.add($("agree"), "click", function() {
				index.agreed = !index.agreed;
				this.className = index.agreed ? "a_1 checked_focus" : "a_1 unchecked_focus";
				var a = $("submit");
				index.agreed ? (a.className = "", a.disabled = "", a.title = index.submitE[1]) : (a.className = "disabled", a.disabled = "disabled", a.title = index.submitE[0])
			});
			$.e.add($("agree"), "keydown", function(a) {
				if (a.keyCode == index.keyCode.ENTER) {
					index.agreed = !index.agreed;
					this.className = index.agreed ? "a_1 checked_focus" : "a_1 unchecked_focus";
					var c = $("submit");
					index.agreed ? (c.className = "", c.disabled = "", c.title = index.submitE[1]) : (c.className = "disabled", c.disabled = "disabled", c.title = index.submitE[0]);
					a.stopPropagation();
					a.preventDefault()
				}
			});
			$.e.add($("agree"), "focus", function() {
				this.className = index.agreed ? "a_1 checked_focus" : "a_1 unchecked_focus"
			});
			$.e.add($("agree"), "blur", function() {
				this.className = index.agreed ? "a_1 checked" : "a_1 unchecked"
			});
			$.e.add($("x_switcher"), "click", function(a) {
				index.switchProvision(a)
			});
			$.e.add(document.body, "click", function() {
				index.hideProvision();
				index.hideCountry();
				index.hideProvince();
				index.hideCity();
				index.hideType();
				index.hideBirtydayType();
				index.hideYear();
				index.hideMonth();
				index.hideDay();
				index.hideEmailTips()
			});
			$.e.add($("email_code_ipt"), "keydown", function() {
				$("email_code_ipt_err").innerHTML = "";
				$("email_code_ipt_err").style.display = "none"
			});
			$.e.add($("email_code_ipt"), "blur", function() {
				index.chkEmailCode()
			});
			window.setTimeout(index.reportSource, 300);
			$.e.add($("email_1"), "click", function() {
				index.changeInit()
			});
			$.e.add($("email_2"), "click", function() {
				index.changeInit()
			});
			$.css.hasClass($("nav_1"), "cur") && index.numRegReport();
			$.e.add($("email_info"), "click", function() {
				index.changeMethod(1)
			});
			$.e.add($("email_info"), "mouseover", function() {
				this.setAttribute("_hover", "over")
			});
			$.e.add($("email_info"), "mouseout", function() {
				this.removeAttribute("_hover")
			});
			index.inited = true;
			index.bindEmailTipsEvent();
			index.bindInputSearchEvent();
			$.report.monitor("pv");
			$.http.jsonp("http://a.zc.qq.com/s.js?t=" + Math.random())
		}
	},
	chkSex: function() {
		$("sex_info").className = "info"
	},
	preCheckOtherEmail: function() {
		function a(a) {
			$("email_info").className = "error";
			$("email_info").innerHTML = index.otherEmailE[a]
		}
		var b = $("other_email").value;
		if (!b) return a(0), false;
		if (!index.emailReg.test(b)) return a(2), false;
		if (/[\.@]foxmail.com$/i.test(b)) return a(5), false;
		return /[\.@]qq.com$/i.test(b) ? (a(6), false) : true
	},
	chkEmailCode: function() {
		var a = $("email_code_ipt").value;
		if (a == "") $("email_code_ipt_err").innerHTML = index.codeE[3], $("email_code_ipt_err").style.display = "inline-block";
		else if (a.length < 4) $("email_code_ipt_err").innerHTML = index.codeE[2], $("email_code_ipt_err").style.display = "inline-block";
		else return $("email_code_ipt_err").innerHTML = "", $("email_code_ipt_err").style.display = "none", a;
		return false
	},
	ajaxChkEmail: function(a, b, c) {
		if (!a) {
			var d = index.chkEmailCode();
			if (!d) {
				$("email_code_ipt").select();
				$("email_code_ipt").focus();
				return
			}
			a = index.ajaxChkEmail.url + "&verifycode=" + d;
			b = index.ajaxChkEmail.isOther;
			c = index.ajaxChkEmail.str
		}
		$.get(a, null, function(d) {
			index.hideEmailCode.needChange = false;
			switch (d.ec) {
			case 0:
				$("email_info").className = "ok";
				$("email_info").innerHTML = index.type == 1 ? index.otherEmailE[3] : "";
				b ? index.otherEmail = c : index.selfEmail = c;
				index.hideEmailCode();
				break;
			case 2:
				$("email_code_img").src = index.codeUrl + "?r=" + Math.random();
				$("email_code_ipt").focus();
				$("email_code_ipt").select();
				$("email_code_ipt_err").innerHTML = index.codeE[0];
				$("email_code_ipt_err").style.display = "inline-block";
				index.hideEmailCode.needChange = true;
				break;
			case 7:
				$("email_info").className = "error";
				$("email_info").innerHTML = index.otherEmailE[2];
				index.hideEmailCode();
				break;
			case 8:
			case 9:
				$("email_info").className = "error";
				$("email_info").innerHTML = index.otherEmailE[1];
				index.pushAlreadyUsedEmails(c);
				index.hideEmailCode();
				break;
			case 12:
				index.showEmailCode();
				index.ajaxChkEmail.url = a;
				index.ajaxChkEmail.isOther = b;
				index.ajaxChkEmail.str = c;
				break;
			default:
				$("email_info").className = "error", $("email_info").innerHTML = index.otherEmailE[1], index.hideEmailCode()
			}
			if (d.ec !== 0) index.otherEmail = "", index.selfEmail = ""
		});
		$("code_img").src = index.codeUrl + "&r=" + Math.random()
	},
	preCheckSelfEmail: function() {
		function a(a) {
			index.chkSelfEMail.id = a;
			$("email_info").className = "error";
			$("email_info").innerHTML = index.selfEmailE[index.chkSelfEMail.id]
		}
		var b = $("self_email").value;
		if (!b) return a(0), false;
		if (b.length < 3) return a(1), false;
		if (/^\d+$/.test(b)) return a(2), false;
		if (/^[^a-z]+/i.test(b)) return a(3), false;
		if (/[^a-z0-9_.-]/i.test(b)) return a(4), false;
		if (/[._-]{2,}/.test(b)) return a(5), false;
		if (/[^A-Za-z0-9]+$/.test(b)) return a(6), false;
		return index.emailHasAlreadyUsed(b) ? ($("email_info").className = "error", $("email_info").innerHTML = index.otherEmailE[1], false) : true
	},
	chkSelfEMail: function() {
		if (index.type == 1 && index.preCheckSelfEmail()) {
			var a = $("self_email").value,
				b = index.host + index.selfChkUrl + "?email=" + a + (index.selfType == 0 ? "@qq.com" : "@foxmail.com") + "&r=" + Math.random();
			index.ajaxChkEmail(b, true, a)
		}
	},
	ajaxChkNick: function(a, b) {
		var c = encodeURIComponent(a),
			c = index.nickChkUrl + "?nick=" + c + "&regType=" + b + "&r=" + Math.random();
		$.get(c, null, function(b) {
			if (b) switch (b.ec) {
			case 0:
				$("nick_info").className = "ok";
				$("nick_info").innerHTML = index.nickE[3];
				index.checkNickMap[a] = 0;
				break;
			case 15:
				$("nick_info").className = "error", $("nick_info").innerHTML = index.nickE[5], index.checkNickMap[a] = 1
			}
		})
	},
	chkNick: function() {
		var a = $("nick").value;
		if (!a) return $("nick_info").className = "error", $("nick_info").innerHTML = index.nickE[0], false;
		if (!a.trim()) return $("nick_info").className = "error", $("nick_info").innerHTML = index.nickE[1], false;
		if ($.str.getBytes(a) > 24) return $("nick_info").className = "error", $("nick_info").innerHTML = index.nickE[4], false;
		if (index.checkNickMap[a] === 1) return $("nick_info").className = "error", $("nick_info").innerHTML = index.nickE[5], false;
		if (index.checkNickMap[a] === 0) $("nick_info").className = "ok", $("nick_info").innerHTML = index.nickE[3];
		return true
	},
	chkPassword: function() {
		index.pwd_valid && index.showPwRank();
		return index.pwd_valid
	},
	getPwdTips: function(a) {
		var b = true;
		a == "" ? ($("pwd_tip1").className = "default", $("pwd_tip2").className = "default", $("pwd_tip3").className = "default", b = false) : (a.length >= index.minPwdLen && a.length <= index.maxPwdLen ? $("pwd_tip1").className = "yes" : ($("pwd_tip1").className = "no", b = false), /^\d{1,8}$/.test(a) ? ($("pwd_tip2").className = "no", b = false) : $("pwd_tip2").className = "yes", /\s/.test(a) ? ($("pwd_tip3").className = "no", b = false) : $("pwd_tip3").className = "yes");
		return index.pwd_valid = b
	},
	chkPasswordAgain: function() {
		var a = $("password").value,
			b = $("password_again").value;
		$("password_again_info").className = "error";
		if (!b) return $("password_again_info").innerHTML = index.passAgainE[1], false;
		if (b !== a) return $("password_again_info").innerHTML = index.passAgainE[0], false;
		if (a.length <= index.maxPwdLen && a.length >= index.minPwdLen && !/^\d{1,8}$/.test(a)) return $("password_again_info").className = "ok", $("password_again_info").innerHTML = "", true;
		index.hideInfo("password_again_info");
		return true
	},
	chkOtherEMail: function() {
		if (index.type == 2 && index.preCheckOtherEmail()) {
			var a = $("other_email").value,
				b = index.host + index.otherChkUrl + "?other_email=" + a + "&r=" + Math.random();
			index.ajaxChkEmail(b, true, a)
		}
	},
	chkBirthday: function() {
		return index.birthType == "" || index.year == "" || index.month == "" || index.day == "" ? ($("birthday_info").className = "error", $("birthday_info").innerHTML = index.birthdayE[0], false) : (index.showBirthdayInfo(), true)
	},
	chkArea: function() {
		return index.country == index.noAreaStr ? ($("area_info").className = "error", $("area_info").innerHTML = index.areaE[0], false) : index.country == "1" ? index.province == index.noAreaStr ? ($("area_info").className = "error", $("area_info").innerHTML = index.areaE[0], false) : ($("area_info").className = "ok", $("area_info").innerHTML = "", true) : ($("area_info").className = "ok", $("area_info").innerHTML = "", true)
	},
	chkCode: function() {
		if (index.initInfo && (index.initInfo.elevel == "1" || index.initInfo.elevel == "2")) {
			var a = $("code").value;
			if (a.length < 4) return $("code_info_err").className = "", $("code_info_err").innerHTML = index.codeE[!a ? 3 : 2], false;
			else $("code_info_err").className = "tips", $("code_info_err").innerHTML = "&nbsp"
		}
		return true
	},
	chkAgree: function() {
		return index.agreed
	},
	changeCode: function() {
		$("code_img").src = index.codeUrl + "&r=" + Math.random();
		$("code").value = "";
		$("code").focus();
		index.setCode(null, 6)
	},
	changeEmailCode: function() {
		$("email_code_img").src = index.codeUrl + "&r=" + Math.random();
		$("email_code_ipt").value = "";
		$("email_code_ipt").focus()
	},
	hideInfo: function(a) {
		$.css.addClass($(a), "hidden")
	},
	showTip: function(a, b) {
		$(a).innerHTML = b;
		$(a).className = "tip"
	},
	changeTab: function(a) {
		$.winName.set("type", a);
		index.type = a;
		$("email_box").className = a == 0 ? "hide" : "";
		$("nav_1").className = a == 0 ? "nav_box cur" : "nav_box";
		$("nav_2").className = a == 0 ? "nav_box" : "nav_box cur";
		if (g.component.qzone) $("qzone_box").className = a == 0 ? "box box_10" : "hide";
		a == 0 ? ($("nick").focus(), $("nick").select(), g.component.qzone && (index.qzone ? index.showItem(2) : index.hideItem(2))) : a == 2 && (index.changeMethod(2), g.component.qzone && index.hideItem(2), $("other_email").focus(), $("other_email").select())
	},
	hideItem: function(a) {
		if (a = $("item_" + a)) a.style.display = "none"
	},
	showItem: function(a) {
		if (a) {
			if (a = $("item_" + a)) a.style.display = "inline"
		} else for (var b = 1; b <= index.totol; b++) if (a = $("item_" + b)) a.style.display = "inline"
	},
	changeMethod: function(a) {
		$.winName.set("type", a);
		$("mail_box").className = a == 1 ? "ipt_box nobg self" : "ipt_box nobg other";
		index.type = a;
		a == 2 ? index.iptFocus("other_email") : a == 1 && index.iptFocus("self_email")
	},
	changeQzone: function() {},
	agree: function(a) {
		index.agreed = !index.agreed;
		a.className = index.agreed ? "a_1 checked" : "a_1"
	},
	switchProvision: function(a) {
		index.showing = !index.showing;
		$("x_box").className = index.showing ? "x_box show" : "x_box";
		a.stopPropagation()
	},
	hideProvision: function() {
		index.showing = false;
		$("x_box").className = "x_box"
	},
	submit: function() {
		isd_t.push(new Date - 0);
		var a = index.chkAgree(),
			a = index.chkCode() && a,
			a = index.chkBirthday() && a,
			a = index.chkArea() && a,
			a = index.chkPassword() && a,
			a = index.chkPasswordAgain() && a,
			a = index.chkNick() && a;
		index.type == 1 && !index.preCheckSelfEmail() ? a = false : index.type == 2 && !index.preCheckOtherEmail() && (a = false);
		if (a) {
			$.winName.set("fromId", index.fromId);
			index.setCodeCookie();
			a = "";
			index.birthType == 1 && (a = calendar.getDate(parseInt(index.year), parseInt(index.month), parseInt(index.day), 1, parseInt(index.isLeap)));
			var b = {
				verifycode: $("code").value,
				qzone_flag: index.type == 0 && index.qzone ? 1 : 0,
				country: index.country,
				province: index.province,
				city: index.city,
				isnongli: index.birthType,
				year: index.year,
				month: index.month,
				day: index.day,
				isrunyue: index.isLeap == "1" ? 0 : 1,
				password: index.rsaEncrypt($("password").value),
				nick: $("nick").value,
				email: index.type == 1 && $("self_email").value + (index.selfType == 0 ? "@qq.com" : "@foxmail.com"),
				other_email: index.type == 2 && $("other_email").value,
				elevel: index.initInfo.elevel,
				sex: index.sex,
				qzdate: a,
				jumpfrom: index.fromId
			};
			b.nick = encodeURIComponent(b.nick);
			b.password = encodeURIComponent(b.password);
			b.email = encodeURIComponent(b.email);
			b.other_email = encodeURIComponent(b.other_email);
			b.csloginstatus = g.getQQnum();
			if (index.ptlang) b.ptlang = index.ptlang;
			if (index.ADUIN) b.ADUIN = index.ADUIN;
			if (index.ADSESSION) b.ADSESSION = index.ADSESSION;
			for (var c in index.aq_object) b[c] = index.aq_object[c];
			$.post(index.getSubmitUrl(), b, function(a) {
				if (a) switch (isd_t.push(new Date - 0), $.report.isd(isd_t), $.cookie.set("index_ec", a.ec, "zc.qq.com", "/", 0.5), a.ec) {
				case 0:
					$.winName.set("temp_last_send", 0);
					$.winName.set("gurad_phone", "");
					$.cookie.set("nick", b.nick, "zc.qq.com", "/", 0.5);
					$.winName.set("_new_uin", a.uin);
					var c = index.getPwdRank($("password").value);
					index.pwdTimeArray[c] = index.pwdNum * 1E3;
					switch (c) {
					case 1:
						$.report.monitor("weakPwd");
						break;
					case 2:
						$.report.monitor("midPwd");
						break;
					case 3:
						$.report.monitor("strongPwd")
					}
					$.report.isdPwdTime(index.pwdTimeArray);
					switch (parseInt(index.type)) {
					case 0:
						$.winName.set("last_page", 1);
						if (g_lang === 1 && Math.floor(Math.random() * index.max_selective_rate) < index.selective_rate) {
							var f, a = [];
							for (f in b) $.winName.set("user_" + f, b[f]), a.push(f);
							$.report.monitor("QQHuiyuan");
							$.winName.set("user_attrs", a.join(","));
							window.location = index.selective_decimal_ok
						} else window.location = index.decimal_ok;
						break;
					case 1:
						$.winName.set("_email", a.email);
						$.winName.set("last_page", 1);
						window.location = index.email_ok;
						break;
					case 2:
						window.location = index.send_ok
					}
					break;
				case 2:
					$("code_info_err").className = "";
					$("code_info_err").innerHTML = index.codeE[0];
					index.changeCode();
					$("code").blur();
					index.code = "";
					break;
				case 5:
					$("birthday_info").className = "error";
					$("birthday_info").innerHTML = index.birthE[1];
					break;
				case 8:
				case 9:
					$("email_info").className = "error";
					$("email_info").innerHTML = index.otherEmailE[1];
					index.hideEmailCode();
					break;
				case 13:
				case 15:
					$("nick_info").className = "error";
					$("nick_info").innerHTML = index.nickE[5];
					break;
				case 20:
					$.cookie.setSessionCookie("param", encodeURIComponent(index.json2str(b)), "zc.qq.com", "/");
					$.winName.set("last_page", 1);
					window.location = "phone_verify.html";
					break;
				case 26:
					$.cookie.setSessionCookie("param", encodeURIComponent(index.json2str(b)), "zc.qq.com", "/", 0.5);
					$.winName.set("last_page", 1);
					window.location = "phone_verify_up.html";
					break;
				case 21:
					window.location = "worst.html?ec=21";
					break;
				case 30:
					window.location = "worst.html?ec=30";
					break;
				default:
					window.location = "error.html?ec=" + a.ec
				}
			})
		}
		$.report.monitor("submit", {
			regType: index.type
		});
		return false
	},
	loadLocation: function(a) {
		index.location = a;
		$("country_box");
		var b = $("country_value"),
			c = $("country_ul");
		$("province_box");
		var d = $("province_value"),
			e = $("province_ul"),
			f = $("city_value"),
			h = $("city_ul");
		$("city_box");
		index.changeCountry();
		$.e.add(b, "click", function(a) {
			index.hideProvince();
			index.hideCity();
			index.hideBirtydayType();
			index.hideYear();
			index.hideMonth();
			index.hideDay();
			a.stopPropagation();
			index.selectListState[4] && (index.changeCountry(), index.selectListState[4] = 0);
			index.switchCountry()
		});
		$.e.add(c, "click", function(a) {
			var c = a.target;
			if (c.nodeName.toLowerCase() != "li") a.stopPropagation();
			else {
				var d = index.country,
					e = c.getAttribute("value");
				index.country = e;
				c = $.html.decode(c.innerHTML);
				c.length > 6 ? ($("country_value").title = c, $("country_value").value = index.isEnglishWord(c) ? c.substring(0, 12) : c.substring(0, 6)) : ($("country_value").title = "", $("country_value").value = c);
				index.selectHasSelected[4] = true;
				index.hideCountry();
				a.stopPropagation();
				d != index.country && (index.changeProvince(), index.changeCity());
				index.updateSelectListIndex(4, index.listIndex[4]);
				b.focus()
			}
		});
		$.e.add(c, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				var c = $("country_" + index.listIndex[4]);
				if (c) c.className = "";
				b.className = "hover";
				index.listIndex[4] = index.getIndexFromId(b.getAttribute("id"));
				a.stopPropagation()
			}
		});
		$.e.add(c, "mouseout", function(a) {
			if (a.target.tagName.toLowerCase() == "li") a.target.className = "", a.stopPropagation()
		});
		index.province != index.noAreaStr && index.changeProvince(index.province);
		$.e.add(d, "click", function(a) {
			index.hideCountry();
			index.hideCity();
			index.hideBirtydayType();
			index.hideYear();
			index.hideMonth();
			index.hideDay();
			a.stopPropagation();
			d.className.indexOf("hide") > -1 || (index.selectListState[5] && (index.changeProvince(null, true), index.selectListState[5] = 0), index.switchProvince())
		});
		$.e.add(e, "click", function(a) {
			var b = a.target;
			if (b.nodeName.toLowerCase() != "li") a.stopPropagation();
			else {
				var c = index.province,
					e = b.getAttribute("value");
				index.province = e;
				b = $.html.decode(b.innerHTML);
				b.length > 6 ? ($("province_value").title = b, $("province_value").value = index.isEnglishWord(b) ? b.substring(0, 12) : namprovinceNamee.substring(0, 6)) : ($("province_value").title = "", $("province_value").value = b);
				index.selectHasSelected[5] = true;
				index.hideProvince();
				a.stopPropagation();
				c != index.province && index.changeCity();
				index.updateSelectListIndex(5, index.listIndex[5]);
				d.focus()
			}
		});
		$.e.add(e, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				var c = $("province_" + index.listIndex[5]);
				if (c) c.className = "";
				b.className = "hover";
				index.listIndex[5] = index.getIndexFromId(b.getAttribute("id"));
				a.stopPropagation()
			}
		});
		$.e.add(e, "mouseout", function(a) {
			if (a.target.tagName.toLowerCase() == "li") a.target.className = "", a.stopPropagation()
		});
		index.city != index.noAreaStr && index.changeCity(index.city);
		$.e.add(f, "click", function(a) {
			index.hideCountry();
			index.hideProvince();
			index.hideBirtydayType();
			index.hideYear();
			index.hideMonth();
			index.hideDay();
			a.stopPropagation();
			f.className.indexOf("hide") > -1 || (index.selectListState[6] && (index.changeCity(null, true), index.selectListState[6] = 0), index.switchCity())
		});
		$.e.add(h, "click", function(a) {
			var b = a.target;
			if (b.nodeName.toLowerCase() != "li") a.stopPropagation();
			else {
				var c = b.getAttribute("value");
				index.city = c;
				b = $.html.decode(b.innerHTML);
				b.length > 6 ? ($("city_value").title = b, $("city_value").value = index.isEnglishWord(b) ? b.substring(0, 12) : b.substring(0, 6)) : ($("city_value").title = "", $("city_value").value = b);
				index.selectHasSelected[6] = true;
				index.hideCity();
				a.stopPropagation();
				index.updateSelectListIndex(6, index.listIndex[6]);
				f.focus()
			}
		});
		$.e.add(h, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				var c = $("city_" + index.listIndex[6]);
				if (c) c.className = "";
				b.className = "hover";
				index.listIndex[6] = index.getIndexFromId(b.getAttribute("id"));
				a.stopPropagation()
			}
		});
		$.e.add(h, "mouseout", function(a) {
			if (a.target.tagName.toLowerCase() == "li") a.target.className = "", a.stopPropagation()
		});
		$.e.add(b, "keydown", function(a) {
			index.moveList(b, c, a, 4)
		});
		$.e.add(d, "keydown", function(a) {
			index.moveList(d, e, a, 5)
		});
		$.e.add(f, "keydown", function(a) {
			index.moveList(f, h, a, 6)
		});
		$.e.add(b, "focus", function() {
			$("country_value_bg").className = "area_value_bg_focus";
			window.setTimeout(function() {
				b.select()
			}, 100)
		});
		$.e.add(b, "blur", function() {
			$("country_value_bg").className = "area_value_bg";
			var a = index.country;
			index.selectHasSelected[4] || (index.setSelectBlurValue(c, b, 4), a != index.country && (index.changeProvince(), index.changeCity()));
			window.clearTimeout(index.searchTimeoutId[4]);
			index.hideInputSearchTips();
			index.chkArea()
		});
		$.e.add(d, "focus", function() {
			$("province_value_bg").className = "area_value_bg_focus";
			window.setTimeout(function() {
				d.select()
			}, 100)
		});
		$.e.add(d, "blur", function() {
			index.chkArea();
			$("province_value_bg").className = "area_value_bg";
			var a = index.province;
			index.selectHasSelected[5] || (index.setSelectBlurValue(e, d, 5), a != index.province && index.changeCity());
			window.clearTimeout(index.searchTimeoutId[5]);
			index.hideInputSearchTips()
		});
		$.e.add(f, "focus", function() {
			$("city_value_bg").className = "area_value_bg_focus";
			window.setTimeout(function() {
				f.select()
			}, 100)
		});
		$.e.add(f, "blur", function() {
			index.chkArea();
			$("city_value_bg").className = "area_value_bg";
			index.selectHasSelected[6] || index.setSelectBlurValue(h, f, 6);
			window.clearTimeout(index.searchTimeoutId[6]);
			index.hideInputSearchTips()
		});
		index.bindTimeSearchEvent();
		index.bindAreaSearchEvent()
	},
	switchType: function() {
		index.switchType.showing ? ($("selfTypeBox").className = "hide", index.switchType.showing = false) : ($("selfTypeBox").className = "", index.switchType.showing = true)
	},
	hideType: function() {
		$("selfTypeBox").className = "hide";
		index.switchType.showing = false
	},
	changeCountry: function() {
		var a = $("country_ul"),
			b = "",
			b = "",
			c = 0,
			d = index.location,
			e;
		for (e in d) e == index.country && index.updateListIndex(4, c), b += '<li value="' + e + '" id=' + ("country_" + c) + ">" + d[e].n + "</li>", c++;
		c == 0 && index.updateListIndex(4, -1);
		a.innerHTML = b
	},
	changeProvince: function(a, b) {
		if (index.country == index.noAreaStr) return $("province_ul").innerHTML = "", index.updateListIndex(5, -1), false;
		var c = index.location[index.country],
			d = "",
			e = "";
		if (!index.country || c["0"]) index.province = index.noAreaStr, $("province_value").className = "hide", $("province_ul").className = "hide", $("province_ul").innerHTML = "", $("province_box").className = "disable_box";
		else {
			$("province_value").className = "province_value";
			if (a) d = c[a] ? c[a].n : "", index.province = a;
			var f = 0,
				h;
			for (h in c) if (h != "n") {
				if (d == "") {
					if (d = c[h].n, !b) index.province = h, index.updateListIndex(5, 0)
				} else h == index.province && index.updateListIndex(5, f);
				e += '<li value="' + h + '" id=' + ("province_" + f) + ">" + c[h].n + "</li>";
				f++
			}
			if (f == 0) index.updateListIndex(5, -1), index.province = index.noAreaStr, $("province_value").className = "hide", $("province_ul").className = "hide", $("province_ul").innerHTML = "", $("province_box").className = "disable_box";
			else {
				if (!b) $("province_value").value = d;
				$("province_ul").innerHTML = e
			}
		}
	},
	changeCity: function(a, b) {
		if (index.country == index.noAreaStr) return $("city_ul").innerHTML = "", index.updateListIndex(6, -1), false;
		$("city_value").className = "city_value";
		var c = index.location[index.country],
			d = "",
			e = "",
			f = 0,
			h;
		for (h in c) if (f++, f >= 3) break;
		switch (f) {
		case 1:
			c = null;
			$("city_value").className = "hide";
			$("city_ul").className = "hide";
			$("city_ul").innerHTML = "";
			break;
		case 2:
			c = c[0];
			break;
		case 3:
			c = c[index.province]
		}
		if (a) d = c[a] ? c[a].n : "", index.city = a;
		f = 0;
		for (h in c) if (h != "n" && c[h].n) {
			if (d == "") {
				if (d = c[h].n, !b) index.city = h, index.updateListIndex(6, 0)
			} else h == index.city && index.updateListIndex(6, f);
			e += '<li value="' + h + '" id=' + ("city_" + f) + ">" + c[h].n + "</li>";
			f++
		}
		if (f == 0) index.city = index.noAreaStr, $("city_value").className = "hide", $("city_box").className = "disable_box", index.updateListIndex(6, -1);
		if (!b) $("city_value").value = d;
		$("city_ul").innerHTML = e
	},
	search_area: function(a, b, c) {
		$.get(a, null, function(a) {
			if (a && a.ec == 0) {
				a = index.searchResultToMap(a.list);
				index.selectHasSelected[c] = false;
				index.showUl(b);
				b.scrollTop = 0;
				var e = "",
					f = 0,
					h;
				for (h in a) {
					var i = "country_" + f;
					e += f == 0 ? '<li class="hover" value="' + h + '" id=' + i + ">" + a[h] + "</li>" : '<li value="' + h + '" id=' + i + ">" + a[h] + "</li>";
					f++
				}
				if (f > 0) index.updateListIndex(c, 0), b.className = "";
				else {
					e = '<p class="red_bg">' + index.areaE[1] + "</p>";
					switch (c) {
					case 4:
						index.country = index.noAreaStr;
						break;
					case 5:
						index.province = index.noAreaStr;
						break;
					case 6:
						index.city = index.noAreaStr
					}
					index.updateListIndex(c, -1);
					b.className = "noSearchResult"
				}
				b.innerHTML = e;
				index.selectListState[c] = 1
			}
		})
	},
	hideCountry: function() {
		$("country_ul").className = "hide";
		index.switchCountry.isShow = false
	},
	switchCountry: function() {
		index.switchCountry.isShow = !index.switchCountry.isShow;
		$("country_ul").className = index.switchCountry.isShow ? "" : "hide";
		if (index.switchCountry.isShow) {
			$("country_ul").scrollTop = index.getSelectScrollTop(4);
			var a = index.getSelectListItem(4);
			if (a) a.className = "hover";
			index.selectHasSelected[4] = false
		}
	},
	hideProvince: function() {
		$("province_ul").className = "hide";
		index.switchProvince.isShow = false
	},
	switchProvince: function() {
		index.switchProvince.isShow = !index.switchProvince.isShow;
		$("province_ul").className = index.switchProvince.isShow ? "" : "hide";
		if (index.switchProvince.isShow) {
			$("province_ul").scrollTop = index.getSelectScrollTop(5);
			var a = index.getSelectListItem(5);
			if (a) a.className = "hover";
			index.selectHasSelected[5] = false
		}
	},
	hideCity: function() {
		$("city_ul").className = "hide";
		index.switchCity.isShow = false
	},
	switchCity: function() {
		index.switchCity.isShow = !index.switchCity.isShow;
		$("city_ul").className = index.switchCity.isShow ? "" : "hide";
		if (index.switchCity.isShow) {
			$("city_ul").scrollTop = index.getSelectScrollTop(6);
			var a = index.getSelectListItem(6);
			if (a) a.className = "hover";
			index.selectHasSelected[6] = false
		}
	},
	initBirthday: function() {
		if (g.component.lunar) var a = $("birthday_type_box"),
			b = $("birthday_type_value"),
			c = $("birthday_type_ul");
		$("year_box");
		var d = $("year_value"),
			e = $("year_ul");
		$("month_box");
		var f = $("month_value"),
			h = $("month_ul");
		$("day_box");
		var i = $("day_value"),
			j = $("day_ul");
		d.value = "年";
		f.value = "月";
		i.value = "日";
		index.changeYear();
		g.component.lunar && ($.e.add(a, "click", function(a) {
			index.hideCountry();
			index.hideProvince();
			index.hideCity();
			index.hideYear();
			index.hideMonth();
			index.hideDay();
			index.switchBirtydayType();
			a.stopPropagation()
		}), $.e.add(c, "click", function(a) {
			if (a.target.nodeName.toLowerCase() != "li") a.stopPropagation();
			else {
				var c = index.birthType,
					d = a.target.getAttribute("value");
				index.birthType = d;
				$("birthday_type_value").innerHTML = a.target.innerHTML;
				index.switchBirtydayType();
				index.switchBirtydayType.dom = a.target;
				a.stopPropagation();
				c != index.birthType && (index.updateShowdDate(), index.changeYear(), index.changeMonth(), index.changeDay(), index.showBirthdayInfo());
				index.updateSelectListIndex(0, index.listIndex[0]);
				b.focus()
			}
		}), $.e.add(c, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				index.switchBirtydayType.dom && (index.switchBirtydayType.dom.className = "");
				index.switchBirtydayType.dom = null;
				var c = $("birthday_" + index.listIndex[0]);
				if (c) c.className = "";
				b.className = "hover";
				index.listIndex[0] = index.getIndexFromId(b.getAttribute("id"));
				a.stopPropagation()
			}
		}), $.e.add(c, "mouseout", function(a) {
			if (a.target.tagName.toLowerCase() == "li") a.target.className = "", a.stopPropagation()
		}), $.e.add(b, "keydown", function(a) {
			index.moveList(b, c, a, 0)
		}), $.e.add(b, "focus", function() {
			$.css.addClass(b, "birthday_type_box_focus")
		}), $.e.add(b, "blur", function() {
			$.css.removeClass(b, "birthday_type_box_focus")
		}));
		$.e.add(d, "keydown", function(a) {
			index.moveList(d, e, a, 1)
		});
		$.e.add(f, "keydown", function(a) {
			index.moveList(f, h, a, 2)
		});
		$.e.add(i, "keydown", function(a) {
			index.moveList(i, j, a, 3)
		});
		$.e.add(d, "focus", function() {
			$("year_bg").className = "year_bg_focus";
			window.setTimeout(function() {
				d.select()
			}, 100)
		});
		$.e.add(d, "blur", function() {
			$("year_bg").className = "year_bg_txt";
			index.selectHasSelected[1] || (index.setSelectBlurValue(e, d, 1), index.changeMonth(), index.changeDay(), index.showBirthdayInfo());
			window.clearTimeout(index.searchTimeoutId[1]);
			index.hideInputSearchTips()
		});
		$.e.add(f, "focus", function() {
			f.className = "month_value_focus";
			window.setTimeout(function() {
				f.select()
			}, 100)
		});
		$.e.add(f, "blur", function() {
			f.className = "month_value";
			index.selectHasSelected[2] || (index.setSelectBlurValue(h, f, 2), index.changeDay(), index.showBirthdayInfo());
			window.clearTimeout(index.searchTimeoutId[2]);
			index.hideInputSearchTips()
		});
		$.e.add(i, "focus", function() {
			i.className = "day_value_focus";
			window.setTimeout(function() {
				i.select()
			}, 100)
		});
		$.e.add(i, "blur", function() {
			i.className = "day_value";
			index.selectHasSelected[3] || (index.setSelectBlurValue(j, i, 3), index.showBirthdayInfo());
			window.clearTimeout(index.searchTimeoutId[3]);
			index.chkBirthday();
			index.hideInputSearchTips()
		});
		$.e.add(d, "click", function(a) {
			index.hideCountry();
			index.hideProvince();
			index.hideCity();
			index.hideBirtydayType();
			index.hideMonth();
			index.hideDay();
			index.selectListState[1] && (index.changeYear(), index.selectListState[1] = 0);
			index.switchYear();
			a.stopPropagation()
		});
		$.e.add(e, "click", function(a) {
			var b = a.target;
			if (b.nodeName.toLowerCase() != "li") a.stopPropagation();
			else {
				var c = index.year,
					e = b.getAttribute("value");
				index.year = e;
				index.showDate.year = e;
				d.value = $.html.decode(b.innerHTML);
				index.switchYear();
				index.switchYear.dom = a.target;
				a.stopPropagation();
				c != index.year && (index.changeMonth(), index.changeDay(), index.showBirthdayInfo());
				index.updateSelectListIndex(1, index.listIndex[1]);
				index.selectHasSelected[1] = true;
				d.focus()
			}
		});
		$.e.add(e, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				index.switchYear.dom && (index.switchYear.dom.className = "");
				index.switchYear.dom = null;
				var c = $("year_" + index.listIndex[1]);
				if (c) c.className = "";
				index.listIndex[1] = index.getIndexFromId(b.getAttribute("id"));
				b.className = "hover";
				a.stopPropagation()
			}
		});
		$.e.add(e, "mouseout", function(a) {
			if (a.target.tagName.toLowerCase() == "li") a.target.className = "", a.stopPropagation()
		});
		$.e.add(f, "click", function(a) {
			index.hideCountry();
			index.hideProvince();
			index.hideCity();
			index.hideBirtydayType();
			index.hideYear();
			index.hideDay();
			index.selectListState[2] && (index.changeMonth(), index.selectListState[2] = 0);
			index.switchMonth();
			a.stopPropagation()
		});
		$.e.add(h, "click", function(a) {
			var b = a.target;
			if (b.nodeName.toLowerCase() != "li") a.stopPropagation();
			else {
				var c = index.month,
					d = index.isLeap,
					e = b.getAttribute("value");
				index.month = e;
				index.showDate.month = e;
				index.isLeap = b.getAttribute("isLeap") ? b.getAttribute("isLeap") : 1;
				index.showDate.isLeap = index.isLeap == 1 ? false : true;
				f.value = $.html.decode(b.innerHTML);
				index.switchMonth();
				index.switchMonth.dom = b;
				a.stopPropagation();
				if (c != index.month || d != index.leap) index.changeDay(), index.showBirthdayInfo();
				index.updateSelectListIndex(2, index.listIndex[2]);
				index.selectHasSelected[2] = true;
				f.focus()
			}
		});
		$.e.add(h, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				index.switchMonth.dom && (index.switchMonth.dom.className = "");
				index.switchMonth.dom = null;
				var c = $("month_" + index.listIndex[2]);
				if (c) c.className = "";
				index.listIndex[2] = index.getIndexFromId(b.getAttribute("id"));
				b.className = "hover";
				a.stopPropagation()
			}
		});
		$.e.add(h, "mouseout", function(a) {
			if (a.target.tagName.toLowerCase() == "li") a.target.className = "", a.stopPropagation()
		});
		$.e.add(i, "click", function(a) {
			index.hideCountry();
			index.hideProvince();
			index.hideCity();
			index.hideBirtydayType();
			index.hideYear();
			index.hideMonth();
			index.selectListState[3] && (index.changeDay(), index.selectListState[3] = 0);
			index.switchDay();
			a.stopPropagation()
		});
		$.e.add(j, "click", function(a) {
			var b = a.target;
			if (b.nodeName.toLowerCase() != "li") a.stopPropagation();
			else {
				var c = index.day,
					d = b.getAttribute("value");
				index.day = d;
				index.showDate.day = d;
				i.value = $.html.decode(b.innerHTML);
				index.switchDay();
				index.switchDay.dom = b;
				a.stopPropagation();
				c != index.day && index.showBirthdayInfo();
				index.updateSelectListIndex(3, index.listIndex[3]);
				index.selectHasSelected[3] = true;
				i.focus()
			}
		});
		$.e.add(j, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				index.switchDay.dom && (index.switchDay.dom.className = "");
				index.switchDay.dom = null;
				var c = $("day_" + index.listIndex[3]);
				if (c) c.className = "";
				index.listIndex[3] = index.getIndexFromId(b.getAttribute("id"));
				b.className = "hover";
				a.stopPropagation()
			}
		});
		$.e.add(j, "mouseout", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") b.className = "", a.stopPropagation()
		})
	},
	changeYear: function() {
		var a = index.maxDate.year,
			b = index.showDate.year,
			c = a - 119;
		b > 0 && index.updateListIndex(1, a - b);
		var d = [];
		switch (index.birthType + "") {
		case "0":
			for (var e = a; e >= c; e--) {
				var f = "year_" + (a - e);
				if (e == b) $("year_value").value = b + "年";
				d.push("<li value=" + e + " id=" + f + ">" + e + "年</li>")
			}
			break;
		case "1":
			for (e = a; e >= c; e--) {
				var f = "year_" + (a - e),
					h = calendar.getGanZhi(e + 1, 0, 0, 0);
				if (e == b) $("year_value").value = h + "年(" + e + ")";
				d.push("<li value=" + e + " id=" + f + ">" + h + "年(" + e + ")</li>")
			}
		}
		$("year_ul").innerHTML = d.join(" ");
		index.ulToSelectArr($("year_ul"), 1);
		index.year = b
	},
	changeMonth: function() {
		if (index.year != "") {
			var a = parseInt(index.birthType),
				b = parseInt(index.year),
				c = index.showDate.month;
			c > 0 && index.updateListIndex(2, c - 1);
			var d = [];
			index.month = c;
			switch (index.birthType + "") {
			case "0":
				for (var e = index.inMaxDate(b, c, 1, a, 1), f = 1; f <= 12; f++) {
					var h = "month_" + (f - 1);
					if (f == c) $("month_value").value = f + "月";
					index.inMaxDate(b, f, 1, a, 1) ? d.push("<li value=" + f + " id=" + h + ">" + f + "月</li>") : d.push("<p value=" + f + ' class="gray" title=' + index.noSelectTip + " id=" + h + ">" + f + "月</p>")
				}
				if (!e) $("month_value").value = "1月", index.month = 1, index.showDate.month = 1, index.updateListIndex(2, 0);
				break;
			case "1":
				var e = calendar.getChineseLunarMonth(index.year),
					i = e.leap ? e.leap.m : 0,
					j = index.inMaxDate(b, c, 1, a, index.showDate.isLeap ? 0 : 1);
				(index.showDate.isLeap && c == i || i > 0 && c > i) && index.updateListIndex(2, c);
				for (var f = 1, k = 0; f <= 12; f++, k++) {
					h = "month_" + k;
					if (f == c && ($("month_value").value = index.showDate.isLeap && c == i ? "闰" + e.m[f - 1] : e.m[f - 1], c != i)) index.isLeap = 1, index.showDate.isLeap = false;
					f == i ? (index.inMaxDate(b, f, 1, a, 1) ? d.push("<li value=" + f + " isLeap=1 id=" + h + ">" + e.m[f - 1] + "</li>") : d.push("<p value=" + f + ' class="gray" title=' + index.noSelectTip + " isLeap=1 id=" + h + ">" + e.m[f - 1] + "</p>"), k++, h = "month_" + k, index.inMaxDate(b, f, 1, a, 0) ? d.push("<li value=" + f + " isLeap=0 id=" + h + ">" + e.leap.name + "</li>") : d.push("<p value=" + f + ' class="gray" title=' + index.noSelectTip + " isLeap=0 id=" + h + ">" + e.leap.name + "</p>")) : index.inMaxDate(b, f, 1, a, 1) ? d.push("<li value=" + f + " isLeap=1 id=" + h + ">" + e.m[f - 1] + "</li>") : d.push("<p value=" + f + ' class="gray" title=' + index.noSelectTip + " isLeap=1 id=" + h + ">" + e.m[f - 1] + "</p>")
				}
				if (!j) $("month_value").value = "正月", index.month = 1, index.showDate.month = 1, index.updateListIndex(2, 0), index.isLeap = 1, index.showDate.isLeap = false
			}
			$("month_ul").innerHTML = d.join(" ");
			index.ulToSelectArr($("month_ul"), 2)
		}
	},
	changeDay: function() {
		if (index.month != "") {
			var a = parseInt(index.birthType),
				b = parseInt(index.year),
				c = parseInt(index.month),
				d, e = parseInt(index.showDate.day);
			e > 0 && index.updateListIndex(3, e - 1);
			var f = [];
			index.day = e;
			switch (index.birthType + "") {
			case "0":
				d = calendar.getSolarMonthDays(index.year, index.month);
				var h = index.inMaxDate(b, c, e, a, 1);
				if (e > d || !h) $("day_value").value = "1日", index.showDate.day = 1, index.day = 1, index.updateListIndex(3, 0);
				for (var i = 1; i <= d; i++) {
					var j = "day_" + (i - 1);
					if (i == e && h) $("day_value").value = i + "日";
					index.inMaxDate(b, c, i, a, 1) ? f.push("<li value=" + i + "  id=" + j + ">" + i + "日</li>") : f.push("<p value=" + i + ' class="gray" title=' + index.noSelectTip + " id=" + j + ">" + i + "日</p>")
				}
				break;
			case "1":
				d = calendar.getChineseLunarDay(b, c, index.showDate.isLeap ? 0 : 1);
				h = index.inMaxDate(b, c, e, a, index.showDate.isLeap ? 0 : 1);
				if (e > d.length || !h) $("day_value").value = d[0], index.showDate.day = 1, index.day = 1, index.updateListIndex(3, 0);
				for (var i = 1, k = d.length; i <= k; i++) {
					j = "day_" + (i - 1);
					if (i == e && h) $("day_value").value = d[i - 1];
					index.inMaxDate(b, c, i, a, index.showDate.isLeap ? 0 : 1) ? f.push("<li value=" + i + " id=" + j + ">" + d[i - 1] + "</li>") : f.push("<p value=" + i + ' class="gray" title=' + index.noSelectTip + " id=" + j + " >" + d[i - 1] + "</p>")
				}
			}
			$("day_ul").innerHTML = f.join(" ");
			index.ulToSelectArr($("day_ul"), 3)
		}
	},
	switchBirtydayType: function() {
		if (g.component.lunar && (index.switchBirtydayType.isShow = !index.switchBirtydayType.isShow, $("birthday_type_ul").className = index.switchBirtydayType.isShow ? "" : "hide", index.switchBirtydayType.isShow)) {
			var a = index.getSelectListItem(0);
			if (a) a.className = "hover"
		}
	},
	switchYear: function() {
		index.switchYear.isShow = !index.switchYear.isShow;
		$("year_ul").className = index.switchYear.isShow ? "" : "hide";
		if (index.switchYear.isShow) {
			$("year_ul").scrollTop = index.getSelectScrollTop(1);
			var a = index.getSelectListItem(1);
			if (a) a.className = "hover";
			index.selectHasSelected[1] = false
		}
	},
	switchMonth: function() {
		index.switchMonth.isShow = !index.switchMonth.isShow;
		$("month_ul").className = index.switchMonth.isShow ? "" : "hide";
		if (index.switchMonth.isShow) {
			$("month_ul").scrollTop = index.getSelectScrollTop(2);
			var a = index.getSelectListItem(2);
			if (a) a.className = "hover";
			index.selectHasSelected[2] = false
		}
	},
	switchDay: function() {
		index.switchDay.isShow = !index.switchDay.isShow;
		$("day_ul").className = index.switchDay.isShow ? "" : "hide";
		if (index.switchDay.isShow) {
			$("day_ul").scrollTop = index.getSelectScrollTop(3);
			var a = index.getSelectListItem(3);
			if (a) a.className = "hover";
			index.selectHasSelected[3] = false
		}
	},
	hideBirtydayType: function() {
		if (g.component.lunar) $("birthday_type_ul").className = "hide", index.switchBirtydayType.isShow = false
	},
	hideYear: function() {
		$("year_ul").className = "hide";
		index.switchYear.isShow = false
	},
	hideMonth: function() {
		$("month_ul").className = "hide";
		index.switchMonth.isShow = false
	},
	hideDay: function() {
		$("day_ul").className = "hide";
		index.switchDay.isShow = false
	},
	showBirthdayInfo: function() {
		var a = "",
			b = "";
		if (index.year > 0 && index.month > 0 && index.day > 0) a = calendar.getZodiac(index.year, index.month, index.day, index.birthType, index.isLeap), b = calendar.getConstellation(parseInt(index.year), parseInt(index.month), parseInt(index.day), parseInt(index.birthType), parseInt(index.isLeap)), $("birthday_info").innerHTML = "属" + a + " " + b, $("birthday_info").className = "birthdayTip"
	},
	showEmailCode: function() {
		$("email_code_img").src = index.codeUrl + "?r=" + Math.random();
		$("email_code_ipt").value = "";
		$("chk_email_code_box").style.display = "block";
		$("cover").style.display = "block"
	},
	hideEmailCode: function() {
		$("chk_email_code_box").style.display = "none";
		$("cover").style.display = "none";
		if ((index.initInfo.elevel == "1" || index.initInfo.elevel == "2") & index.hideEmailCode.needChange) $("code_img").src = index.codeUrl + "?r=" + Math.random(), $("code").value = ""
	},
	generateEmailTips: function(a) {
		for (var b = a.indexOf("@"), c = "", c = b == -1 ? a : a.substring(0, b), b = [], d = 0, e = index.knownEmail.length; d < e; d++) b.push(c + "@" + index.knownEmail[d]);
		c = [];
		c.push(a);
		d = 0;
		for (e = b.length; d < e; d++) b[d].indexOf(a) > -1 && c.push(b[d]);
		return c
	},
	hideEmailTips: function() {
		$("other_email_ul").className = "hide"
	},
	createEmailTips: function(a) {
		index.updateListIndex(7, 0);
		var a = index.generateEmailTips(a),
			b = [],
			c = "";
		b.push("<p>请选择邮箱类型</p>");
		for (var d = 0, e = a.length; d < e && d < 10; d++) c = "emailTips_" + d, 0 == d ? b.push("<li id=" + c + " class='hover' >" + $.html.encode(a[d]) + "</li>") : b.push("<li id=" + c + ">" + $.html.encode(a[d]) + "</li>");
		$("other_email_ul").className = "other_email_ul";
		$("other_email_ul").innerHTML = b.join(" ")
	},
	showUl: function(a) {
		if (a) a.className = ""
	},
	hideUl: function(a) {
		if (a) a.className = "hide"
	},
	bindEmailTipsEvent: function() {
		var a = $("other_email_ul"),
			b = $("other_email");
		$.e.add(a, "mousemove", function(a) {
			var b = a.target;
			if (b.tagName.toLowerCase() == "li") {
				var e = $("emailTips_" + index.listIndex[7]);
				if (e) e.className = "";
				b.className = "hover";
				index.listIndex[7] = index.getIndexFromId(b.getAttribute("id"));
				a.stopPropagation()
			}
		});
		$.e.add(a, "mouseout", function(a) {
			if (a.target.tagName.toLowerCase() == "li") a.target.className = "", a.stopPropagation()
		});
		$.e.add(a, "click", function(c) {
			if (c.target.nodeName.toLowerCase() == "li") b.value = $.html.decode(c.target.innerHTML), a.className = "hide", index.isChangingTab() || index.chkOtherEMail(), $("nick").focus(), c.stopPropagation()
		});
		$.e.add(b, "keydown", function(b) {
			index.moveList($("other_email"), a, b, 7)
		})
	},
	isEnglishWord: function(a) {
		return index.enWordReg.test(a)
	},
	searchResultToMap: function(a) {
		for (var b = {}, c = a.length, d = 0; d < c; d++) {
			var e = a[d].split(":");
			e.length == 2 && (b[e[0]] = e[1])
		}
		return b
	},
	bindAreaSearchEvent: function() {
		$.e.add($("country_value"), "keyup", function(a) {
			a = a.keyCode;
			a != index.keyCode.UP && a != index.keyCode.DOWN && a != index.keyCode.ENTER && a != index.keyCode.TAB && (window.clearTimeout(index.searchTimeoutId[4]), index.searchTimeoutId[4] = window.setTimeout(function() {
				var a = encodeURIComponent($("country_value").value.trim()),
					c = index.areaSearchUrl + "?type=1&word=" + a;
				a ? index.search_area(c, $("country_ul"), 4) : (index.changeCountry(), index.country = index.noAreaStr)
			}, 500))
		});
		$.e.add($("province_value"), "keyup", function(a) {
			a = a.keyCode;
			a != index.keyCode.UP && a != index.keyCode.DOWN && a != index.keyCode.ENTER && a != index.keyCode.TAB && (window.clearTimeout(index.searchTimeoutId[5]), index.searchTimeoutId[5] = window.setTimeout(function() {
				var a = encodeURIComponent($("province_value").value.trim()),
					c = index.areaSearchUrl + "?type=2&word=" + a + "&countryid=" + index.country;
				a ? index.search_area(c, $("province_ul"), 5) : (index.changeProvince(null, true), index.province = index.noAreaStr)
			}, 500))
		});
		$.e.add($("city_value"), "keyup", function(a) {
			a = a.keyCode;
			a != index.keyCode.UP && a != index.keyCode.DOWN && a != index.keyCode.ENTER && a != index.keyCode.TAB && (window.clearTimeout(index.searchTimeoutId[6]), index.searchTimeoutId[6] = window.setTimeout(function() {
				var a = encodeURIComponent($("city_value").value.trim()),
					a = index.areaSearchUrl + "?type=3&word=" + a + "&countryid=" + index.country + "&provinceid=" + index.province;
				$("city_value").value ? index.search_area(a, $("city_ul"), 6) : (index.changeCity(null, true), index.city = index.noAreaStr)
			}, 500))
		})
	},
	setSelectBlurValue: function(a, b, c) {
		a = a.getElementsByTagName("li");
		if (index.listIndex[c] >= 0 && (a = a[index.listIndex[c]])) {
			var d = a.getAttribute("value");
			b.value = $.html.decode(a.innerHTML);
			index.updateListIndex(c, index.listIndex[c]);
			switch (c) {
			case 1:
				index.year = d;
				index.showDate.year = index.year;
				break;
			case 2:
				index.month = d;
				b = a.getAttribute("isLeap");
				index.isLeap = b ? b : "1";
				index.showDate.month = index.month;
				index.showDate.isLeap = index.isLeap == 1 ? false : true;
				break;
			case 3:
				index.day = d;
				index.showDate.day = index.day;
				break;
			case 4:
				index.country = d;
				break;
			case 5:
				index.province = d;
				break;
			case 6:
				index.city = d
			}
		}
	},
	bindTimeSearchEvent: function() {
		$.e.add($("year_value"), "keyup", function(a) {
			a = a.keyCode;
			a != index.keyCode.UP && a != index.keyCode.DOWN && a != index.keyCode.ENTER && a != index.keyCode.TAB && (window.clearTimeout(index.searchTimeoutId[1]), index.searchTimeoutId[1] = window.setTimeout(function() {
				var a = $("year_value").value;
				index.search_time($("year_ul"), 1, a)
			}, 50))
		});
		$.e.add($("month_value"), "keyup", function(a) {
			a = a.keyCode;
			a != index.keyCode.UP && a != index.keyCode.DOWN && a != index.keyCode.ENTER && a != index.keyCode.TAB && (window.clearTimeout(index.searchTimeoutId[2]), index.searchTimeoutId[2] = window.setTimeout(function() {
				var a = $("month_value").value;
				index.search_time($("month_ul"), 2, a)
			}, 50))
		});
		$.e.add($("day_value"), "keyup", function(a) {
			a = a.keyCode;
			a != index.keyCode.UP && a != index.keyCode.DOWN && a != index.keyCode.ENTER && a != index.keyCode.TAB && (window.clearTimeout(index.searchTimeoutId[3]), index.searchTimeoutId[3] = window.setTimeout(function() {
				var a = $("day_value").value;
				index.search_time($("day_ul"), 3, a)
			}, 50))
		})
	},
	ulToSelectArr: function(a, b) {
		var j;
		switch (b) {
		case 1:
			index.yearSearchArr = [];
			break;
		case 2:
			index.monthSearchArr = [];
			break;
		case 3:
			index.daySearchArr = []
		}
		for (var c = a.getElementsByTagName("li"), d = null, e = null, f = null, d = 1, h = 0, i = c.length; h < i; h++) switch (d = c[h], e = d.getAttribute("value"), f = d.innerHTML, e = {
			id: e,
			name: f
		}, b) {
		case 1:
			index.yearSearchArr.push(e);
			break;
		case 2:
			j = (d = d.getAttribute("isleap")) ? d : 1, d = j;
			e.isLeap = d;
			index.monthSearchArr.push(e);
			break;
		case 3:
			index.daySearchArr.push(e)
		}
	},
	arrayToUl: function(a, b, c) {
		for (var d = [], e = 0, f = a.length; e < f; e++) {
			var h = a[e],
				i = h.id,
				h = h.name,
				j = "",
				j = "";
			switch (c) {
			case 1:
				j = "year_" + e;
				j = e == 0 ? "<li value=" + i + ' class="hover" id=' + j + ">" + h + "</li>" : "<li value=" + i + " id=" + j + ">" + h + "</li>";
				break;
			case 2:
				var j = "month_" + e,
					k = a[e].isLeap,
					j = e == 0 ? "<li value=" + i + ' class="hover" isLeap=' + k + " id=" + j + ">" + h + "</li>" : "<li value=" + i + " isLeap=" + k + " id=" + j + ">" + h + "</li>";
				break;
			case 3:
				j = "day_" + e, j = e == 0 ? "<li value=" + i + ' class="hover" id=' + j + ">" + h + "</li>" : "<li value=" + i + " id=" + j + ">" + h + "</li>"
			}
			d.push(j)
		}
		e > 0 ? index.updateListIndex(c, 0) : index.updateListIndex(c, -1);
		b.innerHTML = d.join(" ")
	},
	search_time: function(a, b, c) {
		c = c.trim();
		a.scrollTop = 0;
		index.selectHasSelected[b] = false;
		var d = [],
			e = [];
		switch (b) {
		case 1:
			e = index.yearSearchArr;
			break;
		case 2:
			e = index.monthSearchArr;
			break;
		case 3:
			e = index.daySearchArr
		}
		for (var f = 0, h = e.length; f < h; f++)((e[f].id + "").indexOf(c) > -1 || (e[f].name + "").indexOf(c) > -1) && d.push(e[f]);
		d.length == 0 && (d = e);
		index.arrayToUl(d, a, b);
		index.showUl(a);
		index.selectListState[b] = 1
	},
	bindInputSearchEvent: function() {
		$.e.add($("year_ul"), "scroll", function() {
			index.showInputSearchTips(1)
		});
		$.e.add($("month_ul"), "scroll", function() {
			index.showInputSearchTips(2)
		});
		$.e.add($("day_ul"), "scroll", function() {
			index.showInputSearchTips(3)
		});
		$.e.add($("country_ul"), "scroll", function() {
			index.showInputSearchTips(4)
		});
		$.e.add($("province_ul"), "scroll", function() {
			index.showInputSearchTips(5)
		});
		$.e.add($("city_ul"), "scroll", function() {
			index.showInputSearchTips(6)
		})
	},
	showInputSearchTips: function(a) {
		var b = $("inptu_search_tips");
		$("inptu_search_tips_wording").innerHTML = index.inputSearchTipsArray[a - 1];
		index.birthdayTipsShow && a < 4 && (a = 0);
		index.areaTipsShow && a >= 4 && (a = 0);
		switch (a) {
		case 1:
			b.style.display = "block";
			b.style.top = "-31px";
			b.style.left = "100px";
			b.style.width = "158px";
			index.birthdayTipsShow = true;
			break;
		case 2:
			b.style.display = "block";
			b.style.top = "-31px";
			b.style.left = "180px";
			b.style.width = "145px";
			index.birthdayTipsShow = true;
			break;
		case 3:
			b.style.display = "block";
			b.style.top = "-31px";
			b.style.left = "250px";
			b.style.width = "145px";
			index.birthdayTipsShow = true;
			break;
		case 4:
			b.style.display = "block";
			b.style.top = "9px";
			b.style.left = "40px";
			b.style.width = "181px";
			index.areaTipsShow = true;
			break;
		case 5:
			b.style.display = "block";
			b.style.top = "9px";
			b.style.left = "140px";
			b.style.width = "181px";
			index.areaTipsShow = true;
			break;
		case 6:
			b.style.display = "block", b.style.top = "9px", b.style.left = "250px", b.style.width = "181px", index.areaTipsShow = true
		}
	},
	hideInputSearchTips: function() {
		$("inptu_search_tips").style.display = "none"
	},
	rsaEncrypt: function(a) {
		var b = new RSAKey;
		b.setPublic("C4D23C2DB0ECC904FE0CD0CBBCDC988C039D79E1BDA8ED4BFD4D43754EC9693460D15271AB43A59AD6D0F0EEE95424F70920F2C4A08DFDF03661300047CA3A6212E48204C1BE71A846E08DD2D9F1CBDDFF40CA00C10C62B1DD42486C70A09C454293BCA9ED4E7D6657E3F62076A14304943252A88EFA416770E0FBA270A141E7", "10001");
		return b.encrypt(a)
	},
	hasNoEmail: function() {
		index.changeTab(1);
		index.changeInit();
		index.mailRegReport(1)
	}
};
index.init();
isd_t.push(new Date - 0);

function A(a, b) {
	index.aq_object[a] = b
}
function initLocation(a) {
	index.loadLocation(a)
};