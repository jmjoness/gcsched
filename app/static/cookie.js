function daysToMinutes(days) {
	return days * 24 * 60;
}

function setCookie(cname, cvalue, exminutes) {
	const d = new Date();
	d.setTime(d.getTime() + (exminutes * 60 * 1000));
	const expires = "expires=" + d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";SameSite=Lax;path=/";
}

function getCookie(cname) {
	const name = cname + "=";
	const ca = document.cookie.split(';');
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

function deleteCookie(cname) {
	document.cookie = cname + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC;SameSite=Lax;path=/";
}

function clearCookies() {
	document.cookie.split(";").forEach(function (c) {
		document.cookie = "lastid=;expires=" +
			new Date().toUTCString() + ";SameSite=Lax;path=/";
	});
}
