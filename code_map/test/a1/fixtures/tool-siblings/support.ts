export function validateParcel(parcel: string) { return parcel.trim(); }
export function sealParcel(parcel: string) { return `sealed:${parcel}`; }
export function chillParcel(parcel: string) { return `chilled:${parcel}`; }
export function stampParcel(parcel: string) { return `stamped:${parcel}`; }
