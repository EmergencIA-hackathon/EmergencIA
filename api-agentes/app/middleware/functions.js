export function getDateTime() {
    const dateObj = new Date();

    let time = dateObj.toTimeString().slice(0, 8);
    let hours = time.slice(0, 3);
    hours = parseInt(hours) - 3;

    time = `${hours}:${time.slice(3, 8)}`;

    const day =
        dateObj.getDate() > 9 ? dateObj.getDate() : `0${dateObj.getDate()}`;
    const month =
        dateObj.getMonth() + 1 > 9
            ? dateObj.getMonth() + 1
            : `0${dateObj.getMonth() + 1}`;
    const year = dateObj.getFullYear();

    const dateTime = {
        date: `${day}/${month}/${year}`,
        time: time,
    };

    return dateTime;
}
