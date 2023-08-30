const blkDuration = 15;

function getDateString(date) {
	return date.toLocaleDateString('en-us', { weekday: 'long'}) + ", " + (date.getMonth() + 1) + "/" + date.getDate() + "/" + date.getFullYear();
}

function getBlockString(date, start, total) {
	dStr = date.toLocaleDateString('en-us', { weekday: 'long'}) + ", " + (date.getMonth() + 1) + "/" + date.getDate() + "/" + date.getFullYear();
	let hrStart = Math.floor(start / 60) % 12;
	if (hrStart == 0) {
		hrStart = 12;
	}
	let hrEnd = Math.floor((start + total) / 60) % 12;
	if (hrEnd == 0) {
		hrEnd = 12;
	}
	tStr = " (" + hrStart.toString() + " - " + hrEnd.toString() + ")";

	return  dStr + tStr;
}

function getDateValue(date) {
	return date.toISOString().substring(0, 10);
}

function getBlockValue(date, start) {
	return date.toISOString().substring(0, 11) + Math.floor(start / 60).toString();
}