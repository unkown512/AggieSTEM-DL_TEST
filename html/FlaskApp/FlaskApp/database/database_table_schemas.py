# Tables and column descriptions for `aggiestemdl`. See the aggiestemdl_db_strucure PDF

def db_table_schemas():
  table_list = [
    "user",
    "security",
    "question",
    "profile"
    ]

  # `Key` is table name and `value` is an array of columns
  table_attributes = {
    "user": [
      ["username", "varchar(20)", "not null", "First Initial + Last Name", ""],
      ["position", "varchar(3)", "not null", "Researcher (R), Senior Doc (S), Director (D)", ""],
      ["email", "varchar(321)", "not null UNIQUE", "Unique email address", ""],
      ["phone_number", "varchar(11)", "not null UNIQUE", "Contact Number", ""],
      ["privacy_agreement", "varchar(1)", "not null", "Cache and privacy info.", ""],
      ["contact_agreement", "varchar(1)", "not null", "text messages and email notifications", ""],
      ["last_login", "timestamp", "not null default current_timestamp on update current_timestamp", "last login UTC time", ""],
      ["deleted", "varchar(1)", "not null default 0", "", ""],
      ["recno", "BIGINT", " not null auto_increment", "Unique record number (row)", ""]
    ],
    "security" : [
      ["password", "varchar(350)", "not null", "pw", ""],
      ["question1", "varchar(25)", "not null", "q1 answer", ""],
      ["question2", "varchar(25)", "not null", "q2 answer", ""],
      ["question3", "varchar(25)", "not null", "q3 answer", ""],
      ["request_new_pw", "varchar(1)", "not null default 0", "flag to change password", ""],
      ["user_id", "BIGINT", "not null UNIQUE", "FK to user table", "Y"],
      ["access_level", "SMALLINT", "not null default 0", "", ""],
      ["recno", "BIGINT", " not null auto_increment", "Unique record number (row)", ""]
    ],
    "question" : [
      ["question1", "varchar(25)", "not null", "", ""],
      ["question2", "varchar(25)", "not null", "", ""],
      ["question3", "varchar(25)", "not null", "", ""],
      ["recno", "BIGINT", " not null auto_increment", "Unique record number (row)", ""]
    ],
    "profile": [
      ["external_link", "varchar(250)", "", "Link to website, cv, or research papers", ""],
      ["ref_name", "varchar(25)", "", "external_link display name", ""],
      ["user_id", "BIGINT", "not null", "link to user table not unique", "Y"],
      ["recno", "BIGINT", " not null auto_increment", "Unique record number (row)", ""]

    ]
  }
  return (table_list, table_attributes)
