function format_phonenumber(phone) {
  if(!phone.includes("-")) {
    var new_phone = phone.substring(0,3) + "-";
    new_phone += phone.substring(3,6) + "-" + phone.substring(6,10);
    return new_phone;
  } else {
    return phone;
  }
}
